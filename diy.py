'''
Author: Thund1r thund1r@foxmail.com
Date: 2022-09-22 14:18:12
LastEditTime: 2022-09-29 09:34:31
Description: 自定义数据

Copyright (c) 2022 by Thund1r thund1r@foxmail.com, All Rights Reserved. 
'''
# -*- coding: utf8 -*-
import config
import days
import api
import requests
import random

title = config.get("title")
content = config.get("content")
pic = config.get("pic")


# 获取标题数据
def get_my_title():
    my_title = title
    if my_title:
        return my_title
    else:
        # 需要通过接口获取动态内容时，请替换下一行内容
        return None


# 获取自定义第一段内容数据
def get_my_content():
    content_list = []
    today_tip = days.get_today()["today_tip"]
    content_list.append(today_tip)
    my_content = content
    if my_content:
        content_list.append(my_content)
    chp_tip = api.get_chp()
    if chp_tip:
        content_list.append(chp_tip)
    # 加入其他数据作为第一段在这里接收
    return '\n'.join(content_list)


# 获取自定义头图数据
def get_my_pic():
    my_pic = pic
    if my_pic:
        return my_pic
    else:
        return None
