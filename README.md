<h1 align="center">DailyInfo</h1>
<h6 align="center">基于云函数的企业微信每日图文推送</h6>

## Introduction

- Bing必应 每日壁纸
- 和风天气 天气预报
- 金山词霸 每日一句
- ONE·一个 一图一句
- 农历 / 公历多日期倒数日
- 多图文并自带图文展示页

## Preparation

|  环境变量  |                             含义                             |  备注  |
| :--------: | :----------------------------------------------------------: | :----: |
|     TZ     |              时区，国内用户填 **Asia/Shanghai**              |  必填  |
|   corpid   |                        企业微信企业ID                        |  必填  |
| corpsecret |                      企业微信应用Secret                      |  必填  |
|  agentid   |                     企业微信应用AgentId                      |  必填  |
|  qweather  |                       和风天气应用Key                        | 非必填 |
|    city    |                    天气预报地址 市/区/县                     | 非必填 |
| targetday  | 倒数日项目日期，公历格式：2001-01-01<br />农历年份前加n，格式：n2001-01-01<br />多日期以 && 间隔<br />格式：2001-01-01&&n2001-01-01 | 非必填 |
| targetname | 倒数日项目名称，多目标以 && 间隔<br />注意与日期位置对应<br />格式：张三生日&&结婚纪念日 | 非必填 |

## Preview

<div align=center><img src="pic/首页.jpg" width="150" alt="DiaryIndex"/>  <img src="pic/必应.jpg" width="150" alt="DiaryShow"/>  <img src="pic/金山.jpg" width="150" alt="DiaryShow"/></div>

<div align=center><img src="pic/一个.jpg" width="150" alt="DiaryShow"/>  <img src="pic/倒数.jpg" width="150" alt="DiaryShow"/>  <img src="pic/和风.jpg" width="150" alt="DiaryShow"/></div>

## Deployment

以腾讯云函数为例：

### 1. 创建函数：

新建 / 从头开始 / 事件函数 / 环境 Python3.7 / 内存 64MB / 执行超时时间 900秒 / 填入环境变量 / 自行设置触发器，其余内容默认 / 完成

### 2. 克隆代码：

函数代码 / 提交方法 - 在线编辑 / 点击 终端-新终端 / 复制粘贴执行以下命令

```shell
rm -rf src
git clone https://gitee.com/thund1r/daily-info.git
mv daily-info src
cd src
pip3 install zhdate requests -t .
```

所有命令执行完毕后，点击**部署**，部署成功后点击**测试**，查看日志输出以及微信消息

配置**触发器**即可实现每天定时消息推送

### 3. 更新代码：

新终端执行以下命令

```shell
cd src
git pull
```

更新完后再次部署和测试即可

## Notice

- **倒数日** 会自动排序，越接近的时间越显示在上方，以保证提醒的及时性。
- **ONE·一个 **每天更新时间为早上8:30，触发器早于此时间将收到前一天的一图一句。
- 腾讯云日志服务CLS将于2022年9月5日开始执行按量计费。请在配置并测试好云函数之后及时前往 **函数管理 - 函数配置** 中关闭日志投递，并在 [日志服务 CLS 控制台](https://console.cloud.tencent.com/cls) - 日志主题 中删除相应日志主题。
- **图文展示页 **来自我的项目 **Diary**——基于 Python Fastapi 部署于 Vercel 的简易图文展示，仅通过URL传递参数实现，不存储任何数据，开源地址  [Github](https://github.com/Thund1R/diary)   [Gitee](https://gitee.com/thund1r/diary)
