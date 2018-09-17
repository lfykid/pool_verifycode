# -*- coding: utf-8 -*-
import time

import requests
from flask import Flask, jsonify, request

from Util.GetConfig import GetConfig
from Manager import ProxyManager
from ProxyGetter import RuokuaiProxy
from db.mysql_handler import MysqlHandler

mysql = MysqlHandler()

app = Flask(__name__)


@app.route('/file_name/', methods=['POST'])
def get_filename():
    image_url = request.form.get('image_url')
    sess = requests.Session()
    file_name = sess.get(image_url).content
    result = ProxyManager.get_result(file_name)
    return jsonify({'identify_code':result}) if result and result != 'error' else 'didn`t get code'


def run():
    config = GetConfig()
    app.run(host=config.host_ip, port=config.host_port)


if __name__ == '__main__':
    run()
