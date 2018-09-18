# coding:utf-8
import time
import requests


ss = requests.session()

vcode = ss.post('http://127.0.0.1:5000/file_name', data={'image_url': 'http://www.libopac.seu.edu.cn:8080/reader/captcha.php'})

result = vcode.content

print(result)