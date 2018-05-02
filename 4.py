# -*- coding: utf-8 -*-
# @Date    : 2017/8/25 0025 , @Author  : fengshaomin@bjsasc.com
from collections import defaultdict
from operator import  itemgetter
rows = [
{'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
{'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
{'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

a  = sorted(rows,key = itemgetter('uid','fname'))
print(a)