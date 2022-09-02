import os
SYS_CONFIG = {
    # 企业微信企业ID,必填
    "corpid": "",
    # 企业微信应用Secret,必填
    "corpsecret": "",
    # 企业微信AgentId,必填
    "agentid": "",
    # 和风天气Key，非必填
    "qweather": "",
    # 天气预报地址，非必填
    # 格式：省/市-市/县/区，多地址以&&分隔
    # 如：四川-成都&&江苏-南京
    "city": "",
    # 纪念日名称，非必填
    # 每年都有的日子，多日期以&&分隔
    # 如：某某某的生日&&结婚纪念日
    "targetname": "",
    # 纪念日日期，非必填
    # 公历格式20XX-XX-XX，农历年份前加n
    # 多日期以&&分隔，注意与名称对应
    # 如：n2020-08-11&&2021-08-26
    "targetday": "",
    # 单日项目名称，非必填
    # 只有某一年有的日子，多日期以&&分隔
    # 如：跟XX在一起&&某某某出生
    "beginname": "",
    # 单日日期，非必填
    # 公历格式20XX-XX-XX，农历年份前加n
    # 多日期以&&分隔，注意与名称对应
    # 如：n2020-08-11&&2021-08-26
    "beginday": "",
    # 图文类型，非必填
    # 1为单图文，2为多图文，默认单图文
    "msgtype": "",
    # 自定义头图链接，以http/https开始
    # 喝水图：https://b2.kuibu.net/file/imgdisk/2022/09/01/drink.png
    "pic": "",
    # 随机头图风格类型，默认fengjing。
    # 可选项meizi、dongman、fengjing、suiji、none，分别是妹子、动漫、风景、随机、单图文不显示图片
    # 来自搏天API:https://api.btstu.cn/
    "pictype": "",
    # 自定义标题，例如：今天的推送来啦！
    "title": "",
    # 自定义第一段内容，例如：记得喝水水哦~
    "content": "",
    # 自定义称呼，例如：宝贝~
    "call": "",
    # 图文详情页链接
    # 腾讯云函数用户填写API网关网址
    # 服务器用户请自行搭建网站，填写域名:端口/show
    "link": ""

}


def get(key: str):
    value = os.getenv(key)
    if value is None:
        if key in SYS_CONFIG:
            value = SYS_CONFIG[key]
    return value
