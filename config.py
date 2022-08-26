import os
SYS_CONFIG = {
    # 企业微信机器人配置
    "corpid": "",
    "corpsecret": "",
    "agentid": "",
    # 和风天气key
    "qweather": "",
    # 天气预报地址
    "city": "",
    # 倒数日项目日期
    "targetday": "",
    # 倒数日项目名称
    "targetname": "",
    # 正数日项目日期
    "beginday": "",
    # 正数日项目名称
    "beginname": ""
    # 图文类型，1为单图文，2为多图文
    "msgtype": ""
}


def get(key: str):
    value = os.getenv(key)
    if value is None:
        if key in SYS_CONFIG:
            value = SYS_CONFIG[key]
    return value
