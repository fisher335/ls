#-*- coding: utf-8 -*-
# @Date    : '2018/4/16 0016'
# @Author  : Terry feng  (fengshaomin@qq.com)
import qrcode

data = "中文测试"
# try:
#     data = data.decode('utf-8').encode('sjis').decode('utf-8')
# except:
#     data = data
img=qrcode.make(data)
img.save("fengshaomin.png")