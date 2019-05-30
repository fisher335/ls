# -*- coding: utf-8 -*-
# @Date : 2018-06-11 10:08:54 , @Author : fengshaomin@bjsasc.com
# conding:utf-8
import requests

uri = "https://api.github.com/repos/fisher335/wiki/issues/6/comments"
token = "aba9f55145d03581d6e236d459ff2e5f08cbff7a"
header = {"Authorization ": {"token":token}}
header2 = {"Authorization ": {"token":token},"Content-Type": "application/json"}
a = requests.post(uri, headers = header)

print(a.status_code)
print(a.content)
d = a.json()
print(d)
for index, k in enumerate(d):
    if "beego" in k["body"]:
        print(k["url"])
        if (len(k["url"]) > 0):
            b = requests.get(k["url"][1])
            print(b.json())

print(len(d))
