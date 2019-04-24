#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "charlene"
__time__ = "2019-04-23"

import networkx as nx
import json

with open('data/station_connect.json') as fp:
    station_connect = json.load(fp)

with open('data/distance_dict.json') as fp:
    distance_dict = json.load(fp)

with open('data/station_line.json') as fp:
    station_line = json.load(fp)

subway_network = nx.DiGraph(station_connect)


def is_goal(destination):
    def _wrap(path, by_way):
        return path[-1] == destination and all([b in path for b in by_way])

    return _wrap

def get_path_length(path):
    """
    计算路径总长度
    :param path:
    :return:
    """
    dist = 0
    for i in range(len(path) - 1):
        if path[i + 1] not in distance_dict[path[i]]:
            print('{}-{} not in distance_dict'.format(path[i], path[i + 1]))
        dist += distance_dict[path[i]][path[i + 1]]

    return dist


def get_nega_length(path):
    return -get_path_length(path)


def get_transfer_times(path):
    """
    计算一条路径中的换乘次数
    :param path:
    :return:
    """
    times = 0
    for i in range(1, len(path) - 1):

        if len(station_line[path[i]]) > 1 and \
                        len(set(station_line[path[i - 1]]).intersection(set(station_line[path[i + 1]]))) < 1:
            times += 1

    return times


def get_comprehensive(path):
    return get_path_length(path) + get_transfer_times(path)


def sort_path(compare_func, beam):
    def _sort(pathes):
        return sorted(pathes, key=compare_func)[:beam]

    return _sort


def search(graph, start, is_goal, search_strategy=lambda x: x, by_way=[]):
    pathes = [[start]]
    seen = set()

    while pathes:
        path = pathes.pop(0)
        frontier = path[-1]
        if path == ['望京西', '芍药居', '光熙门', '柳芳', '东直门', '东四十条', '朝阳门', '建国门', '东单', '王府井', '天安门东', '天安门西',
                    '西单']:  # , '复兴门', '南礼士路', '木樨地', '军事博物馆']:
            print(path)
        if frontier in seen:

            continue

        successors = graph[frontier]

        for station in successors:

            if station in path:
                continue

            new_path = path + [station]

            pathes.append(new_path)

            if is_goal(new_path, by_way):
                return new_path

        seen.add(frontier)  # TODO 地铁线路图是一个有环的图，而不是树，因此这种seen的定义方式，会导致有些路径遍历不到
        pathes = search_strategy(pathes)



# by_way
shortest_path = search(subway_network, "望京西", is_goal("八宝山"), search_strategy=sort_path(get_comprehensive, beam=1000))
print(shortest_path)
dist, transfer_times = get_path_length(shortest_path), get_transfer_times(shortest_path)
print("望京西 到 八宝山 最优方案全长 {} 千米，需换乘 {} 次".format(dist, transfer_times))