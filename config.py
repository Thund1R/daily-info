import os
SYS_CONFIG = {
    # 企业微信机器人配置
    "corpid": "",
    "corpsecret": "",
    "agentid": "",
    # 和风天气key
    "qweather": "",
    # 天气预报地址，格式：市-市/县/区，多地址以&&分隔，如：成都-成都&&南京-江宁
    "city": "",
    # 纪念日名称，每年都有的日子
    # 多日期以&&分隔，如：某某某的生日&&结婚纪念日
    "targetname": "",
    # 纪念日日期，公历格式20XX-XX-XX，农历年份前加n
    # 多日期以&&分隔，如n2020-08-11&&2021-08-26，注意与名称对应
    "targetday": "",
    # 单日项目名称，只有某一年有的日子
    # 多日期以&&分隔，例如跟XX在一起&&某某某出生
    "beginname": "",
    # 单日日期，公历格式20XX-XX-XX，农历年份前加n
    # 多日期以&&分隔，如n2020-08-11&&2021-08-26，注意与名称对应
    "beginday": "",
    # 图文类型，1为单图文，2为多图文
    "msgtype": ""
}


def get(key: str):
    value = os.getenv(key)
    if value is None:
        if key in SYS_CONFIG:
            value = SYS_CONFIG[key]
    return value
