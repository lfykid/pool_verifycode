# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from Util.GetConfig import GetConfig
from Util.LogHandler import LogHandler
from ProxyGetter import RuokuaiProxy
from ProxyGetter import FeiFeiProxy
from ProxyGetter import YundmProxy
from db.mysql_handler import MysqlHandler
from gevent.queue import Queue, Empty
import time
import gevent
import requests

mysql = MysqlHandler()

final_code = []


def get1(file_name):
    start = time.time()
    plat, result = RuokuaiProxy.main(file_name)
    final_code.append(result.lower())
    end_time = time.time() - start
    req_time = round(end_time, 2)
    print(plat, result)
    print(req_time)

    post = {
        'photo':file_name,
        'identify_code':result,
        'req_time': req_time,
        'plat':plat,
        'created': int(time.time()),
    }
    mysql.store_one(post, 'CodeProxy', ['id'])
    return result


def get2(file_name):
    start = time.time()
    plat, result = FeiFeiProxy.main(file_name)
    final_code.append(result.lower())
    end_time = time.time() - start
    req_time = round(end_time, 2)
    print(plat, result)
    print(req_time)

    post = {
        'photo':file_name,
        'identify_code':result,
        'req_time': req_time,
        'plat':plat,
        'created': int(time.time()),
    }
    mysql.store_one(post, 'CodeProxy', ['id'])
    return result


def get3(file_name):
    start = time.time()
    plat, result = YundmProxy.main(file_name)
    final_code.append(result.lower())
    end_time = time.time() - start
    req_time = round(end_time, 2)
    print(plat, result)
    print(req_time)

    post = {
        'photo':file_name,
        'identify_code':result,
        'req_time': req_time,
        'plat':plat,
        'created': int(time.time()),
    }
    mysql.store_one(post, 'CodeProxy', ['id'])
    return result


def get_result(file_name):
    gevent.joinall([
        gevent.spawn(get1, file_name),
        gevent.spawn(get2, file_name),
        gevent.spawn(get3, file_name),
    ])
    for val in list(set(final_code)):
        if final_code.count(val) >= 2:
           return val


if __name__ == '__main__':
    # pp = ProxyManager()
    image_url = 'http://www.libopac.seu.edu.cn:8080/reader/captcha.php'
    sess = requests.Session()
    file_name = sess.get(image_url).content
    print(get_result(file_name))
