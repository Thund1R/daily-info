'''
Author: Thund1r thund1r@foxmail.com
Date: 2022-09-22 14:26:19
LastEditTime: 2022-09-27 11:51:07
Description: 日期数据

Copyright (c) 2022 by Thund1r thund1r@foxmail.com, All Rights Reserved. 
'''
# -*- coding: utf8 -*-
import config
from datetime import datetime, date, timedelta
from zhdate import ZhDate
import random

nowdatetime = (datetime.utcnow() + timedelta(hours=8))
targetday_list = config.get_list("targetday")
targetname_list = config.get_list("targetname")
beginday_list = config.get_list("beginday")
beginname_list = config.get_list("beginname")
call = config.get("call")


# 计算纪念日
def get_remain(target_day, target_name):
    ndt = nowdatetime
    today = date(ndt.year, ndt.month, ndt.day)
    this_year = datetime.now().year
    target_day_year = target_day.split("-")[0]
    if target_day_year[0] == "n":
        lunar_mouth = int(target_day.split("-")[1])
        lunar_day = int(target_day.split("-")[2])
        this_date = ZhDate(this_year, lunar_mouth,
                           lunar_day).to_datetime().date()
    else:
        solar_month = int(target_day.split("-")[1])
        solar_day = int(target_day.split("-")[2])
        this_date = date(this_year, solar_month, solar_day)
    if today == this_date:
        remain_day = 0
        remain_tip = f"🌟 {target_name}就是今天啦！"
    elif today > this_date:
        if target_day_year[0] == "n":
            lunar_next_date = ZhDate(
                (this_year + 1), lunar_mouth, lunar_day).to_datetime().date()
            next_date = date(
                (this_year + 1), lunar_next_date.month, lunar_next_date.day)
        else:
            next_date = date(
                (this_year + 1), solar_month, solar_day)
        remain_day = int(str(next_date.__sub__(today)).split(" ")[0])
        remain_tip = f"🗓️ 距离{target_name}还有 {remain_day} 天"
    else:
        next_date = this_date
        remain_day = int(str(next_date.__sub__(today)).split(" ")[0])
        remain_tip = f"🗓️ 距离{target_name}还有 {remain_day} 天"
    return (remain_tip, remain_day)


# 计算单日
def get_duration(begin_day, begin_name):
    ndt = nowdatetime
    today = date(ndt.year, ndt.month, ndt.day)
    begin_day_year = begin_day.split("-")[0]
    if begin_day_year[0] == "n":
        lunar_year = int(begin_day_year[1:])
        lunar_mouth = int(begin_day.split("-")[1])
        lunar_day = int(begin_day.split("-")[2])
        begin_date = ZhDate(lunar_year, lunar_mouth,
                            lunar_day).to_datetime().date()
    else:
        solar_year = int(begin_day.split("-")[0])
        solar_month = int(begin_day.split("-")[1])
        solar_day = int(begin_day.split("-")[2])
        begin_date = date(solar_year, solar_month, solar_day)
    if today == begin_date:
        duration_day = 0
        duration_tip = f"🌟 {begin_name}就是今天啦！"
    elif today > begin_date:
        duration_day = int(str(today.__sub__(begin_date)).split(" ")[0])
        duration_tip = f"🗓️ {begin_name}已经 {duration_day} 天"
    else:
        duration_day = int(str(begin_date.__sub__(today)).split(" ")[0])
        duration_tip = f"🗓️ 距离{begin_name}还有 {duration_day} 天"
    return (duration_tip, duration_day)


# 获取第一个元素
def get_elemzero(elem):
    return elem[0]


# 获取第二个元素
def get_elemone(elem):
    return elem[1]


# 获取所有日期提醒数据
def get_map_days():
    days_list = []
    days_tip = ""
    target_res = ""
    if targetday_list or targetname_list:
        if len(targetday_list) == len(targetname_list):
            try:
                target_res = list(
                    map(get_remain, targetday_list, targetname_list))
                days_list.extend(target_res)
            except Exception as e:
                print("获取纪念日数据错误，请检查纪念日targetname与targetday填写是否正确", e)
                return None
        else:
            print("获取纪念日数据错误，请检查纪念日targetname与targetday数量是否相等")
    else:
        print("未配置纪念日")
    begin_res = ""
    if beginday_list or beginname_list:
        if len(beginday_list) == len(beginname_list):
            try:
                begin_res = list(
                    map(get_duration, beginday_list, beginname_list))
                days_list.extend(begin_res)
            except Exception as e:
                print("获取单日数据错误，请检查单日beginname与beginday填写是否正确", e)
                return None
        else:
            print("获取单日数据错误，检查单日beginname与beginday数量是否相等")
    else:
        print("未配置单日")
    days_list = list(filter(None, days_list))
    if days_list:
        days_list.sort(key=get_elemone)
        res = list(map(get_elemzero, days_list))
        days_tip = "\n".join(res)
    return days_tip

# 获取今天
def get_today():
    ndt = nowdatetime
    d = ndt.strftime("%Y{y}%m{m}%d{d}").format(y='年', m='月', d='日')
    w = int(ndt.strftime("%w"))
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    today_date = f"{d} {week_list[w]} "
    now_time = ndt.strftime("%H:%M:%S")
    time_tip = ""
    if "00:00:00" <= now_time < "06:00:00":
        time_tip = "凌晨好"
    elif "06:00:00" <= now_time < "09:00:00":
        time_tip = "早上好"
    elif "09:00:00" <= now_time < "12:00:00":
        time_tip = "上午好"
    elif "12:00:00" <= now_time < "13:00:00":
        time_tip = "中午好"
    elif "13:00:00" <= now_time < "18:00:00":
        time_tip = "下午好"
    elif "18:00:00" <= now_time < "23:59:59":
        time_tip = "晚上好"
    time_tip = f"{time_tip} ~ {get_emoticon()}"
    today_tip = call + time_tip if call else time_tip
    return {
        "today_date": today_date,
        "today_tip": today_tip
    }


# 获取随机颜文字
def get_emoticon():
    emoticon_list = ["(￣▽￣)~*", "(～￣▽￣)～", "︿(￣︶￣)︿", "~(￣▽￣)~*", "(oﾟ▽ﾟ)o", "ヾ(✿ﾟ▽ﾟ)ノ", "٩(๑❛ᴗ❛๑)۶", "ヾ(◍°∇°◍)ﾉﾞ", "ヾ(๑╹◡╹)ﾉ", "(๑´ㅂ`๑)", "(*´ﾟ∀ﾟ｀)ﾉ", "(´▽`)ﾉ", "ヾ(●´∀｀●)",
                     "(｡◕ˇ∀ˇ◕)", "(≖ᴗ≖)✧", "(◕ᴗ◕✿)", "(❁´◡`❁)*✲ﾟ*", "(๑¯∀¯๑)", "(*´・ｖ・)", "(づ｡◕ᴗᴗ◕｡)づ", "o(*￣▽￣*)o", "(｀・ω・´)", "( • ̀ω•́ )✧", "ヾ(=･ω･=)o", "(￣３￣)a", "(灬°ω°灬)", "ヾ(•ω•`。)", "｡◕ᴗ◕｡"]
    return random.choice(emoticon_list)
