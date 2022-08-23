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
    # 生日
    "birthday": ""
}


def get(key: str):
    value = os.getenv(key)
    if value is None:
        if key in SYS_CONFIG:
            value = SYS_CONFIG[key]
    return value
