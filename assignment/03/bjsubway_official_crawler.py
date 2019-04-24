#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "charlene"
__time__ = "2019-04-20"

import re
import requests
from bs4 import BeautifulSoup, element
import json

"""
北京地铁官方网站爬虫
"""

distance_url = 'http://www.bjsubway.com/station/zjgls/'
time_url = ''

distance_html = requests.get(distance_url)
# distance_html.encoding = 'gb2312'
# distance_soup = BeautifulSoup(distance_html.text)  # text只包含一个line_place, 不可
# distance_html.content.decode("utf8","ignore").encode("gbk","ignore")
distance_soup = BeautifulSoup(distance_html.content.decode('gb2312'), 'html5lib')

station_connect = {} # 站点的相邻站点
distance_dict = {} # 站点间距
station_line = {} # 途经站点的线路

def station_info_fill(subway_line, stations, dis):
    if stations[0] not in station_connect:
        station_connect[stations[0]] = set([stations[1]])
    else:
        station_connect[stations[0]].add(stations[1])

    if stations[0] in distance_dict:
        distance_dict[stations[0]][stations[1]] = float(dis)
    else:
        distance_dict[stations[0]] = {stations[1]:float(dis)}

    if stations[0] in station_line:
        station_line[stations[0]].add(subway_line)
    else:
        station_line[stations[0]] = set([subway_line])

for line in distance_soup.find_all('div', class_='line_place'):
    table_heads = line.find_all('thead')
    for table_head in table_heads:
        current_line = table_head.find('tr').find('td').\
             string.replace('相邻站间距信息统计表', '')
        tbody = table_head.next_sibling
        while type(tbody)!=element.Tag:
            tbody = tbody.next_sibling
        for station_pair in tbody.find_all('tr'):
            td = station_pair.find_all('td')
            s = station_pair.find('th').string.split('――')
            if '上行' in td[1].string:
                station_info_fill(current_line, s, td[0].string)

            if '下行' in td[1].string:
                station_info_fill(current_line, [s[1],s[0]], td[0].string)


with open('data/station_connect.json', 'w') as fp:
    json.dump(dict(map(lambda p: (p[0],list(p[1])), station_connect.items())), fp)

with open('data/distance_dict.json', 'w') as fp:
    json.dump(distance_dict, fp)

with open('data/station_line.json', 'w') as fp:
    json.dump(dict(map(lambda p: (p[0],list(p[1])), station_line.items())), fp)