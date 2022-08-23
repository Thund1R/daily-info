import requests
import json
import datetime
import re
import config
from zhdate import ZhDate

corpid = config.get("corpid")
corpsecret = config.get("corpsecret")
agentid = config.get("agentid")
qweather = config.get("qweather")
city = config.get("city")
targetday = config.get("targetday").split("&&")
targetname = config.get("targetname").split("&&")
target_day = list(filter(None, targetday))
target_name = list(filter(None, targetname))


# 获取当前日期


def get_date():
    a = datetime.datetime.now()
    y = str(a.year)
    m = str(a.month)
    d = str(a.day)
    date = y + '年' + m + '月' + d + '日'
    return date

# 获取随机图片


def get_pic():
    pic_url = "https://api.btstu.cn/sjbz/api.php?format=json&lx=fengjing"
    r = requests.get(pic_url).json()
    return r["imgurl"]

# 获取bing每日壁纸链接


def get_bing():
    bing_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
    res = requests.get(bing_url).json()
    bing_pic = "https://cn.bing.com/"+res["images"][0]["url"]
    bing_title = res["images"][0]["title"]
    bing_content = re.sub(u"\\(.*?\\)", "", res["images"][0]["copyright"])
    return {
        "bing_pic": bing_pic,
        "bing_title": bing_title,
        "bing_content": bing_content
    }

# 获取城市ID


def get_city_id():
    city_url = f'https://geoapi.qweather.com/v2/city/lookup?key={qweather}&location={city}'
    city_json = requests.get(city_url).json()
    city_code = city_json["code"]
    if city_code.__eq__("200"):
        return city_json["location"][0]["id"]
    else:
        print("访问获取地区接口失败！")
        return None

# 获取城市天气信息


def get_today_weater():
    city_id = get_city_id()
    weather_url = f"https://devapi.qweather.com/v7/weather/3d?key={qweather}&location={city_id}"
    weather_json = requests.get(weather_url).json()
    weather_link = weather_json["fxLink"]
    res_code = weather_json["code"]
    if res_code.__eq__("200"):
        today_weather = weather_json["daily"][0]
        weather_info = f"{today_weather['textDay']}，{today_weather['tempMin']}~{today_weather['tempMax']}℃"
        return {
            'weather_info': weather_info,
            'weather_link': weather_link
        }
    else:
        print("获取天气失败！")
        return None

# 获取词霸图片与每日一句


def get_ciba():
    ciba_url = "http://open.iciba.com/dsapi/"
    r = requests.get(ciba_url).json()
    ciba_content = r["content"]
    ciba_share = r["fenxiang_img"]
    ciba_note = r["note"]
    return {
        "ciba_content": ciba_content,
        "ciba_share": ciba_share,
        "ciba_note": ciba_note
    }

# 获取一个图文


def get_one():
    one_url = "https://apier.youngam.cn/essay/one"
    r = requests.get(one_url).json()['dataList'][0]
    one_id = r['id']
    one_pic = r['src']
    one_text = r['text']
    return {
        "one_id": one_id,
        "one_pic": one_pic,
        "one_text": one_text
    }


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
        tip = f"🌟{target_name}就是今天啦！"
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
        tip = f"距离{target_name}还有 {remain_day} 天"
    else:
        next_date = this_date
        remain_day = int(str(next_date.__sub__(today)).split(" ")[0])
        tip = f"距离{target_name}还有 {remain_day} 天"
    return (tip, remain_day)


def get_elemzero(elem):
    return elem[0]


def get_elemone(elem):
    return elem[1]


def handle_target():
    if target_day and target_name and len(target_day) == len(target_name):
        r = list(map(get_remain, target_day, target_name))
        r.sort(key=get_elemone)
        res = list(map(get_elemzero, r))
        target_tip = '\n'.join(res)
        return target_tip
    else:
        print("请检查倒数日数据有效性与数量")
        return None

# 处理信息


def handle_message():
    today_date = get_date()
    bing_data = get_bing()
    weather_data = get_today_weater()
    bing_pic = bing_data["bing_pic"]
    bing_title = bing_data["bing_title"]
    bing_content = bing_data["bing_content"]

    ciba_data = get_ciba()
    ciba_content = ciba_data["ciba_content"]
    ciba_share = ciba_data["ciba_share"]
    ciba_note = ciba_data["ciba_note"]

    one_data = get_one()
    one_id = one_data['one_id']
    one_pic = one_data["one_pic"]
    one_text = one_data["one_text"]

    article = [{
        "title": today_date+"\n"+bing_title,
        "url": f"https://ii.vercel.app/show/?t={bing_title}&p={bing_pic}&c={bing_content}",
        "picurl": bing_pic
    }, {
        "title": ciba_content+"\n"+ciba_note,
        "url": f"https://ii.vercel.app/show/?t={ciba_content}&p={ciba_share}&c={ciba_note}",
        "picurl": ciba_share
    }, {
        "title": one_text,
        "url": f"https://ii.vercel.app/show/?t=VOL.{one_id}&p={one_pic}&c={one_text}",
        "picurl": one_pic
    }]

    target_tip = handle_target()
    if target_tip:
        target_pic = get_pic()
        target_content = target_tip.replace("\n", "\\n")
        article.append({
            "title": target_tip,
            "url": f"https://ii.vercel.app/show/?t=📆倒数日&p={target_pic}&c={target_content}",
            "picurl": target_pic
        })

    if qweather and city:
        weather_info = weather_data["weather_info"]
        weather_link = weather_data["weather_link"]
        weather_pic = get_pic()
        article.append({
            "title": city + "天气："+weather_info,
            "url": weather_link,
            "picurl": weather_pic
        })

    data = {
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
    return data

# 获取调用接口凭证


def get_token(corpid, corpsecret):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {
        'corpid': corpid,
        'corpsecret': corpsecret,
    }
    res = requests.get(url, params=values).json()
    if res["errcode"] == 0:
        return res["access_token"]
    else:
        print("企业微信access_token获取失败: " + str(res))
        return None

# 推送信息


def push():
    values = handle_message()
    token = get_token(corpid, corpsecret)
    if token is None:
        return
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
    res = requests.post(url, json=values).json()
    if res["errcode"] == 0:
        print("企业微信消息发送成功")
        return 1
    elif res["errcode"] != 0:
        print("企业微信消息发送失败: "+str(res))
        return 0


def main_handler(event, context):
    push()


def handler(event, context):
    push()


if __name__ == "__main__":
    push()
