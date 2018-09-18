# coding=utf-8

import base64
import hashlib
import time
import json
import requests


def CalcSign(usr_id, passwd, timestamp):
    md5 = hashlib.md5()
    md5.update(timestamp + passwd)
    csign = md5.hexdigest()

    md5 = hashlib.md5()
    md5.update(usr_id + timestamp + csign)
    csign = md5.hexdigest()
    return csign


def predict(usr_id, usr_key, app_id, app_key,  pred_type, img_data, retry=3):
    tm = str(int(time.time()))
    sign = CalcSign(usr_id, usr_key, tm)
    img_base64 = base64.b64encode(img_data)
    param = {
            "user_id": usr_id,
            "timestamp":tm,
            "sign":sign,
            "predict_type":pred_type,
            "img_data":img_base64,
            }
    if app_id != "":
        asign = CalcSign(app_id, app_key, tm)
        param["appid"] = app_id
        param["asign"] = asign
    url = "http://pred.fateadm.com/api/capreg"
    headers = {'headers':'Mozilla/5.0'}
    try:
        response = requests.post(url, data=param, headers=headers)
        if response.status_code == 200:
            result = response.json().get('RspData')
            vcode = json.loads(result).get('result','')
            if vcode:
                return vcode
        elif response.status_code != 200 and retry != 0:
             retry -= 1
             return predict(usr_id, usr_key, app_id, app_key, pred_type, img_data, retry)
        else:
            return 'error'
    except Exception, e:
        return 'error'




def main(file_name):
    pd_id = "105595"
    pd_key = "TzcIOF/kiQSRuHt7LZOVfeOQnDWQfda4"
    app_id = "305595"
    app_key = "8qNaHA1JIiIHg+WRaMF6i4gs74DkCVYf"
    pred_type = "20400"


    # 如果是通过url直接获取内存图片，这直接调用Predict接口就好

    # with open('a.jpg','wb') as f:
    #     f.write(file_name)
    rsp = predict(pd_id, pd_key, app_id, app_key, pred_type, file_name)
    plat = 'feifei'
    return plat, rsp


if __name__ == "__main__":
    image_url = 'http://www.libopac.seu.edu.cn:8080/reader/captcha.php'
    sess = requests.Session()
    file_name = sess.get(image_url).content
    print(main(file_name))


