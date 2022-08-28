# Deployment

腾讯云函数：

### 1. 创建函数

新建 / 从头开始 / 事件函数 / 环境 Python3.7 / 内存 64MB / 执行超时时间 900秒 / 填入环境变量 / 网络配置-勾选固定出口IP / 其余配置默认 / 完成

创建完成后跳转导函数配置-网络配置-公网固定IP，填到企业微信应用的企业可信IP中。

### 2. 配置代码

函数代码 / 提交方法 - 在线编辑 / 终端-新终端 / 复制粘贴执行以下命令

```shell
rm -rf src
git clone https://gitee.com/thund1r/daily-info.git
mv daily-info src
cd src
pip3 install zhdate requests -t .
 
```

所有命令执行完毕后，点击部署，部署成功后点击测试，查看日志输出以及微信消息

配置触发器即可实现每天定时消息推送，例如：0 0 9 * * * *，即早上9:00:00发送消息，具体参考Cron相关文档

### 3. 更新代码

新终端执行以下命令

```shell
cd src
git pull
 
```

更新完后再次部署和测试即可