# -*- coding: utf-8 -*-
# @Date    : 2017/10/9 0009 , @Author  : fengshaomin@bjsasc.com
import requests
import json
import util.desencript

class NetDisk:
    auth_token = ""
    rest_api = "http://disk.bjsasc.com:8180/NetDisk/rest/mobile"

    def __init__(self, userName, passWord):
        params = {"method": "login",
                  "userName": userName, "passWord": passWord}
        result = requests.get(self.rest_api, params=params)
        # print(result.json())
        if "token" in result.json():
            self.auth_token = result.json()['token']
        else:
            self.auth_token = ""

    def getFilelist(self, page=1):
        header = {"Authorization": self.auth_token}
        params = {"method": "mobile_list", "start": (page - 1) * 10}
        result = requests.post(self.rest_api, params=params, headers=header)
        print(result.text)
        if "rows" in result.text:
            return result.json()["rows"]
        else:
            return []

if __name__ == '__main__':
    a = NetDisk(userName="fengshaomin", passWord="1")
    # print(a.auth_token)
    li = a.getFilelist(1)
    print(len(li))
    for i in li:
        print(i)
