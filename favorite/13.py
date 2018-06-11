#-*- coding: gbk -*-
# @Date    : '2018/3/27 0027'
# @Author  : Terry feng  (fengshaomin@qq.com)
from requests_html import  HTMLSession

client  = HTMLSession()
r = client.get("https://www.qiushibaike.com/text/")
a = r.html.find(".content")
for i in a:
    print(i.text)
    print("--------------------------")