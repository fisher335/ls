# -*- coding: utf-8 -*-
import json
import pandas as pd


def getData():
    result = []

    district = ['dongcheng', 'xicheng', 'chaoyang', 'haidian', 'fengtai', 'shijingshan', 'tongzhou', 'changping',
                'daxing', 'yizhuangkaifaqu', 'shunyi', 'fangshan', 'mentougou', 'pinggu', 'huairou', 'miyun', 'yanqing']

    for i in district:
        with open('分区数据/链家二手房{}.txt'.format(i), 'r') as f:
            l = json.loads(f.read())
            result.extend(l)

    print(len(result))
    return result


#

def getArea(pingmishu):
    l = pingmishu.find("平米")

    nu = pingmishu[0:l]

    num = float(nu)

    if num > 90:
        return '大户型'
    else:
        return '小户型'


def saveResult(name, li):
    pd_book = pd.DataFrame(li)
    pd_book.to_excel('{}.xlsx'.format(name), sheet_name='链家二手房')

    with open('{}.txt'.format(name), 'a+')as f:
        data = json.dumps(li)
        f.write(data)


def addArea(li):
    lt = []
    for i in li:
        if i[1] == '车位':#去掉卖车位的
            continue
        a = getArea(i[2])
        i.append(a)
        i.append(float(i[9]))
        lt.append(i)
    return lt


if __name__ == '__main__':
    # print(int(62.75))
    # print(getArea('62.75平米'))

    a = getData()
    b = addArea(a)
    saveResult("二手房", b)
