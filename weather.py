'''
Author: Thund1r thund1r@foxmail.com
Date: 2022-09-22 14:28:08
LastEditTime: 2022-09-22 15:16:43
Description: 天气数据

Copyright (c) 2022 by Thund1r thund1r@foxmail.com, All Rights Reserved. 
'''
# -*- coding: utf8 -*-
import requests
import config
import re

qweather = config.get("qweather")
wea_city_list = config.get_list("city")


# 获取和风天气数据
def get_weather(city_name):
    try:
        city_id = None
        weather_tip = None
        city = city_name.split("-")[0]
        county = city_name.split("-")[1]
        city_url = f"https://geoapi.qweather.com/v2/city/lookup?&adm={city}&key={qweather}&location={county}"
        city_json = requests.get(city_url).json()
        city_code = city_json["code"]
        if city_code.__eq__("200"):
            city_id = city_json["location"][0]["id"]
        else:
            print(
                f"没有找到{city_name}这个地方，请检查city值是否正确，格式是否为 省/市-市/区/县 ，例如 成都-双流&&江苏-江宁")
        if city_id:
            # 获取逐天天气预报，有很多天气类信息，可以根据自己需要进行获取和拼接
            # 具体请参考和风天气逐天天气预报开发文档https://dev.qweather.com/docs/api/weather/weather-daily-forecast/
            weather_url = f"https://devapi.qweather.com/v7/weather/3d?key={qweather}&location={city_id}"
            weather_json = requests.get(weather_url).json()
            weather_code = weather_json["code"]
            weather_list = []
            if weather_code.__eq__("200"):
                temp = weather_json["daily"][0]
                textDay = temp["textDay"]
                tempMin = temp["tempMin"]
                tempMax = temp["tempMax"]
                weather_icon = get_weather_icon(textDay)
                weather_tip = weather_icon+" "+county+textDay+"，"+tempMin+"~"+tempMax+"℃"
                weather_list.append(weather_tip)
            # 获取穿衣指数。生活指数有很多信息，可以根据自己需要进行获取和拼接
            # 具体请参考和风天气生活指数开发文档https://dev.qweather.com/docs/api/indices/
            life_url = f"https://devapi.qweather.com/v7/indices/1d?type=3&location={city_id}&key={qweather}"
            life_json = requests.get(life_url).json()
            life_code = life_json["code"]
            if life_code.__eq__("200"):
                life_tip = "👔 " + life_json["daily"][0]["text"]
                weather_list.append(life_tip)
            # 需要和风天气其他接口的信息请参考以上代码格式进行获取和添加，所有开发文档https://dev.qweather.com/docs/api/

            weather_tip = '\n'.join(weather_list)
        else:
            print(
                f"获取{city_name}ID失败，请检查qweather、city值是否正确，city格式是否为 省/市-市/区/县 ，例如 四川-成都&&江苏-江宁")
        return weather_tip
    except Exception as e:
        print(f"获取{city_name}和风天气数据错误:", e)
        return None


# 获取天气icon
def get_weather_icon(text):
    weather_icon = "🌤️"
    weather_icon_list = ["☀️",  "☁️", "⛅️",
                         "☃️", "⛈️", "🏜️", "🏜️", "🌫️", "🌫️", "🌪️", "🌧️"]
    weather_type = ["晴", "阴", "云", "雪", "雷", "沙", "尘", "雾", "霾", "风", "雨"]
    for index, item in enumerate(weather_type):
        if re.search(item, text):
            weather_icon = weather_icon_list[index]
            break
    return weather_icon


# 获取所有天气数据
def get_map_weather():
    if qweather and wea_city_list:
        map_weather_tip = None
        weather_list = list(map(get_weather, wea_city_list))
        weather_list = list(filter(None, weather_list))
        if weather_list:
            map_weather_tip = "\n".join(weather_list)
        return map_weather_tip
    else:
        print("和风天气秘钥qweather或城市city配置缺失")
        return None
