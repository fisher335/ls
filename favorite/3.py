# coding:gbk
import heapq

import jieba.analyse
from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator


def sortd(x):
    return x[1]


lyric = ''
f = open('./1.txt', 'r', encoding='utf-8')
# for i in f:
#   # lyric+=f.readline()

result = jieba.analyse.textrank(f.read(), topK=50, withWeight=True)
print(result)
keywords = dict()
for i in result:
    keywords[i[0]] = i[1]
# print(keywords)

print(keywords)

c = heapq.nlargest(10, result, key=sortd)
print(c)
