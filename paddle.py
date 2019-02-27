# coding：utf-8
# coding:utf-8
import string
import time
import pandas as pd
import requests


def get_comment(url):
    b = requests.get(url, auth=("fengshaomin@qq.com", "shaomina1984"))
    if b == "":
        return ""
    else:
        return url


def get_label(list_lable):
    result = ""
    if len(list_lable) != 0:
        for i in list_lable:
            result = result + ("," + i["name"])
    return result


def get_assignees(li):
    result = ""
    if len(li) != 0:
        for i in li:
            result = result + ("," + i["login"])
    return result


page_num = 1
cnt = 0
r = []
flag = True
result = []
while flag:

    url = "https://api.github.com/repos/PaddlePaddle/Paddle/issues?state=open&page={pn}&per_page=20".format(pn=page_num)
    print(url)
    a = requests.get(url, auth=('fengshaomin@qq.com', 'shaomina1984'))
    time.sleep(3)
    if len(a.json())==0:

        flag = False
        break
    else:
        d = a.json()
        page_num += 1

        for i in d:

            row = []
            print(i)
            if "pull" in str(i["html_url"]):
                continue
            else:
                row.append(i["number"])
                row.append(i["title"])
                row.append(i["body"])
                row.append(get_label(i["labels"]))
                row.append(i["user"]["login"])
                if i["assignee"] is not None:
                    row.append(i["assignee"].get("login", ""))
                else:
                    row.append("")
                row.append(get_assignees(i["assignees"]))

                # row.append(i["comments_url"])
                row.append(i["created_at"])
                row.append(i["updated_at"])
                row.append(i["html_url"])
                row.append(i["state"])
                result.append(row)
print(result)

pd_book = pd.DataFrame(result)
pd_book.columns = ["issue_id","title","body","labels","user","assignee","assignees","created_at","updated_at","issue_url","state"]
pd_book.to_excel('issues_Paddle.xlsx', sheet_name='Paddle')
