import requests
import json
import datetime
import re
import config
import random
from zhdate import ZhDate

corpid = config.get("corpid")
corpsecret = config.get("corpsecret")
agentid = config.get("agentid")
qweather = config.get("qweather")
city = config.get("city").split("&&")
city_name_list = list(filter(None, city))
targetday = config.get("targetday").split("&&")
targetname = config.get("targetname").split("&&")
target_day_list = list(filter(None, targetday))
target_name_list = list(filter(None, targetname))
beginday = config.get("beginday").split("&&")
beginname = config.get("beginname").split("&&")
begin_day_list = list(filter(None, beginday))
begin_name_list = list(filter(None, beginname))


# 获取当前日期


def get_time():
    a = datetime.datetime.now()
    y = str(a.year)
    m = str(a.month)
    d = str(a.day)
    w = int(a.strftime("%w"))
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    today_date = y + "年" + m + "月" + d + "日  " + week_list[w]
    now_time = a.strftime("%H:%M:%S")
    today_tip = "你好"
    if "00:00:00" <= now_time < "06:00:00":
        today_tip = "早上好~"
    if "06:00:00" <= now_time < "09:00:00":
        today_tip = "早上好"
    elif "9:00:00" <= now_time < "12:00:00":
        today_tip = "上午好"
    elif "12:00:00" <= now_time < "13:00:00":
        today_tip = "中午好"
    elif "13:00:00" <= now_time < "18:00:00":
        today_tip = "下午好"
    elif "18:00:00" <= now_time < "23:59:59":
        today_tip = "晚上好"
    return {
        "today_date": today_date,
        "today_tip": today_tip + " ~ " + get_emoticon()
    }


def get_emoticon():
    emoticon_list = ["(￣▽￣)~*", "(～￣▽￣)～ ", "︿(￣︶￣)︿", "[]~(￣▽￣)~*", "(oﾟ▽ﾟ)o  ", "ヾ(✿ﾟ▽ﾟ)ノ", "٩(๑❛ᴗ❛๑)۶", "ヾ(◍°∇°◍)ﾉﾞ", "ヾ(๑╹◡╹)ﾉ",  "(๑´ㅂ`๑) ", "(*´ﾟ∀ﾟ｀)ﾉ ", "ヽ(ﾟ∀ﾟ)ﾒ(ﾟ∀ﾟ)ﾉ ", "(´▽`)ﾉ ", "ヾ(●´∀｀●) ",
                     "(｡◕ˇ∀ˇ◕)", "(≖ᴗ≖)✧", "(◕ᴗ◕✿)", "(❁´◡`❁)*✲ﾟ*", "(๑¯∀¯๑)", "(*´・ｖ・)", "(づ｡◕ᴗᴗ◕｡)づ", "o(*￣▽￣*)o ", "(｀・ω・´)", "( • ̀ω•́ )✧", "ヾ(=･ω･=)o", "(￣３￣)a ", "(灬°ω°灬) ", "ヾ(•ω•`。)", "｡◕ᴗ◕｡"]
    return random.choice(emoticon_list)


# 获取bing每日壁纸数据


def get_bing():
    try:
        bing_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
        res = requests.get(bing_url).json()
        bing_pic = "https://cn.bing.com/"+res["images"][0]["url"]
        bing_title = res["images"][0]["title"]
        bing_content = re.sub(u"\\(.*?\\)", "", res["images"][0]["copyright"])
        bing_content = bing_title+"——"+bing_content
        return {
            "bing_pic": bing_pic,
            "bing_content": bing_content
        }
    except Exception as e:
        print("获取必应数据出错:", e)
        return None

# 获取和风天气数据


def get_weather(city_name):
    try:
        city_url = f"https://geoapi.qweather.com/v2/city/lookup?key={qweather}&location={city_name}"
        city_json = requests.get(city_url).json()
        city_id = city_json["location"][0]["id"]
        weather_url = f"https://devapi.qweather.com/v7/weather/3d?key={qweather}&location={city_id}"
        weather_json = requests.get(weather_url).json()
        temp = weather_json["daily"][0]
        textDay = temp["textDay"]
        tempMin = temp["tempMin"]
        tempMax = temp["tempMax"]
        weather_icon = get_weather_icon(textDay)
        life_url = f"https://devapi.qweather.com/v7/indices/1d?type=3&location={city_id}&key={qweather}"
        life_json = requests.get(life_url).json()
        life_tip = "👔 "+life_json["daily"][0]["text"]
        weather_info = f"{weather_icon} {city_name}{textDay}，{tempMin} ~ {tempMax} ℃" + \
            "\n" + life_tip
        return weather_info
    except Exception as e:
        print("获取和风天气数据出错:", e)
        return None


def get_weather_icon(text):
    weather_icon = "🌈"
    weather_icon_list = ["☀️", "⛅️", "☁️", "🌧️", "☃️", "🌩️", "🏜️", "🌫️", "🌪️"]
    weather_type = ["晴", "阴", "云", "雨", "雪", "雷", "沙", "雾", "风"]
    for index, item in enumerate(weather_type):
        if re.search(item, text):
            weather_icon = weather_icon_list[index]
            break
    return weather_icon


def get_map_weather(city_name):
    if qweather and city_name:
        r = list(map(get_weather, city_name))
        map_weather_tip = "\n".join(r)
        return map_weather_tip
    else:
        print("和风天气配置缺失")

    # 获取金山词霸数据


def get_ciba():
    try:
        ciba_url = "http://open.iciba.com/dsapi/"
        r = requests.get(ciba_url).json()
        ciba_content = r["content"]
        ciba_pic = r["fenxiang_img"]
        ciba_note = r["note"]
        ciba_content = "🔤 "+ciba_content+"\n"+"🀄️ "+ciba_note
        return {
            "ciba_content": ciba_content,
            "ciba_pic": ciba_pic,
        }
    except Exception as e:
        print("获取金山词霸数据出错:", e)
        return None


# 计算倒数日


def get_remain(target_day, target_name):
    today = datetime.date.today()
    this_year = datetime.datetime.now().year
    target_day_year = target_day.split("-")[0]
    # 判断是否为农历日期
    if target_day_year[0] == "n":
        lunar_mouth = int(target_day.split("-")[1])
        lunar_day = int(target_day.split("-")[2])
        # 今年日期
        this_date = ZhDate(this_year, lunar_mouth,
                           lunar_day).to_datetime().date()
    else:
        # 获取国历日期的今年对应月和日
        solar_month = int(target_day.split("-")[1])
        solar_day = int(target_day.split("-")[2])
        # 今年日期
        this_date = datetime.date(this_year, solar_month, solar_day)
    # 计算日期年份，如果还没过，按当年减，如果过了需要+1
    if today == this_date:
        remain_day = 0
        remain_tip = f"🌟 {target_name}就是今天啦！"
    elif today > this_date:
        if target_day_year[0] == "n":
            # 获取农历明年日期的月和日
            lunar_next_date = ZhDate(
                (this_year + 1), lunar_mouth, lunar_day).to_datetime().date()
            next_date = datetime.date(
                (this_year + 1), lunar_next_date.month, lunar_next_date.day)
        else:
            next_date = datetime.date(
                (this_year + 1), solar_month, solar_day)
        remain_day = int(str(next_date.__sub__(today)).split(" ")[0])
        remain_tip = f"🗓️ 距离{target_name}还有 {remain_day} 天"
    else:
        next_date = this_date
        remain_day = int(str(next_date.__sub__(today)).split(" ")[0])
        remain_tip = f"🗓️ 距离{target_name}还有 {remain_day} 天"
    return (remain_tip, remain_day)

# 计算间隔天数


def get_duration(begin_time, begin_name):
    a = datetime.datetime.now()
    b = datetime.datetime.strptime(begin_time, "%Y-%m-%d")
    duration_day = (a-b).days
    duration_tip = f"🗓️ {begin_name}已经 {duration_day} 天"
    return (duration_tip, duration_day)


def get_elemzero(elem):
    return elem[0]


def get_elemone(elem):
    return elem[1]

# 获取日期计算结果


def get_map_days(func, days, names):
    if days or names:
        if len(days) == len(names):
            r = list(map(func, days, names))
            r.sort(key=get_elemone)
            res = list(map(get_elemzero, r))
            map_days_tip = "\n".join(res)
            return map_days_tip
        else:
            print("请检查日期数据有效性与数量")
            return None
    else:
        print(func, "配置缺失")
        return None


# 处理信息


def handle_message():
    info_content = []
    time_data = get_time()
    today_date = time_data["today_date"]
    today_tip = time_data["today_tip"]
    info_content.append(today_tip)

    bing_data = get_bing()
    bing_pic = None
    if bing_data:
        bing_pic = bing_data["bing_pic"]
        bing_content = bing_data["bing_content"]
    weather_tip = get_map_weather(city_name_list)
    if weather_tip:
        info_content.append(weather_tip)

    days_tip = []
    remain_tip = get_map_days(get_remain, target_day_list, target_name_list)
    if remain_tip:
        days_tip.append(remain_tip)
    duration_tip = get_map_days(get_duration, begin_day_list, begin_name_list)
    if duration_tip:
        days_tip.append(duration_tip)
    if days_tip:
        days_tip = "\n".join(days_tip)
        info_content.append(days_tip)

    ciba_data = get_ciba()
    if ciba_data:
        ciba_content = ciba_data["ciba_content"]
        info_content.append(ciba_content)

    info_desp = "\n\n".join(info_content)
    info_detail = info_desp.replace("\n", "\\n")

    msg = {
        "touser": "@all",
        "toparty": "",
        "totag": "",
        "msgtype": "news",
        "agentid": agentid,
        "news": {
            "articles": [{
                "title": today_date + "\n" + bing_content,
                "description": info_desp,
                "url": f"https://ii.vercel.app/show/?t={today_date}" + "\\n" + f"{bing_content}&p={bing_pic}&c={info_detail}",
                "picurl": bing_pic
            }]
        },
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    return msg

# 获取调用接口凭证


def get_token(corpid, corpsecret):
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    values = {
        "corpid": corpid,
        "corpsecret": corpsecret,
    }
    res = requests.get(url, params=values).json()
    if res["errcode"] == 0:
        return res["access_token"]
    else:
        print("企业微信access_token获取失败: " + str(res))
        return None

# 推送信息


def push(token, data):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
    res = requests.post(url, json=data).json()
    if res["errcode"] == 0:
        print("企业微信消息发送成功")
        return 1
    elif res["errcode"] != 0:
        print("企业微信消息发送失败: "+str(res))
        return 0


def main():
    if corpid and corpsecret and agentid:
        values = handle_message()
        token = get_token(corpid, corpsecret)
        if token is None:
            return
        push(token, values)
        return
    else:
        print("请完善企业微信机器人配置！")
        return


def main_handler(event, context):
    main()


def handler(event, context):
    main()


if __name__ == "__main__":
    main()
