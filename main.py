# -*- coding: utf-8 -*-
import pandas as pd
import json
import matplotlib.pyplot as plt


def getData(filename="二手房.txt"):
    with open(filename, 'r')  as f:
        result = json.loads(f.read())

    return result


def getpadata():
    data = getData("二手房.txt")

    df = pd.DataFrame(data,
                      columns=['地址', '户型', '大小', '朝向', '装修', '电梯', '楼层', '建筑方式', '片区', '总价', '单价', '原始页', '区县', "大小户型",
                               '求平均值'])
    da = df.loc[:, ['大小户型', '区县', '求平均值']]
    return da


def getTocal(da):
    d1 = da.groupby(['大小户型', '区县']).mean()
    format = lambda x: round(x, 2)
    d1 = d1["求平均值"].map(format)
    d1.to_excel('户型分布.xlsx', sheet_name='链家二手房')
    return d1


def gefGetBig(da):
    dt = da[da['大小户型'].isin(["大户型"])]
    d1 = dt.groupby('区县').mean()
    format = lambda x: round(x, 2)
    d1 = d1["求平均值"].map(format)
    d1 = d1.sort_values(ascending=False)
    d1.to_excel('大户型.xlsx', sheet_name='链家二手房')
    return d1


def getSmall(da):
    dt = da[da['大小户型'].isin(["小户型"])]
    d1 = dt.groupby('区县').mean()
    format = lambda x: round(x, 2)
    d1 = d1["求平均值"].map(format)
    d1 = d1.sort_values(ascending=False)
    d1.to_excel('小户型.xlsx', sheet_name='链家二手房')
    return d1


def showDaHuXing():
    '''画出大户型的直方图'''
    da = getpadata()
    a = gefGetBig(da)
    a.plot(kind='bar')
    plt.show()


def showXiaoHuXing():
    '''画出小户型的直方图'''
    da = getpadata()
    b = getSmall(da)
    b.plot(kind='bar')
    plt.show()


if __name__ == '__main__':
    showDaHuXing()
    # showXiaoHuXing()
