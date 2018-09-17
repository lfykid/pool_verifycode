# coding: utf-8

import time
import mysql_models
import json
from tenacity import *
from pprint import pprint
from Util.LogHandler import LogHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Util.GetConfig import GetConfig

config = GetConfig()

MYSQL_URL = config.mysql_url


class MysqlHandler(object):

    def __init__(self, mysql_url = None):

        if mysql_url == None:
            self.engine = create_engine(MYSQL_URL, pool_recycle=7200, pool_pre_ping=True, pool_size=15)
        else:
            self.engine = create_engine(mysql_url, pool_recycle=7200, pool_pre_ping=True, pool_size=15)
        self.dbSession = sessionmaker(bind=self.engine)
        self.logger = LogHandler("MysqlHandler")
        self.models = {}

    @retry(stop=stop_after_attempt(3),
           wait=wait_fixed(0.5),
           retry=retry_if_result(lambda p: p is None),
           retry_error_callback=lambda p: p.result())
    def store_one(self, data, model_name, cols_feed_back = []):

        if model_name not in self.models:
            self.models[model_name] = getattr(mysql_models, model_name)
        model = self.models[model_name]

        feed_back = {}
        session = self.dbSession()
        try:
            sql_data = model(data)
            session.add(sql_data)
            session.commit()

            for col in cols_feed_back:
                feed_back[col] = getattr(sql_data, col)

        except Exception, e:
            self.logger.error("store failed: {}".format(e))
            session.rollback()
            session.close()
            return None
        session.close()

        return feed_back

    def store(self, data_list, model_name):

        store_count = 0
        for data in data_list:

            if self.store_one(data) is None:
                self.logger.error("store data failed model_name:{} data:{}".format(model_name, json.dumps(data)))
                continue

            store_count += 1

        return store_count

    @retry(stop=stop_after_attempt(3),
           wait=wait_fixed(0.5),
           retry=retry_if_result(lambda p: p is None),
           retry_error_callback=lambda p: p.result())
    def update_or_insert_one(self, data, model_name, key_cols, update = True):

        if model_name not in self.models:
            self.models[model_name] = getattr(mysql_models, model_name)
        model = self.models[model_name]

        session = self.dbSession()
        new_node = model(data)
        try:

            rows = session.query(model)
            for key_col in key_cols:
                rows = rows.filter(getattr(model, key_col) == getattr(new_node, key_col))
            rows = rows.all()

            if len(rows) > 1:
                self.logger.error("query muti rows by cols {} with {}".format(key_cols, data))
                session.close()
                return None
            elif len(rows) == 1:
                node = rows[0]
            else:
                node = None

        except Exception, e:
            self.logger.error("query failed: {}".format(e))
            session.close()
            return None

        try:
            if node:
                if update:
                    attrs = filter(lambda attr: False if "_" in attr and attr.index("_") == 0 or \
                                                    attr in ("id", "metadata") else True, node.__dict__)
                    for attr in attrs:
                        setattr(node, attr, getattr(new_node, attr))
                    session.commit()
            else:
                session.add(new_node)
                session.commit()
        except Exception, e:
            self.logger.error("update failed: {}".format(e))
            session.close()
            return None

        session.close()
        return True

    def query(self, data, model_name, key_cols, delete = False):

        if model_name not in self.models:
            self.models[model_name] = getattr(mysql_models, model_name)
        model = self.models[model_name]

        session = self.dbSession()
        new_node = model(data)
        try:

            rows = session.query(model)

            for key_col in key_cols:
                rows = rows.filter(getattr(new_node, key_col) == getattr(model, key_col))
            if delete:
                rows.delete()
                session.commit()
            else:
                rows = rows.all()

        except Exception, e:
            self.logger.error("query failed: {}".format(e))
            session.close()
            return None

        session.close()
        return rows

    # @retry(stop=stop_after_attempt(3),
    #        wait=wait_fixed(0.5),
    #        retry=retry_if_result(lambda p: p is None),
    #        retry_error_callback=lambda p: p.result())
    def get_last(self, model_name, key_col):

        if model_name not in self.models:
            self.models[model_name] = getattr(mysql_models, model_name)
        model = self.models[model_name]

        session = self.dbSession()
        record = None
        try:
            record = session.query(model).order_by(getattr(model, key_col).desc()).first()
        except Exception, e:
            self.logger.error("get last failed: {}".format(e))
            session.close()
            return None

        return record if record else None


if __name__ == "__main__":

     logic = MysqlHandler()
     a = logic.query({'symbol':'BTC',}, 'CoinInfo', ['symbol'])
     print(a)