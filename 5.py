# -*- coding: utf-8 -*-  
# @Date    : 2017-08-28 14:54:44 , @Author  : fengshaomin@bjsasc.com 
import heapq
print('jim',100)
portfolio = [('jim',100),
('tom',12),
('sun',46),
('kum',89)
]

def sort(var):
    return var[1]

num = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
a = heapq.nsmallest(3,portfolio,key= lambda x:x[0])
print(a)