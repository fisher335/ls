#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import socket
import requests
import json
import time

FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(filename='1.log', level=logging.INFO, format=FORMAT)
config = {
    "ID": 67944,  # 填写你自己的API Token ID
    "TokenID": "fd23a30bfdeb724436f44c71d0a7eae9",  # 填写你自己的API Token
    "domains": {
        "fengshaomin.com": ['home']  # 填写需要更新的域名及对应的记录
    },
    "delay": 10  # 检查时间
}

Action_DomainList = 'Domain.List'
Action_RecordList = 'Record.List'
Action_RecordModify = 'Record.Modify'

ip_cache = {
    'refresh_time': 0,
    'cached_ip': '0.0.0.0'
}


def get_local_ip():
    try:
        sock = socket.create_connection(address=('ns1.dnspod.net', 6666), timeout=10)
        ip = sock.recv(32)
        sock.close()
        return ip

    except Exception as e:
        logging.error("GetIP Error: %s", e)
        return None


def update_local_ip():
    ip = get_local_ip().decode()
    print(ip, ip_cache['cached_ip'], len(ip))
    if ip != ip_cache['cached_ip'] and len(ip) < 16:
        logging.info('本地IP有更新，准备更新到dns' + '本地ip：' + ip + '上次IP：' + ip_cache['cached_ip'])
        ip_cache['cached_ip'] = ip
        ip_cache['refresh_time'] = time.time()
        return True
    else:
        return False


class DnsPod():
    base_uri = 'https://dnsapi.cn'
    user_agent = 'DDNSPOD Update Agent/0.0.1 (fengshaomina@gmail.com)'
    format = 'json'
    lang = 'cn'
    success_code = ["1"]

    def invoke(self, action, post_data=None):
        uri = self.base_uri + '/' + action
        if post_data is None:
            post_data = dict()
        else:
            assert isinstance(post_data, dict)
        headers = {
            'Host': 'dnsapi.cn',
            'User-Agent': self.user_agent,
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/json",
        }
        post_data['login_token'] = str(config['ID']) + ',' + config['TokenID']
        post_data['format'] = self.format
        r = requests.post(url=uri, data=post_data, headers=headers)
        return json.loads(r.text, encoding='utf-8')

    def __init__(self, with_config):
        self.config = with_config

    def get_domains(self):
        ret = self.invoke(Action_DomainList)
        assert ret['status']['code'] in self.success_code
        if len(ret['domains']) > 0:
            return ret['domains']
        result = list()
        for domain in ret['domains']:
            if domain['name'] in config['domains']:
                result.append(domain)

    def get_records(self, domain_id):
        ret = self.invoke(Action_RecordList, {'domain_id': domain_id})
        assert ret['status']['code'] in self.success_code
        if len(ret['records']) > 0:
            return ret['records']
        else:
            return None

    def update_record(self, domain_id, record_id, record_name, new_ip=None):
        if new_ip is None:
            new_ip = ip_cache['cached_ip']
        ret = self.invoke(Action_RecordModify, {
            'domain_id': domain_id,
            'record_id': record_id,
            'value': new_ip,
            'record_type': 'A',
            'record_line': '默认',
            'sub_domain': record_name,
        })

        print(ret)
        logging.info(ret)
        assert ret['status']['code'] in self.success_code


if __name__ == '__main__':
    while True:
        try:
            if update_local_ip():
                x = DnsPod(config)
                for domain in x.get_domains():
                    records = x.get_records(domain_id=int(domain['id']))
                    for record in records:
                        if record['name'] in config['domains'][domain['name']]:
                            logging.info(record)
                            x.update_record(domain['id'], record['id'], record['name'])
            else:
                logging.info("----IP地址没有变化，暂不更新-----")
            time.sleep(config['delay'] * 60)
        except Exception as e:
            logging.info("-------------------本次更新异常------------------", e.args)
            continue
