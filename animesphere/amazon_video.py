#!/usr/bin/env python

import requests
import re
from pyquery import PyQuery as pq


def get_stories(code):
    URL = 'https://www.amazon.co.jp/gp/video/detail/{}'.format(code)
    res = requests.get(URL)
    dom = pq(res.text)
    div_list = dom('div.dv-el-title-data div.dv-el-title')

    titles = [re.sub('\s*(\d+.*)\s*', '\\1', x.text_content(),
                     flags=(re.MULTILINE))
              for x in div_list]
    index_titles = [t.split('. ') for t in titles]
    return [(int(x), y, None) for x, y in index_titles]


def main():
    products = [
        ('銀河英雄伝説 Die Neue These', 'B07BZB7MQ8'),
        ('魔法少女 俺', 'B07BX47VFQ'),
        ('メガロボクス', 'B07BYR6GG5'),
        ('魔法少女サイト', 'B07BYXFS97'),
        ('多田くんは恋をしない', 'B07C2N8ZCJ'),
        ('Caligula -カリギュラ-', 'B07BYV666J'),
        ('かくりよの宿飯', 'B07BZK6ZYB'),
        ('こみっくがーるず', 'B07BZ6X524'),
        ('あまんちゅ！ シーズン2', 'B07CF731RW'),
        ('ラストピリオド ―終わりなき螺旋の物語―', 'B07C2KRBL3'),
        ('若おかみは小学生！', 'B07C3BC5L6'),
    ]
    # code = 'B07C3B58P2'

    for p in products:
        avail = get_stories(p[1])
        print(p[0], avail)


if __name__ == '__main__': main()
    
