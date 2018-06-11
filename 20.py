# -*- coding: utf-8 -*-  
# @Date : 2018-06-11 10:08:54 , @Author : fengshaomin@bjsasc.com 
# conding:utf-8

import yaml

with open("application.yml",encoding="utf-8") as f:
    d = yaml.load(f)
    print(d['server']['port'])
