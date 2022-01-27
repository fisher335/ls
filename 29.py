# coding:utf-8
import json

import requests

from client.MysqlClient import MySQLHelper
from config.database import database


def getinfo():
    with open("1.ini", "r", encoding="utf-8") as f:
        lines = f.readlines()
        re = []
        for i in range(len(lines)):
            # print("序号：%s   值：%s" % (i + 1, lines[i]))
            s = lines[i]
            if 'uid' in s:
                li = []
                for j in range(22):
                    a = lines[i + j].split(".", 3)[3]
                    li.append(a)
                re.append(li)
        print(re)
        info = sorted(re, key=lambda user: user[1])
        return info


def changeli(li):
    d = dict()
    for i in li:
        i = i.replace('''\n''', "")
        s = i.split("=")
        d[s[0]] = s[1]
    return d


def getlidic(li):
    l = []
    for i in li:
        d = changeli(i)
        l.append(d)
    return l


def getloginname(card):
    client = MySQLHelper(database["url"], database["port"],
                         database["user"], database["password"], database["database_name"])
    if card != "":
        loginname = client.fetch_one("select UserNote from 04_User where card = {}".format(card.zfill(6)))
        # print(card+"card------------------------{}",loginname)
        return loginname['UserNote']


def sendMessage(dict):
    f = ''' {"SanpPic":"data:image/jpeg;base64,Qk225QArx","operator":"VerifyPush","info":{"Nation":1,"VerifyStatus":1,"Temperature":36.3,"Address":"北京","VerfyType":513,"PersonType":0,"Birthday":"2021-10-22","Gender":0,"TemperatureMode":0,"Direction":0,"Name":"吕建1","Native":"1","ValidBegin":"0000-00-00T00:00:00","PersonID":820,"Tempvalid":0,"CardType":0,"OpendoorWay":2,"IdCard":"1.10106198532642E+17","Notes":"lvjian1","TemperatureAlarm":0,"PushType":1,"MjCardNo":761,"DeviceID":1737267,"CreateTime":"2022-01-07T08:22:29","Sendintime":1,"Similarity2":0.000000,"Similarity1":85.003731,"Telnum":"13800138000","MjCardFrom":"2","isNoMask":0,"PersonUUID":"E520A591D667E0EE","CustomizeID":376791,"ValidEnd":"0000-00-00T00:00:00"}}
'''
    d = json.loads(f)
    # print(dict)
    login = getloginname(str(dict['MjCardNo']))
    d['info']['Notes'] = str(login)
    d['info']['CreateTime'] = dict['utime'].replace("/", "T")
    d['info']['Name'] = dict['uname']
    print(d)
    if d['info']['Name'] !='周港娜':
        j = json.dumps(d)
        headers = {'Content-Type': 'application/raw'}
        r = requests.post('http://open.cese3.com/Subscribe/Verify',data = j,headers = headers)
        print(j)
        # r = requests.post('http://192.168.0.16:9000/Subscribe/Verify', json=j)
        # print(r.content)


if __name__ == '__main__':
    li = getinfo()
    result = getlidic(li)
    for i in result:
        sendMessage(i)
        # print(i)
