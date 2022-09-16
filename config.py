'''
Author: thund1r thuncoder@foxmail.com
Date: 2022-08-23 09:36:39
LastEditTime: 2022-09-16 16:14:18
Description: 配置函数

Copyright (c) 2022 by thund1r thuncoder@foxmail.com, All Rights Reserved. 
'''
# -*- coding: utf8 -*-
import os
SYS_CONFIG = {
    # 企业微信企业ID,必填
    "corpid": "",

    # 企业微信应用Secret,必填
    "corpsecret": "",

    # 企业微信AgentId,必填
    "agentid": "",

    # 和风天气Key，非必填
    "qweather": "",

    # 天气预报地址，非必填
    # 格式：省/市-市/县/区，多地址以&&分隔
    # 例如：四川-成都&&江苏-江宁
    "city": "",

    # 纪念日名称，非必填
    # 每年都有的日子，多日期以&&分隔
    # 例如：某某某的生日&&结婚纪念日
    "targetname": "",

    # 纪念日日期，非必填
    # 公历格式20XX-XX-XX，农历年份前加n
    # 多日期以&&分隔，注意与名称对应
    # 例如：n2020-08-11&&2021-08-26
    "targetday": "",

    # 单日项目名称，非必填
    # 只有某一年有的日子，多日期以&&分隔
    # 例如：跟XX在一起&&某某某出生
    "beginname": "",

    # 单日日期，非必填
    # 公历格式20XX-XX-XX，农历年份前加n
    # 多日期以&&分隔，注意与名称对应
    # 例如：n2020-08-11&&2021-08-26
    "beginday": "",

    # 图文类型，非必填
    # 1为单图文，2为多图文，默认单图文
    "msgtype": "",

    # 自定义头图链接，非必填
    # 务必以http:// 或 https:// 开头
    "pic": "",

    # 随机图片类型，非必填
    # 默认fengjing
    # 可选项meizi、dongman、fengjing、suiji、none
    # 分别是妹子、动漫、风景、随机、单图文不显示图片
    "pictype": "",

    # 自定义标题，非必填
    # 例如：今天的推送来啦！
    "title": "",

    # 自定义第一段内容，非必填
    # 例如：记得喝水水哦~
    "content": "",

    # 自定义称呼，非必填
    # 例如：宝贝~
    "call": "",

    # 需要疫情数据的城市名称，非必填
    # 只能是市级，多城市以&&分隔
    # 例如：成都&&南京
    "yqcity": "",

    # 天行数据APIKEY，非必填
    # 需要彩虹屁等数据时填写
    "tian": "",

    # 图文详情页链接，非必填
    # 完成教程 配置页面 后再填写
    # 腾讯云函数用户填写API网关触发网关网址
    # 服务器用户请自行搭建Diary，填写已备案域名:端口号/show
    # 务必以http:// 或 https:// 开头
    "link": ""
}


# 获取配置
def get(key: str):
    value = os.getenv(key.upper())
    if value is None:
        key = key.lower()
        value = os.getenv(key)
    if value is None and key in SYS_CONFIG:
        value = SYS_CONFIG[key]
    return value


# 获取配置列表化
def get_list(key: str):
    value = get(key)
    if value:
        value = list(filter(None, value.split("&&")))
    return value
