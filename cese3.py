#coding:utf-8
from client import DBUtil

conn = DBUtil.DBConn(host='192.168.0.14', user='root', passwd='ddc.2017', database='yunwei')

rows = [{'name': 'xiaoming', 'age': '12', 'gender': 'male'},
        {'name': 'xiaohong', 'age': '11', 'gender': 'female'}]
ret = conn.qj("select * from accounts_user")
print('ret:', ret)