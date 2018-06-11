# -*- coding: utf-8 -*-
# @Date    : '2018/6/6 0006'
# @Author  : Terry feng  (fengshaomin@qq.com)
from concurrent.futures import ProcessPoolExecutor
import time


def p(count):
    print(count)
    if count % 2 ==0:
        time.sleep(5)
    else:
        time.sleep(2)


if __name__ == '__main__':
    with ProcessPoolExecutor(2) as task:
        task.map(p,[1,2,3,4,5,6,7,8,9])
