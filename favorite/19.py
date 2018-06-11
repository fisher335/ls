# -*- coding: utf-8 -*-
# @Date    : '2018/6/6 0006'
# @Author  : Terry feng  (fengshaomin@qq.com)
from fake_useragent import UserAgent

ua = UserAgent()

for i in range(10):
    print(ua.random)
