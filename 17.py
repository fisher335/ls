#-*- coding: utf-8 -*-
# @Date    : '2018/4/25 0025'
# @Author  : Terry feng  (fengshaomin@qq.com)
import os,json
import pandas as pd
from collections import Counter
def getdata():

    with open("jsondata100.txt",'r',encoding='utf-8') as f:
        info = json.loads(f.read())

        print(len(info))
        return list(info)

if __name__ == '__main__':
    data = getdata()
    print(type(data))
    aa = Counter(data)
    print(aa)
