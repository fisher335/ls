#-*- coding: utf-8 -*-
# @Date    : '2018/4/25 0025'
# @Author  : Terry feng  (fengshaomin@qq.com)
import json
from collections import Counter
def getdata():

    with open("jsondata100.txt",'r',encoding='utf-8') as f:
        info = json.loads(f.read())

        print(len(info))
        return list(info)

if __name__ == '__main__':
    # data = getdata()
    # print(type(data))
    #
    data = {"name":"fengshaomin","age":11}
    aa = data
    aa["agender"] = "男"
    aa["爱好"]="chifan"
    aa["shunxu"]=1
    print(aa)
