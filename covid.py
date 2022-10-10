'''
Author: Thund1r thund1r@foxmail.com
Date: 2022-09-22 14:31:16
LastEditTime: 2022-10-08 22:12:16
Description: 疫情数据

Copyright (c) 2022 by Thund1r thund1r@foxmail.com, All Rights Reserved. 
'''
# -*- coding: utf8 -*-
import config
import requests


yqcity_list = config.get_list("yqcity")


# 获取城市疫情数据
def get_yq(city_name):
    try:
        res = requests.get(
            f'https://covid.myquark.cn/quark/covid/data/index_data?format=json&method=Huoshenshan.ncov2022&city={city_name}').json()['data']
        if len(res['cityData']) == 0:
            res['cityData'] = res['provinceData']
        yq_res_list = [
            {"desc": "🤒 新增确诊/无症状",
                "detail": str(res['cityData']["sure_new_loc"])+"/" + str(res['cityData']["sure_new_hid"])},
            {"desc": "😷 现有确诊",
                "detail": res['cityData']["present"]},
            {"desc": "⛔️ 中/高风险区",
                "detail": str(res['cityData']["danger"]["1"]) + "/" + str(res['cityData']["danger"]["2"])}
        ]
        yq_tip_list = []
        yq_tip_list.append(f'🏥 {city_name}疫情（{(res["time"][4:])}）')
        for item in yq_res_list:
            yq_tip_list.append(item['desc'] + "：" + str(item['detail']))
        yq_tip = '\n'.join(yq_tip_list)
        return yq_tip
    except Exception as e:
        print("获取疫情数据错误：", e)
        return None


# 获取所有疫情数据
def get_map_yq():
    if yqcity_list:
        map_yq_tip = None
        yq_list = list(map(get_yq, yqcity_list))
        yq_list = list(filter(None, yq_list))
        if yq_list:
            map_yq_tip = "\n".join(yq_list)
        return map_yq_tip
    else:
        print("没有填写疫情数据城市")
        return None
