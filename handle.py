'''
Author: Thund1r thund1r@foxmail.com
Date: 2022-09-22 14:34:31
LastEditTime: 2022-10-18 10:59:14
Description: 处理所有数据与网页

Copyright (c) 2022 by Thund1r thund1r@foxmail.com, All Rights Reserved. 
'''
# -*- coding: utf8 -*-
import config
import os
import api
import days
import diy
import weather
import covid

link = config.get("link")
pictype = config.get("pictype")
msgtype = str(config.get("msgtype")) if config.get("msgtype") else "1"
agentid = config.get("agentid")


# 处理所有信息
def handle_msg():
    info_list = []
    multi_list = []
    pic_type = pictype
    own_link = link
    own_pic = diy.get_my_pic()
    own_title = diy.get_my_title()
    own_content = diy.get_my_content()
    info_list.append(own_content)

    # 接受今日日期数据
    today_data = days.get_today()
    today_date = today_data["today_date"]

    # 接收必应数据
    bing_pic = ""
    bing_tip = ""
    bing_flag = 1
    bing_data = api.get_bing()
    if bing_data:
        bing_pic = bing_data["bing_pic"]
        bing_tip = bing_data["bing_tip"]

    art_title = today_date
    art_content = own_content
    art_pic = api.get_random_pic()
    if own_pic or own_title or pic_type:
        if own_pic:
            art_pic = own_pic
        if own_title:
            art_title += "\n" + own_title
        multi_list.append(handle_multi(
            art_title, art_title, art_content, art_pic, None))

    elif bing_tip and bing_pic:
        art_pic = bing_pic
        art_title = art_title + "\n" + bing_tip
        multi_list.append(handle_multi(
            art_title, art_title, art_content, art_pic, None))
        bing_flag = 0
    art_pic = art_pic if pic_type != "none" else None

    # 下面加入各数据的顺序即在卡片上显示的顺序
    # 不需要的数据请在下面对应的段落操作
    # 不需要出现在单图文的请删除info_list.append(XXX)
    # 不需要出现在多图文的请删除multi_list.append(XXX)
    # 都不要的数据直接删除一整段即可

    # 加入天气数据
    weather_tip = weather.get_map_weather()
    if weather_tip:
        info_list.append(weather_tip)
        multi_list.append(handle_multi(
            weather_tip, "Weather", weather_tip, None, None))

    # 加入日期提醒数据
    days_tip = days.get_map_days()
    if days_tip:
        info_list.append(days_tip)
        multi_list.append(handle_multi(
            days_tip, "Days", days_tip, None, None))

    # 加入疫情数据
    yq_tip = covid.get_map_yq()
    if yq_tip:
        info_list.append(yq_tip)
        multi_list.append(handle_multi(
            yq_tip, "COVID-19", yq_tip, None, None))

    # 加入必应数据
    if bing_flag and bing_pic and bing_tip:
        multi_list.append(handle_multi(
            "🖼️ "+bing_tip, "Bing", "🖼️ "+bing_tip, bing_pic, None))

    # 加入金山词霸数据
    ciba_data = api.get_ciba()
    if ciba_data:
        ciba_tip = ciba_data["ciba_tip"]
        ciba_pic = ciba_data["ciba_pic"]
        info_list.append(ciba_tip)
        multi_list.append(handle_multi(
            ciba_tip, "iCiba", ciba_tip, ciba_pic, None))

    # 加入ONE一个数据
    one_data = api.get_one()
    if one_data:
        one_tip = one_data["one_tip"]
        one_pic = one_data["one_pic"]
        info_list.append(one_tip)
        multi_list.append(handle_multi(
            one_tip, "ONE·一个", one_tip, one_pic, None))

    # 加入自定义XXX数据可以放置在下方，务必注意缩进，格式参考上方的加入ONE一个数据
    # # 加入XXX图文数据
    # XXX_data = api.get_XXX()
    # if XXX_data:
    #     XXX_tip = XXX_data["XXX_tip"]
    #     # 没有pic就删除下面这一句
    #     XXX_pic = XXX_data["XXX_pic"]
    #     # 单图文添加数据，不需要就删除下面这一句
    #     info_list.append(XXX_tip)
    #     # 多图文添加数据，不需要就删除下面这一整句
    #     multi_list.append(handle_multi(
    #         out_title, inner_title, content, pic, link))
    #     # out_title多图文卡片标题, inner_title多图文展示页内标题, content多图文内容, pic多图文头图, link自定义跳转链接
    #     # 没有的参数就填None，不能五个参数都没有

    # 处理文本格式
    art_content = "\n\n".join(info_list)
    html_content = art_content.replace("\n", "\\n")
    page_content = replace_symbol(art_content)
    page_title = replace_symbol(art_title)
    page_pic = art_pic

    art_url = None
    beta_url = None
    if own_link:
        beta_url = f"{own_link}?t={page_title}&p={page_pic}&c={page_content}"
        art_url = beta_url if len(
            beta_url) < 1000 else beta_url[:1000]+"······"

    article = ""
    if msgtype == "1":
        article = [{
            "title": art_title,
            "description": art_content,
            "url": art_url,
            "picurl": art_pic
        }]
    else:
        article = list(filter(None, multi_list))

    # 封装企业微信数据
    wecom_data = {
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

    # 封装测试号数据
    beta_data = {
        "art_url": beta_url,
        "art_content": art_content
    }

    # 封装html可用数据
    html_data = {
        "p": art_pic,
        "t": art_title,
        "c": html_content
    }

    # 封装所有数据
    msg_data = {
        "wecom_data": wecom_data,
        "html_data": html_data,
        "beta_data": beta_data
    }

    return msg_data


# 处理多图文内容
def handle_multi(out_title, inner_title, content, pic, art_link):
    if msgtype != "2":
        return None
    if out_title or inner_title or content or pic or art_link:
        if out_title is None:
            if content:
                out_title = content
            elif inner_title:
                out_title = inner_title
            else:
                out_title = "查看图片"
        picurl = pic or api.get_random_pic()
        inner_title = replace_symbol(inner_title)
        content = replace_symbol(content)

        multi_url = None
        if art_link is None:
            own_link = link
            if own_link:
                multi_url = f"{own_link}?t={inner_title}&p={picurl}&c={content}"
                if len(multi_url) > 1000:
                    multi_url = multi_url[:1000]+"······"
        else:
            multi_url = art_link

        return {
            "title": out_title,
            "url": multi_url,
            "picurl": picurl
        }
    else:
        print("多图文没有任何内容，生成链接失败")
        return None

# 处理个别字符替换


def replace_symbol(str_data):
    return str_data.replace("&", "%26").replace(
        "'", "%27").replace("\n", "\\n") if str_data else None


# 处理图文详情页
def handle_html(html_data):
    with open(os.path.join(os.path.dirname(__file__), "show.html"), 'r', encoding='utf-8') as f:
        html = f.read()
    p = html_data.get("p")
    t = html_data.get("t")
    c = html_data.get("c")
    if p and p != "none" and p != "None":
        html = html.replace('class="pic" style="display:none;',
                            'class="pic" style="').replace("<&p&>", p)
    if t and t != "none" and t != "None":
        t = t.replace("\\n", "<br/>")
        html = html.replace('class="title" style="display:none;',
                            'class="title" style="').replace("<&t&>", t)
    if c and c != "none" and c != "None":
        c = c.replace("\\n", "<br/>")
        html = html.replace('class="content" style="display:none;',
                            'class="content" style="').replace("<&c&>", c)
    return html
