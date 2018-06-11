# -*- coding: utf-8 -*-
# @Date    : '2018/4/24 0024'
# @Author  : Terry feng  (fengshaomin@qq.com)
import os
from io import StringIO
import json, time
import datetime

from random import randint

t = time.time()
print(int(t))

d = {"name": "fengshaomin", "time": t + 7200}

c = json.dumps(d)
print(c)

a = StringIO()
a.write(c)
b = a.getvalue()
e = json.loads(b)
print(e['time'])
