# coding: utf-8


import re
import json
import time
import requests
from tenacity import *


def yundama(username, passwd, filename, app_id, app_key, codetype, retry=3):
    app_id = str(app_id)
    time_out = 60
    data = {'method': 'upload', 'username': username, 'password': passwd, 'appid': app_id,
            'appkey': app_key, 'codetype': codetype, 'timeout': time_out}
    file = {'file': filename}
    try:
        response = requests.post('http://api.yundama.com/api.php', data, files=file)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            res = response_dict['cid']
            if res > 0:
                for i in range(0, time_out):
                    vcode = result(username, passwd, app_id, app_key, str(res))
                    if vcode != '':
                        return vcode
        elif response.status_code != 200 and retry != 0:
             retry -= 1
             yundama(username, passwd, filename, app_id, app_key, codetype, retry)
        else:
            return
    except Exception, e:
        return 'error'


def result(username, passwd, app_id, app_key, cid):
    data = {'username': username, 'password': passwd, 'appid': app_id,
            'appkey': app_key, 'cid':cid}
    response = requests.post('http://api.yundama.com/api.php?method=result', data)
    code = response.json().get('text','')
    return code


# class DmptHttp(object):
#     def __init__(self, name, passwd, filename):
#         self.username = name
#         self.password = passwd
#         # self.appid = str(app_id)
#         # self.appkey = app_key
#         # self.codetype = codetype
#         self.filename = filename
#         self.timeout = 60
#
#     def yundama(self,app_id, app_key, codetype):
#         appid = str(app_id)
#         data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': appid,
#                 'appkey': app_key, 'codetype': codetype, 'timeout': self.timeout}
#         f = open(self.filename, 'rb')
#         file = {'file': f}
#         response = requests.post('http://api.yundama.com/api.php?method=upload', data, files=file).text
#         f.close()
#         response_dict = json.loads(response)
#         result = response_dict['text']
#         return result
#
#     def feifeidama(self):
#         pass


# def code_verificate():
#     username = 'wangjiangrong'
#     password = 'wjr_123'
#     app_id = 1
#     app_key = '22cc5376925e9387a23cf797cb9ba745'
#
#     file_name = '../static/image.jpg'
#
#     yundama_obj = DmptHttp(username, password, file_name)
#     start = time.time()
#     result = yundama_obj.yundama(app_id, app_key, 5000)
#     end = time.time() - start
#     count = 0
#     while not result:
#         count += 1
#         if count >= 5:
#             break
#         result = yundama_obj.yundama(app_id, app_key, 5000)
#         if result:
#             break
#     photo = open(file_name, 'rb').read()
#     with open("../dm_images/{}_{}s.jpg".format(result, end), "wb") as f:
#         f.write(photo)
#
#     return result

def main(file_name):
    username = 'xxxxx'
    password = 'xxxxx'
    app_id = 5705
    app_key = 'c7a65ca7eb91045548d7aef35a05770d'

    # file_name = '../static/image.jpg'

    vcode = yundama(username,password,file_name, app_id, app_key, 3004)
    plat = 'yundama'
    return plat, vcode


if __name__ == '__main__':
    image_url = 'http://www.libopac.seu.edu.cn:8080/reader/captcha.php'
    sess = requests.Session()
    file_name = sess.get(image_url).content
    print(main(file_name))