# -*- coding:utf-8 -*-

import requests
import json

class YuanPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【golang新手】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        return re_dict

if __name__ == '__main__':
    yunpian = YuanPian("28918179b6d76619951c676e08591497")
    yunpian.send_sms("1234","17621906833")