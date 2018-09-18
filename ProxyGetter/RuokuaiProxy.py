# coding=utf8

import requests
import time


def ruokuai(username, passwd, filename, app_id, app_key, codetype, retry=3):
    app_id = str(app_id)
    params = {
        'typeid': codetype,
        'timeout': 60,
        'username': username,
        'password': passwd,
        'softid': app_id,
        'softkey': app_key
    }
    file = {'image': ('a.jpg', filename)}
    headers = {
        'Connection': 'Keep-Alive',
        'Expect': '100-continue',
        'User-Agent': 'ben'
    }
    try:
        response = requests.post('http://api.ruokuai.com/create.json', data=params, files=file, headers=headers)
        if response.status_code == 200:
            verify_code = response.json().get('Result', '')
            if verify_code:
                return verify_code

        elif response.status_code != 200 and retry != 0:
             retry -= 1
             return ruokuai(username, passwd, filename, app_id, app_key, codetype, retry)
        else:
            return 'error'
    except Exception, e:
        return 'error'


def main(file_name):
    username = 'xxxxx'
    password = 'xxxxxx'
    app_id = 112207
    app_key = 'edb33d89dfe3447db25d040ff97060d0'

    # file_name = '../static/image.jpg'

    vcode = ruokuai(username,password,file_name, app_id, app_key, 2040)
    plat = 'ruokuai'
    return plat, vcode


if __name__ == '__main__':
    image_url = 'http://www.libopac.seu.edu.cn:8080/reader/captcha.php'
    sess = requests.Session()
    file_name = sess.get(image_url).content
    print(main(file_name))

