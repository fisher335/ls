#coding:utf-8
import os
import socket
import logging



def getip():
    try:
        sock = socket.create_connection(address=('ns1.dnspod.net', 6666), timeout=10)
        ip = sock.recv(32)
        sock.close()
        return ip
    except Exception as e:
        logging.info("GetIP Error: %s", e)
        return None

if __name__ == '__main__':
    getip()
