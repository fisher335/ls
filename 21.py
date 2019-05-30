# -*- coding: utf-8 -*-
# @Date    : '2019/2/27 0027'
# @Author  : Terry feng  (fengshaomin@qq.com)
import os

from requests_html import HTMLSession

session = HTMLSession()
my_url = 'https://www.jianshu.com/u/1f9e71a85238'
my_requests = session.get(url=my_url)
my_requests.html.render(scrolldown=5,sleep=2)
titles = my_requests.html.find('a.title')
for i,title in enumerate(titles):
    print(f'{i+1} {title.text}：https://www.jianshu.com{title.attrs["href"]}')