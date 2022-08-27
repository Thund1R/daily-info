<h1 align="center">DailyInfo</h1>
<h6 align="center">基于云函数的企业微信每日图文推送</h6>

## Introduction

- Bing必应 每日壁纸
- 金山词霸 每日一句
- ONE·一个 一图一句
- 和风天气 多地区天气预报
- 农历 / 公历多日期纪念日 / 单日提醒
- 可选的单图文 / 多图文推送模式
- ~~自带图文展示页~~（等官方修复）

## Preview

- 单图文

<div align=center><img src="docs/单图文.jpg" width="200"/>  <img src="docs/单图文详情.jpg" width="200"/></div>

- 多图文

<div align=center><img src="docs/多图文.jpg" width="200"/>  <img src="docs/多图文详情.jpg" width="200"/></div>

## Preparation

|  环境变量  |                             含义                             |  备注  |
| :--------: | :----------------------------------------------------------: | :----: |
|   corpid   |                        企业微信企业ID                        |  必填  |
| corpsecret |                      企业微信应用Secret                      |  必填  |
|  agentid   |                     企业微信应用AgentId                      |  必填  |
|  qweather  |                       和风天气应用Key                        | 非必填 |
|    city    | 天气预报地址，格式：市-市/区/县<br />多地区以&&间隔<br />例如：成都-成都&&南京-江宁 | 非必填 |
| beginname  | 单日项目名称，只有某一年有的日子<br />多日期以&&分隔<br />例如跟XX在一起&&某某某出生 | 非必填 |
|  beginday  | 单日日期，公历格式20XX-XX-XX<br />农历年份前加n，多日期以&&分隔<br />如n2020-08-11&&2021-08-26，注意与名称对应 | 非必填 |
| targetname | 纪念日名称，每年都有的日子<br />多日期以&&分隔<br />如：某某某的生日&&结婚纪念日 | 非必填 |
| targetday  | 纪念日日期，公历格式20XX-XX-XX<br />农历年份前加n，多日期以&&分隔<br />如n2020-08-11&&2021-08-26，注意与名称对应 | 非必填 |
|  msgtype   |        图文类型，默认单图文<br />1为单图文，2为多图文        | 非必填 |

## Deployment

超长完整版：[酷安图文](https://www.coolapk.com/feed/38775487?shareKey=YTYyZmUyYjMxMGIxNjMwYTRkYTc~)

精简版：[部署步骤](./docs/deployment.md)

## Update

[更新日志](./docs/update.md)

## Notice

- 提供**方法函数模板**[template.py](./template.py)用于大家自行拓展，玩得开心~
- 受vercel.app被ban的限制，**图文展示页**暂不可用，等待官方修复。
- 受企业微信的限制，2022年6月20日后新建应用必须配置企业可信IP，在此之前创建的应用不受此限制。建议使用云服务器或腾讯云函数等IP固定的方式，阿里云、华为云函数暂时均无此功能，可能无法正常运行本项目。
- 受企业微信API限制，超出字数限制部分文字将自动截断不展示。图文展示页面不受此限制，但仍受图片链接长度和文字长度的制约，**请合理安排多地区天气、多日期提醒等内容**。
- 腾讯云日志服务CLS将于2022年9月5日开始执行按量计费。请在配置并测试好云函数之后及时前往 **函数管理 - 函数配置** 中关闭日志投递，并在 [日志服务 CLS 控制台](https://console.cloud.tencent.com/cls) - 日志主题 中删除相应日志主题，避免后续产生不必要的费用。
- 所有环境变量均可通过直接修改 **config.py** 完成配置，系统环境变量优先级高于 **config.py** 。
- **日期提醒** 会自动排序，越接近的时间越显示在上方，以保证提醒的有效性。
- **和风天气预报** 会根据天气文本信息自动更换对应的天气emoji图标。
- **图文展示页** 来自我的项目 **Diary** —— 基于 Python Fastapi 部署于 Vercel 的简易图文展示，通过URL传递参数实现，不存储任何数据，开源地址   [Github](https://github.com/Thund1R/diary)     [Gitee](https://gitee.com/thund1r/diary)
