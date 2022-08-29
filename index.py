import os
import requests
import json
from datetime import datetime, date, timedelta
import re
import config
import random
from zhdate import ZhDate

nowdatetime = (datetime.utcnow() + timedelta(hours=8))
corpid = config.get("corpid")
corpsecret = config.get("corpsecret")
agentid = config.get("agentid")
qweather = config.get("qweather")
link = config.get("link")
msg_type = str(config.get("msgtype")) if config.get("msgtype") else "1"
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


# 获取随机图片


def get_pic():
    try:
        pic_url = "https://api.btstu.cn/sjbz/api.php?format=json&lx=fengjing"
        r = requests.get(pic_url).json()
        return r["imgurl"]
    except Exception as e:
        print("获取随机图片数据出错:", e)
        return None


# 获取当前日期


def get_today():
    ndt = nowdatetime
    d = ndt.strftime("%Y{y}%m{m}%d{d}").format(y='年', m='月', d='日')
    w = int(ndt.strftime("%w"))
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    today_date = d + " " + week_list[w]
    now_time = ndt.strftime("%H:%M:%S")
    today_tip = "你好"
    if "00:00:00" <= now_time < "06:00:00":
        today_tip = "凌晨好~"
    elif "06:00:00" <= now_time < "09:00:00":
        today_tip = "早上好"
    elif "09:00:00" <= now_time < "12:00:00":
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
    emoticon_list = ["(￣▽￣)~*", "(～￣▽￣)～", "︿(￣︶￣)︿", "~(￣▽￣)~*", "(oﾟ▽ﾟ)o", "ヾ(✿ﾟ▽ﾟ)ノ", "٩(๑❛ᴗ❛๑)۶", "ヾ(◍°∇°◍)ﾉﾞ", "ヾ(๑╹◡╹)ﾉ", "(๑´ㅂ`๑)", "(*´ﾟ∀ﾟ｀)ﾉ", "(´▽`)ﾉ", "ヾ(●´∀｀●)",
                     "(｡◕ˇ∀ˇ◕)", "(≖ᴗ≖)✧", "(◕ᴗ◕✿)", "(❁´◡`❁)*✲ﾟ*", "(๑¯∀¯๑)", "(*´・ｖ・)", "(づ｡◕ᴗᴗ◕｡)づ", "o(*￣▽￣*)o", "(｀・ω・´)", "( • ̀ω•́ )✧", "ヾ(=･ω･=)o", "(￣３￣)a", "(灬°ω°灬)", "ヾ(•ω•`。)", "｡◕ᴗ◕｡"]
    return random.choice(emoticon_list)


# 获取bing每日壁纸数据


def get_bing():
    try:
        bing_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
        res = requests.get(bing_url).json()
        bing_pic = "https://cn.bing.com/"+res["images"][0]["url"]
        bing_title = res["images"][0]["title"]
        bing_content = re.sub(u"\\(.*?\\)", "", res["images"][0]["copyright"])
        bing_tip = bing_title+"——"+bing_content
        return {
            "bing_pic": bing_pic,
            "bing_title": bing_title,
            "bing_content": bing_content,
            "bing_tip": bing_tip
        }
    except Exception as e:
        print("获取必应数据出错:", e)
        return None


# 获取和风天气数据


def get_weather(city_name):
    try:
        city_id = None
        weather_list = []
        weather_info = None
        city = city_name.split("-")[0]
        county = city_name.split("-")[1]
        city_url = f"https://geoapi.qweather.com/v2/city/lookup?&number=20&key={qweather}&location={city}"
        city_json = requests.get(city_url).json()
        city_code = city_json["code"]
        if city_code.__eq__("200"):
            for city_data in city_json["location"]:
                county_name = city_data["name"]
                if county_name.__eq__(county):
                    city_id = city_data["id"]
        else:
            print(
                f"没有找到{city}这个地方，请检查city值是否正确，格式是否为 市-市/区/县 ，例如 成都-双流 ，不要有市区县等后缀")
        if city_id:
            weather_url = f"https://devapi.qweather.com/v7/weather/3d?key={qweather}&location={city_id}"
            weather_json = requests.get(weather_url).json()
            weather_code = weather_json["code"]
            if weather_code.__eq__("200"):
                temp = weather_json["daily"][0]
                textDay = temp["textDay"]
                tempMin = temp["tempMin"]
                tempMax = temp["tempMax"]
                weather_icon = get_weather_icon(textDay)
                weather_tip = f"{weather_icon} {county}{textDay}，{tempMin} ~ {tempMax} ℃"
                weather_list.append(weather_tip)
            # 获取穿衣指数
            life_url = f"https://devapi.qweather.com/v7/indices/1d?type=3&location={city_id}&key={qweather}"
            life_json = requests.get(life_url).json()
            life_code = life_json["code"]
            if life_code.__eq__("200"):
                life_tip = "👔 "+life_json["daily"][0]["text"]
                weather_list.append(life_tip)

            weather_info = '\n'.join(weather_list)
        else:
            print(
                f"获取{city_name}ID失败，请检查city值是否正确，格式是否为 市-市/区/县 ，例如 成都-双流 ，不要有市区县等后缀")
        return weather_info
    except Exception as e:
        print(f"获取{city_name}和风天气数据出错:", e)
        return None


# 获取天气icon


def get_weather_icon(text):
    weather_icon = "🌈"
    weather_icon_list = ["☀️",  "☁️", "⛅️",
                         "☃️", "⛈️", "🏜️", "🏜️", "🌫️", "🌫️", "🌪️", "🌧️"]
    weather_type = ["晴", "阴", "云", "雪", "雷", "沙", "尘", "雾", "霾", "风", "雨"]
    for index, item in enumerate(weather_type):
        if re.search(item, text):
            weather_icon = weather_icon_list[index]
            break
    return weather_icon


# 获取所有天气数据


def get_map_weather(city_name):
    if qweather and city_name:
        map_weather_tip = None
        weather_list = list(map(get_weather, city_name))
        weather_list = list(filter(None, weather_list))
        if weather_list:
            map_weather_tip = "\n".join(weather_list)
        return map_weather_tip
    else:
        print("和风天气配置缺失")
        return None


# 获取金山词霸数据


def get_ciba():
    try:
        ciba_url = "http://open.iciba.com/dsapi/"
        r = requests.get(ciba_url).json()
        ciba_en = r["content"]
        ciba_zh = r["note"]
        ciba_pic = r["fenxiang_img"]
        ciba_tip = "🔤 "+ciba_en+"\n"+"🀄️ "+ciba_zh
        return {
            "ciba_tip": ciba_tip,
            "ciba_pic": ciba_pic
        }
    except Exception as e:
        print("获取金山词霸数据出错:", e)
        return None


# 计算每年纪念日


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


# 计算某天间隔天数


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


def get_elemzero(elem):
    return elem[0]


def get_elemone(elem):
    return elem[1]


# 获取所有日期数据


def get_days_tip():
    days_list = []
    days_tip = ""
    target_res = ""
    if target_day_list or target_name_list:
        if len(target_day_list) == len(target_name_list):
            target_res = list(
                map(get_remain, target_day_list, target_name_list))
            days_list.extend(target_res)
        else:
            print("请检查纪念日target相关参数数量和有效性")
    else:
        print("未配置纪念日")

    begin_res = ""
    if begin_day_list or begin_name_list:
        if len(begin_day_list) == len(begin_name_list):
            begin_res = list(
                map(get_duration, begin_day_list, begin_name_list))
            days_list.extend(begin_res)
        else:
            print("请检查单日begin相关参数数量和有效性")
    else:
        print("未配置单日")

    days_list = list(filter(None, days_list))
    if days_list:
        days_list.sort(key=get_elemone)
        res = list(map(get_elemzero, days_list))
        days_tip = "\n".join(res)
    return days_tip


# 获取一个图文数据


def get_one():
    try:
        one_url = "https://apier.youngam.cn/essay/one"
        r = requests.get(one_url).json()['dataList'][0]
        one_id = "VOL."+r['id']
        one_pic = r['src']
        one_tip = f"✒️ {one_id} {r['text']}"
        return {
            "one_pic": one_pic,
            "one_tip": one_tip
        }
    except Exception as e:
        print("获取ONE一个图文数据出错:", e)
        return None

# 处理多图文内容增加


def handle_extra(out_title, inner_title, content, pic, article_link):
    if msg_type == "2":
        picurl = pic if pic else get_pic()
        inner_title = inner_title.replace("\n", "\\n")
        content = content.replace("\n", "\\n")
        url = article_link if article_link else f"{link}?t={inner_title}&p={picurl}&c={content}"
        return {
            "title": out_title,
            "url": url,
            "picurl": picurl
        }
    else:
        return None


# 处理信息


def handle_message():
    info_list = []
    extra_content = []
    today_data = get_today()
    today_date = today_data["today_date"]
    today_tip = today_data["today_tip"]
    info_list.append(today_tip)

    bing_pic = ""
    bing_tip = ""
    bing_title = ""
    bing_data = get_bing()
    if bing_data:
        bing_pic = bing_data["bing_pic"]
        bing_title = bing_data["bing_title"]
        bing_tip = bing_data["bing_tip"]
        extra_content.append(handle_extra(today_date+"\n"+bing_title,
                                          today_date, bing_tip, bing_pic, None))

    weather_tip = get_map_weather(city_name_list)
    if weather_tip:
        info_list.append(weather_tip)
        extra_content.append(handle_extra(
            weather_tip, "Weather", weather_tip, None, None))

    days_tip = get_days_tip()
    if days_tip:
        info_list.append(days_tip)
        extra_content.append(handle_extra(
            days_tip, "Days", days_tip, None, None))

    ciba_data = get_ciba()
    if ciba_data:
        ciba_tip = ciba_data["ciba_tip"]
        ciba_pic = ciba_data["ciba_pic"]
        info_list.append(ciba_tip)
        extra_content.append(handle_extra(
            ciba_tip, "iCiba", ciba_tip, ciba_pic, None))

    one_data = get_one()
    if one_data:
        one_tip = one_data["one_tip"]
        one_pic = one_data["one_pic"]
        info_list.append(one_tip)
        extra_content.append(handle_extra(
            one_tip, "ONE·一个", one_tip, one_pic, None))

    info_content = "\n\n".join(info_list)
    info_detail = info_content.replace("\n", "\\n")
    info_desp = info_content[:230] + \
        '......' if len(info_content) > 230 else info_content

    article = [{
        "title": today_date + "\n" + bing_title,
        "description": info_desp,
        "url": f"{link}?t={today_date}&p={bing_pic}&c={bing_tip}\\n\\n{info_detail}",
        "picurl": bing_pic
    }]

    if msg_type == "2":
        article = list(filter(None, extra_content))
    msg = {
        "touser": "@all",
        "toparty": "",
        "totag": "",
        "msgtype": "news",
        "agentid": agentid,
        "news": {
            "articles": article
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


# 处理页面


def handle_html(url_data):
    with open(os.path.join(os.path.dirname(__file__), "show.html"), 'r', encoding='utf-8') as f:
        html = f.read()
    p = url_data.get("p")
    t = url_data.get("t")
    c = url_data.get("c")
    if p:
        html = html.replace(".pic{display:none}", "").replace("<&p&>", p)
    if t:
        t = t.replace("\\n", "<br/>")
        html = html.replace(".title{display:none}", "").replace("<&t&>", t)
    if c:
        c = c.replace("\\n", "<br/>")
        html = html.replace(".content{display:none}", "").replace("<&c&>", c)
    return html


# 主函数


def main():
    if corpid and corpsecret and agentid:
        data = handle_message()
        token = get_token(corpid, corpsecret)
        if token is None:
            return 0
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
        res = requests.post(url, json=data).json()
        if res["errcode"] == 0:
            print("企业微信消息发送成功")
            return 1
        elif res["errcode"] != 0:
            print("企业微信消息发送失败: "+str(res))
            return 0
    else:
        print("企业微信机器人配置缺失")
        return 0


# 腾讯云入口函数


def main_handler(event, context):
    url_data = event.get("queryString")
    if url_data:
        html = handle_html(url_data)
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html
        }
    else:
        res = main()
        if res:
            return {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": {"Content-Type": "text/html"},
                "body":'{"code":"200","message":"企业微信消息发送成功"}' 
            }
        else:
            return {
                "isBase64Encoded": False,
                "statusCode": 404,
                "headers": {"Content-Type": "text/html"},
                "body":'{"code":"404","message":"企业微信消息发送失败"}' 
            }


def handler(event, context):
    main()


if __name__ == "__main__":
    main()
