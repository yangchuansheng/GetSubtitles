#!/usr/bin/python3
#coding: utf-8

import requests
import re
from collections import OrderedDict as order_dict
from bs4 import BeautifulSoup
from contextlib import closing
from progress_bar import ProgressBar
from guessit import guessit


""" Zimuku 字幕下载器
"""

class ZimukuDownloader(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)
                            AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Accept": "text/html,application/xhtml+xml,
                        application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        self.site_url = 'http://www.zimuku.net/'
        self.search_url = 'http://www.zimuku.net/search?ad=1&q='
        self.ch_num_dict = {'1': '一', '2': '二', '3': '三',
                            '4': '四', '5': '五', '6': '六',
                            '7': '七', '8': '八', '9': '九',
                            '10': '十', '11': '十一', '12': '十二',
                            '13': '十三', '14': '十四', '15': '十五',
                            '16': '十六', '17': '十八', '19': '十九'}

    def _del_chinese(string):
        ch_pattern = '[\u4e00-\u9fa5]+.*[\u4e00-\u9fa5]+'
        ch_res = re.search(ch_pattern, string)
        if ch_res:
            ch_str = ch_res.group(0)
            string = string.replace(ch_str, '')
        return string

    def get_subtitles(self, keywords, sub_num=5):

        print('├ Searching...', end='\r')

        keyword = ''
        for one in keywords:
            keyword += (one + ' ')
        info_dict = guessit(keyword)
        if info_dict.get('type') == 'episode':
            season = '第{0}季'.
                        foramt(str(self.ch_num_dict[info_dict['season']]))
        else:
            season = ''
