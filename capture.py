#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, os
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd

'''设置随机的UserAgent'''
ua = UserAgent()
headers1 = {'User-Agent': 'ua.ramdom'}


def open_url(district='xianghe', page="1"):  # 分析详细url获取所需信息
    """拿到url，获取url中的房价信息"""
    url = 'https://bj.lianjia.com/ershoufang/{}/pg{}/'.format(district, int(page))
    res = requests.get(url, 'lxml', headers=headers1)
    if res.status_code == 200:
        info = []
        soup = BeautifulSoup(res.content, 'lxml')
        for i in soup.find_all('div', {"class": "info clear"}):
            # print(i)
            info_one = BeautifulSoup(str(i), 'lxml')

            house_info = info_one.find("div", {"class": "houseInfo"})
            print(house_info.text)
            content = house_info.text
            aa = content.split("/")
            print(aa)
            if "别墅" in aa[1]:
                print(aa[1])
                del (aa[1])
            if "车位" in aa[1]:
                continue
            if len(aa) == 5:
                aa.append("")
            # print(aa)

            positionInfo = info_one.find("div", {"class": "positionInfo"})
            print(house_info.text)
            content = positionInfo.text
            bb = content.split("/")
            # print(bb)

            totalPrice = info_one.find("div", {"class": "totalPrice"})
            # print('总价' + totalPrice.span.text)
            unitPrice = info_one.find("div", {"class": "unitPrice"})
            # print('单价' + unitPrice.span.text)

            result = list(aa) + list(bb)
            result.append(totalPrice.span.text)
            result.append(unitPrice.span.text)
            result.append("page" + str(page))
            result.append(district)
            print(result)
            info.append(result)
        return info


def getData(district):
    """抓取页面数，超过100页后限制在100页，因为100页以后的数据是重复数据"""
    url = 'https://bj.lianjia.com/ershoufang/{}'.format(district)
    res = requests.get(url, 'lxml', headers=headers1)
    soup = BeautifulSoup(res.content, 'lxml')
    a = soup.find('h2', {"class": "total fl"})
    record = str(a.text).split(" ")[1]
    page = int(int(record) / 30) + 1
    print(page)
    if page > 100:  # 因为只提供100页的数据，后面的数据是重复的，没有意义，所以只抓100页
        page = 100
    ls_result = []
    for i in range(1, page + 1):
        ls_tmp = open_url(district, i)
        ls_result.extend(ls_tmp)
    return ls_result


def pandas_to_xlsx(name, info):  # 储存到xlsx
    pd_book = pd.DataFrame(info)
    pd_book.to_excel('链家二手房{}.xlsx'.format(name), sheet_name='链家二手房')


def writer_to_json(name, list_data):
    with open('链家二手房{}.txt'.format(name), 'a+')as f:
        data = json.dumps(list_data)
        f.write(data)


if __name__ == '__main__':
    """链家的网站只能抓取100页，为了获取尽可能多的数据，所以分区抓取，每个区能抓取100页"""
    district = ['dongcheng', 'xicheng', 'chaoyang', 'haidian', 'fengtai', 'shijingshan', 'tongzhou', 'changping',
                'daxing', 'yizhuangkaifaqu', 'shunyi', 'fangshan', 'mentougou', 'pinggu', 'huairou', 'miyun', 'yanqing']
    for name in district:
        result = getData(name)
        writer_to_json(name, result)
        pandas_to_xlsx(name, result)
