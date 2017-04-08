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
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
                            AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Accept": "text/html,application/xhtml+xml,\
                        application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        self.site_url = 'http://www.zimuku.net'
        self.search_url = 'http://www.zimuku.net/search?ad=1&q='
        self.ch_num_dict = {'1': '一', '2': '二', '3': '三',
                            '4': '四', '5': '五', '6': '六',
                            '7': '七', '8': '八', '9': '九',
                            '10': '十', '11': '十一', '12': '十二',
                            '13': '十三', '14': '十四', '15': '十五',
                            '16': '十六', '17': '十八', '19': '十九'}

    def __extract_chinese(self, string):
        ch_pattern = '[\u4e00-\u9fa5]+.*[\u4e00-\u9fa5]+'
        ch_res = re.search(ch_pattern, string)
        if ch_res:
            ch_str = ch_res.group(0)
            return ch_str
        else:
            return ''

    def get_subtitles(self, keywords, sub_num=5):

        #print('├ Searching...', end='\r')

        name = ''
        for one in keywords:
            name += (one + ' ')
        info_dict = guessit(name)
        keyword = info_dict['title']
        if info_dict.get('type') == 'episode':
            season_ch = '第{0}季'
            season_ch = season_ch.format(self.ch_num_dict[str(info_dict['season'])])
            sea_epi = 's{0}e{1}'
            sea_epi = sea_epi.format(str(info_dict['season']).zfill(2),
                                    str(info_dict['episode']).zfill(2))
            v_foramt = info_dict.get('format')  # todo
        else:
            season_ch = ''
            sea_epi = ''
            v_foramt = None

        sub_dict = order_dict()
        s = requests.session()
        r = s.get(self.search_url + keyword, headers=self.headers)
        bs_obj = BeautifulSoup(r.text, 'html.parser')

        if '共 0 条记录' in bs_obj.find('div', {'class': 'pagination'}).text:
            return sub_dict
        box = bs_obj.find('div', {'class': 'box'})
        res_boxes = []
        for one in box.find_all('div', {'class': 'item'}):
            if season_ch:  # 搜索的是剧集
                title_a = one.find('div', {'class': 'title'}).p.a
                if season_ch in title_a.text:
                    res_boxes.append(self.site_url + title_a.attrs['href'])
                    break
            else:  # 搜索的是电影
                title_a = one.find('div', {'class': 'title'}).p.a
                res_boxes.append(self.site_url + title_a.attrs['href'])
        for one_page in res_boxes:
            r = s.get(one_page, headers=self.headers)
            bs_obj = BeautifulSoup(r.text, 'html.parser')
            for one_sub in bs_obj.find('tbody').find_all('tr'):
                sub_a = one_sub.find('a')
                if sea_epi:
                    sub_title = sub_a.attrs['title']
                    sub_title = sub_title.replace('(', ' ').replace(')', ' ')
                    sub_ch_title = self.__extract_chinese(sub_title)
                    sub_en_title = sub_title.replace(sub_ch_title, '')
                    type_score = 0
                    lan_box = one_sub.find('td', {'class': 'lang'})
                    for img in lan_box.find_all('img'):
                        type_score += ('English' in img.attrs['alt']) * 1
                        type_score += ('繁體' in img.attrs['alt']) * 2
                        type_score += ('简体' in img.attrs['alt']) * 4
                        type_score += ('双语' in img.attrs['alt']) * 8
                    if sea_epi in sub_en_title.lower():
                        sub_dict[sub_ch_title] = {
                            'lan': type_score,
                            'link': self.site_url + sub_a.attrs['href']
                        }
                else:  # 电影 TODO
                    pass

                if len(sub_dict) >= sub_num:
                    break

        print(sub_dict)





if __name__ == '__main__':
    from main import GetSubtitles
    keywords, info_dict = GetSubtitles('', 1, 2, 3, 4, 5).sort_keyword('the expanse s01e01')
    zimuku = ZimukuDownloader()
    zimuku.get_subtitles(keywords)










