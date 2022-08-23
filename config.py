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
    # 目标日期
    "targetday": "",
    # 目标名称
    "targetname": ""
}


def get(key: str):
    value = os.getenv(key)
    if value is None:
        if key in SYS_CONFIG:
            value = SYS_CONFIG[key]
    return value
