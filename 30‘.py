# coding:utf-8
import json
import requests
from requests import Session
def package():
    s = Session()
    base_url = "https://chenzhuwang.cdjox.com:4433"
    api_url = "/api/v1/B3C2402D8B187BBA1BCA7294AA604F9C/login"
    data = {"username": "18349199865", "password": "199865", "code": "5224", "type": 1, "id": "6QM2o9TuDtFfUZOcyjb4",
            "platform": "backend"}
    # 模拟登陆，获取session连接，但是貌似没有用session
    a = s.post(base_url + api_url, data=json.dumps(data))
    print('-----------------',a.content)
    # 获取工种接口
    work_type_list = "/api/v1/projectworktypes/alllist"
    token = a.json()["token"]
    print(token)
    headers = {}
    headers["token"] = token
    b = s.get(base_url + work_type_list, headers=headers)
    print(b.content)
    person_list = "/api/v1/projectusers/list"
    params = {"pid": "1534", "manager": 1, "pagesize": 100, "page": 1}
    c = s.get(base_url + person_list, params=params, headers=headers)
    print(c.json())
    face_list = "/api/v1/faceinoutrecords/list"
    params_face = {"pid": "1534", "pagesize": 100, "page": 1, "start": None, "end": None}
    d = s.get(base_url + face_list, headers=headers, params=params_face)
    print(d.content)
if __name__ == '__main__':
    package()