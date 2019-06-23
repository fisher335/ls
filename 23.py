# coding:utf-8

import os
from pathlib import Path

a = Path('.')
li = []
for i in a.rglob("*/*"):
    print(i.absolute())
    if i.is_file():
        li.append(i.absolute())

print(len(li))
