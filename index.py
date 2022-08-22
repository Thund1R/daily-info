import requests
import json
import datetime
import re

# 企业微信机器人配置
corpid = ""
corpsecret = ""
agentid = ""
# 和风天气key
qweather_key = ""
# 天气预报地址
# 城市
city = ""


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
    city_url = f'https://geoapi.qweather.com/v2/city/lookup?key={qweather_key}&location={city}'
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
    weather_url = f"https://devapi.qweather.com/v7/weather/3d?key={qweather_key}&location={city_id}"
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
    r = requests.get(ciba_url)
    r = json.loads(r.text)
    ciba_content = r["content"]
    ciba_share = r["fenxiang_img"]
    ciba_note = r["note"]
    return {
        "ciba_content": ciba_content,
        "ciba_share": ciba_share,
        "ciba_note": ciba_note
    }


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
    weather_info = weather_data["weather_info"]
    weather_link = weather_data["weather_link"]
    article = [{
        "title": today_date+"\n"+bing_title,
        "url": f"https://ii.vercel.app/show/?t={bing_title}&p={bing_pic}&c={bing_content}",
        "picurl": bing_pic
    }, {
        "title": ciba_content+"\n"+ciba_note,
        "url": f"https://ii.vercel.app/show/?t={ciba_content}&p={ciba_share}&c={ciba_note}",
        "picurl": ciba_share
    }, {
        "title": city + "天气："+weather_info,
        "url": weather_link,
        "picurl": get_pic()
    }]
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
    req = requests.get(url, params=values)
    data = json.loads(req.text)
    if data["errcode"] == 0:
        return data["access_token"]
    else:
        print("企业微信access_token获取失败: " + str(data))
        return None

# 推送信息


def push():
    values = handle_message()
    token = get_token(corpid, corpsecret)
    if token is None:
        return
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
    resp = requests.post(url, json=values)
    data = json.loads(resp.text)
    if data["errcode"] == 0:
        print("企业微信消息发送成功")
        return 1
    elif data["errcode"] != 0:
        print("企业微信消息发送失败: "+str(data))
        return 0


def main_handler(event, context):
    push()


def handler(event, context):
    push()


if __name__ == "__main__":
    push()
