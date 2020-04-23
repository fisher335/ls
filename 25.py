# coding:utf-8
import os

for row in range(1, 10):
    for col in range(1, row + 1):
        print('{}*{}={}'.format(col, row, col * row), end='\t')
    print("")


name = "20201231"
print(name.find("3020"))