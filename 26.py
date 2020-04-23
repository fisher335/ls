# coding:utf-8
import os

path = r"D:\dev\projects\ls\favorite"
# 待搜索的名称
filename = "py"
result = []
for root, folder, files in os.walk(path):
    for file in files:
        if file.find(filename) >= 0:
            file_abspath = os.path.join(root, file)
            result.append(file_abspath)
for index, val in enumerate(result):
    print("序号{no}的值：{val}".format(no=index + 1, val=val))
