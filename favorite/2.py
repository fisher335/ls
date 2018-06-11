# -*- coding: utf-8 -*-  
# Date    : 2017-08-30 13:41:26 , @Author  : fengshaomin@bjsasc.com
from aip import AipOcr
import json
import time
import os

# 定义常量  
APP_ID = '10359139'
API_KEY = 'QYYZy5SLg8SK7POzuzR4FqEt'
SECRET_KEY = 'BN036LzWI1XzA32GIP0raf911XRvG0pu'

# 初始化AipFace对象  
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 读取图片  
filePath = "2.jpg"


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

        # 定义参数变量


options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

# 调用通用文字识别接口  
result = aipOcr.basicGeneral(get_file_content(filePath), options)

s = str(result)
no = s.find("发票代码")
num = s.find("发票号码")
date = s.find("开票日期")
che = s.find("校验码")
che_f = s.find("'", che, che + 25)
print(s[che:che + 20])
print(s[che:che_f])
print(s[no + 5:num], s[num + 5:date], s[date + 5:che], s[che:che_f][-6:])

s_no = s[no + 5:num]
s_num = s[num + 5:date]
s_date = s[date + 5:che][0:4] + s[date + 5:che][5:7] + s[date + 5:che][8:-1]
print(s_date)
s_yzm = s[che:che_f][-6:]

from selenium import webdriver

try:
    browser = webdriver.Ie()
    browser.get("https://inv-veri.chinatax.gov.cn/")
    fpdm = browser.find_element_by_id("fpdm")
    fpdm.send_keys(s_no)
    fpdm.click()
    time.sleep(2)
    fphm = browser.find_element_by_id("fphm")
    fphm.send_keys(s_num)
    time.sleep(2)
    kqrq = browser.find_element_by_id("kprq")
    kqrq.send_keys(s_date)
    time.sleep(2)
    jym = browser.find_element_by_id("kjje")
    jym.send_keys(s_yzm)
    time.sleep(200000)
except:
    print("1111")
finally:
    browser.close()
