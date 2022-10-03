'''
Author: Thund1r thund1r@foxmail.com
Date: 2022-09-22 14:37:29
LastEditTime: 2022-10-03 04:08:27
Description: 发送数据

Copyright (c) 2022 by Thund1r thund1r@foxmail.com, All Rights Reserved. 
'''
# -*- coding: utf8 -*-
import config
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import handle


corpid = config.get("corpid")
corpsecret = config.get("corpsecret")
agentid = config.get("agentid")
appid = config.get("appid")
appsecret = config.get("appsecret")
userid_list = config.get_list("userid")
templateid = config.get("templateid")
emailfrom = config.get("emailfrom")
emailtoken = config.get("emailtoken")
emailto_list = config.get_list("emailto")


# 获取企业微信token
def get_wecom_token():
    try:
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        values = {"corpid": corpid, "corpsecret": corpsecret}
        res = requests.get(url, params=values).json()
        if res["errcode"] == 0:
            return res["access_token"]
        else:
            print(
                f"企业微信access_token获取失败： {str(res)} 请检查corpid、corpsecret、agentid是否正确填写，是否有多余空格")
            return None
    except Exception as e:
        print("获取企业微信access_token错误：", e)
        return None


# 发送企业微信消息
def send_wecom(msg_data):
    wecom_token = get_wecom_token()
    if wecom_token is None:
        return 0
    try:
        wecom_data = msg_data.get("wecom_data")
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={wecom_token}"
        res = requests.post(url, json=wecom_data).json()
        if res["errcode"] == 0:
            print("企业微信消息发送成功")
            return 1
        else:
            print(f"企业微信消息发送失败： {str(res)}")
            return 0
    except Exception as e:
        print("企业微信消息发送错误：", e)
        return 0


# 获取测试号token
def get_beta_token():
    try:
        token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
        access_token = requests.get(token_url).json()['access_token']
        return access_token
    except Exception as e:
        print("获取access_token失败，请检查app_id和app_secret是否正确：", e)
        return None


# 发送测试号消息
def send_beta(msg_data):
    beta_token = get_beta_token()
    if beta_token is None:
        return 0
    try:
        beta_data = msg_data.get("beta_data")
        send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={beta_token}"
        art_url = beta_data.get("art_url")
        art_content = beta_data.get("art_content")
        res_code = 1
        for item in userid_list:
            data = {
                "touser": item,
                "template_id": templateid,
                "url": art_url,
                "topcolor": "#FF0000",
                "data": {
                    "dailyinfo": {
                        "value": art_content
                    }
                }
            }
            res = requests.post(send_url, json=data).json()
            if res["errcode"] == 0:
                print("测试号消息发送成功")
            else:
                print(f"测试号消息发送失败： {str(res)}")
                res_code = 0
        return res_code
    except Exception as e:
        print("测试号消息发送错误：", e)
        return 0


# 发送邮件
def send_email(msg_data):
    em_from = emailfrom
    em_token = emailtoken
    em_to_list = emailto_list
    smtp_server = f'smtp.{em_from.split("@")[1]}'
    html_data = msg_data.get("html_data")
    subject = html_data.get("t")
    subject_list = subject.split("\n")
    html_title = None
    if len(subject_list) == 2:
        html_title = subject_list[1]
    em_html_data = {
        "p": html_data.get("p"),
        "t": html_title,
        "c": html_data.get("c")
    }
    em_html = handle.handle_html(em_html_data)
    msg = MIMEText(em_html, 'html', 'utf-8')
    msg["Subject"] = subject
    msg["From"] = em_from
    msg["To"] = ",".join(em_to_list)

    try:
        s = smtplib.SMTP_SSL(smtp_server, 465)
        s.login(em_from, em_token)
        s.sendmail(em_from, em_to_list, msg.as_string())
        s.quit()
        print("邮件发送成功")
        return 1
    except smtplib.SMTPException as e:
        print("邮件发送错误：", e)
        return 0


# 执行消息发送
def send_msg():
    wecom_res = 0
    email_res = 0
    res_list = []
    msg_data = {}
    if (corpid and corpsecret and agentid) or (emailfrom and emailto_list and emailtoken):
        msg_data = handle.handle_msg()
    else:
        return {"code": 0, "msg": "发送失败，没有配置任何推送渠道"}

    if corpid and corpsecret and agentid:
        wecom_res = send_wecom(msg_data)
        if wecom_res == 1:
            res_list.append("企业微信发送成功")
        else:
            res_list.append("企业微信发送失败")
    else:
        res_list.append("企业微信配置缺失")

    if appid and appsecret and userid_list:
        beta_res = send_beta(msg_data)
        if beta_res == 1:
            res_list.append("测试号发送成功")
        else:
            res_list.append("测试号发送失败")
    else:
        res_list.append("测试号配置缺失")

    if emailfrom and emailto_list and emailtoken:
        email_res = send_email(msg_data)
        if email_res == 1:
            res_list.append("邮件发送成功")
        else:
            res_list.append("邮件发送失败")
    else:
        res_list.append("邮件配置缺失")

    res_msg = ",".join(res_list)
    res_code = wecom_res or email_res
    res = {"code": res_code, "msg": res_msg}
    return res
