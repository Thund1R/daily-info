# Deployment

### 腾讯云函数：

### 1.创建函数

新建 / 从头开始 / 事件函数 / 环境 Python3.7 / 高级设置 / 内存 64MB / 执行超时时间 900秒 / 填入环境变量 / 网络配置-勾选固定出口IP / 触发器配置-自定义创建-定时触发-自定义触发周期-Cron表达式示例0 0 9 * * * */ 其余配置默认 / 完成

创建完成后跳转导函数配置-网络配置-公网固定IP，填到企业微信应用的企业可信IP中。

### 2.配置代码

函数代码 / 提交方法 - 在线编辑 / 终端-新终端 / 复制粘贴执行以下命令

```shell
rm -rf src
git clone https://gitee.com/thund1r/daily-info.git
mv daily-info src
cd src
pip3 install --upgrade -r requirements.txt -t .
 
```

所有命令执行完毕后，点击部署，部署成功后点击测试，查看日志输出以及微信消息

### 3.配置页面

触发管理-创建触发器-触发方式-API网关触发-勾选启用集成响应-点击复制访问路径最后的复制按钮-粘贴到环境变量link

### 4.更新代码

新终端执行以下命令

```shell
git stash
git pull
git stash pop
pip3 install --upgrade -r requirements.txt -t .

```

更新完后再次部署和测试即可