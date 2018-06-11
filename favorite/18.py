# -*- coding: utf-8 -*-
# @Date    : '2018/5/29 0029'
# @Author  : Terry feng  (fengshaomin@qq.com)
import os


def get_mac_addr():
    import uuid
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    return mac.upper()


if __name__ == '__main__':
    a = get_mac_addr()
    print(a)
