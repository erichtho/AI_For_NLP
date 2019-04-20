#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "charlene"
__time__ = "2019-04-19"

import re
import requests
from bs4 import BeautifulSoup


class SubwayLine():
    def __init__(self, soup):
        self.soup = soup
        self.stations, self.station_distaneces, self.bidirections = SubwayLine.parse_station_distance(soup)

    @staticmethod
    def parse_station_distance(soup):
        distance_table = []
        time_table = []
        for caption in soup.find_all('caption'):
            if caption.string is not None and re.match('[\w（）]+相邻站间距信息统计表', caption.string):
                distance_table.append(caption.parent)
            if caption.string is not None and re.match('[\w（）、]+首末车时刻表', caption.string):
                time_table = []

        stations = []
        distances = {}
        bidirections = {}
        s = None
        for dtable in distance_table:
            # print("Error in parse {}'s station distance, cannot find table 相邻站间距信息统计表".format(soup.))

            for tr in dtable.select('tr'):
                t = tr.contents
                if len(t) != 3:
                    print('Warning: tr has unexpected numbers of children:{}'.format(tr))
                    continue
                if not re.match('[\d|.]\w*', t[1].string):
                    continue
                s = next(t[0].strings)
                # print("s in loop:{}".format(s))
                stations.append(s.split('——')[0])
                distances[s] = float(t[1].string[:-2]) * 1000 if '千米' in t[1].string else float(t[1].string[:-1])
                bidirections[s] = t[1].string

        # s = next(tr.contents[0].strings)
        # if s is None:
        #     print("out of loop is None")
        # print(s.split('——'))
        stations.append(s.split('——')[1])
        return stations, distances, bidirections

headers_strs = """
Connection: keep-alive
Cache-Control: no-cache
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: BAIDUID=343548C5C045A1498BAA1D382DC6D1CC:FG=1; BIDUPSID=343548C5C045A1498BAA1D382DC6D1CC; PSTM=1501732771; MCITY=-75%3A; pgv_pvi=9675362304; BDUSS=JDS3V-U0h2bUE4ckFFZjhreDhlUXN-fmlBRERuVWd-RFA0QWtyYTdYVUFMTjFjRVFBQUFBJCQAAAAAAAAAAAEAAAAlaCBMb2xkaXJvbnNpZGUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACftVwAn7VcS3; pgv_si=s5658319872; H_PS_PSSID=28884_1440_28777_21086_28722_28558_28831_28585_26350_20718; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1555495877,1555498044,1555498060,1555546970; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1555546970
""".split('\n')
headers = dict([(pair[:pair.find(':')], pair[pair.find(':')+1:].strip()) for pair in headers_strs if pair.strip()])

start_url = "https://baike.baidu.com/item/北京地铁/408485"
start_content = requests.get(start_url, allow_redirects=False, headers=headers)
start_content.encoding = 'utf-8'
start_soup = BeautifulSoup(start_content.text)
start_table = start_soup.find('caption',text='北京地铁开通简表').parent
all_subway_url = dict([(a.string, 'https://baike.baidu.com'+a.attrs['href']) for a in start_table.select('a')])

subways = {}
for subway_name,subway_url in all_subway_url.items():
    current_response = requests.get(subway_url, headers=headers)
    current_response.encoding = 'utf-8'
    subways[subway_name] = SubwayLine(BeautifulSoup(current_response.text))

# current_response = requests.get(all_subway_url['北京地铁4号线'], headers=headers)
# current_response.encoding = 'utf-8'
# subways['北京地铁4号线'] = SubwayLine(BeautifulSoup(current_response.text))