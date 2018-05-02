# -*- coding: utf-8 -*-  
# @Date    : 2017-08-28 14:59:02 , @Author  : fengshaomin@bjsasc.com 
import os,sys
from functools import partial
with open('1.txt','rb') as f:
    records = iter(partial(f.read,4),b'')
    for i in records:
        print(i)
