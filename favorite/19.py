# -*- coding: utf-8 -*-
# @Date    : '2018/6/6 0006'
# @Author  : Terry feng  (fengshaomin@qq.com)
from fake_useragent import UserAgent

ua = UserAgent()


def print_random(x: int) -> str:
    for i in range(x):
        print(ua.random)
        print(ua.random)
    return "time"


if __name__ == '__main__':
    name = print_random(10)
