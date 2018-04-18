#!/usr/bin/env python

import requests
from pyquery import PyQuery as pq
import json


def get_stories(url):
    URL = url
    res = requests.get(URL)
    dom = pq(res.text)
    tag_list = dom('script')

    def tag2title(tag):
        script = tag.text_content()
        if script and 'TVEpisode' in script:
            jdata = json.loads(script)
            episode_number = jdata.get('episodeNumber')
            title = jdata.get('name')

            if episode_number and title:
                return (episode_number, title)

        return None

    episodes = [x for x in map(tag2title, tag_list) if x]
    return episodes
            



def main():
    products = [
        ('デビルズライン', 'https://anime.dmkt-sp.jp/animestore/ci_pc?workId=22080'),
        ('銀河英雄伝説 Die Neue These', 'https://anime.dmkt-sp.jp/animestore/ci_pc?workId=22082'),
        ('レイトン ミステリー探偵社 ～カトリーのナゾトキファイル～', 'https://anime.dmkt-sp.jp/animestore/ci_pc?workId=22119'),
    ]

    for p in products:
        avail = get_stories(p[1])
        print(p[0], avail)


if __name__ == '__main__': main()
    
