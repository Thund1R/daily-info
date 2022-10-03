# 函数模板，供爱好者自行研究拓展

# 以下内容请在本地运行测试，不要在云函数里测试！
# 以下内容请在本地运行测试，不要在云函数里测试！
# 以下内容请在本地运行测试，不要在云函数里测试！

# 每一行注释都很重要！请务必认真阅读
# 每一行注释都很重要！请务必认真阅读
# 每一行注释都很重要！请务必认真阅读

# 编写并测试好的获取数据函数要一整段复制粘贴到api.py文件中
# 另外把接收数据的一整段代码复制粘贴搭配handle.py文件的handle_msg()中

# 导包，不用管它
import requests

# 以下是在api.py文件中获取数据

# 编写:获取自定义文字
# 以下示例代码通过接口动态获取文字内容，并且接口返回的数据为json类型
# 不适用直接显示文字内容的接口
# 返回其他类型的接口请自行查看接口提供商文档、示例代码
# 自行百度学习Python request如何获取数据、Python相关语法
# 推荐文章:https://blog.csdn.net/Aai1624/article/details/121614182

# 测试成功后，复制以下代码，粘贴到api.py文件里
# 注意缩进格式，参考下方获取彩虹屁
def get_diy_text():
    try:
        # 接口地址
        XXX_url = "https://XXXX.XXX"
        # 数据结果并转换成json格式，只适用于返回json数据的接口，不适用直接显示文字内容的接口
        XXX_res = requests.get(XXX_url).json()
        print("获取自定义文字json数据:", XXX_res)

        # 根据数据在列表[]中的第n个（从0开始数）和字典{}中的键名获取数据，至少一条数据
        # 例如获取朝阳区位置id，打印出json数据是：
        # {"code":"200","location":[{"name":"朝阳","id":"101010300","lat":"XXXX"},{...}]...}
        # 需要的id是{}中的 location 后面的[]中的第 0 个{}中的 id 对应的值
        # 获取方式即XXX_item0 = XXX_res["location"][0]["id"]
        XXX_item0 = XXX_res["键名"][n]["需要的数据键名"]
        # 少了就再补充，多了就删除
        XXX_item1 = XXX_res["键名"][n]["需要的数据键名"]

        # 拼接数据
        # 标题title位置有限，不建议加emoji，不建议中间再换行，否则会显示不完全
        # 第一段内容content根据实际情况，选择直接拼接n个元素，还是一个元素加换行符再加下一个元素
        # emoji可以自己去 https://www.emojiall.com/zh-hans 选，文字格式与表情格式之间选表情格式，emoji后面加一个空格
        # 少了就再补充，多了就删除
        XXX_tip = "✒️ " + XXX_item0 + "🗓️ " + XXX_item1
        print("获取自定义文字:", XXX_tip)
        return XXX_tip
    except Exception as e:
        print("获取自定义文字错误:", e)
        return None


# # 示例：获取彩虹屁
# def get_chp():
#     try:
#         # 接口地址
#         caihong_url = "https://api.muxiaoguo.cn/api/caihongpi?api_key=" + 你的木小果平台Key
#         # 数据结果并转换成json格式
#         caihong_res = requests.get(caihong_url).json()
#         # 数据结果是{"code":200,"msg":"success","data":{"comment":"遇见你以后，我睁眼便是花田，闭眼便是星空。"}}
#         # 根据数据在列表[]中的第n个（从0开始数）和在字典{}中的键名获取数据
#         caihong_item0 = caihong_res["data"]["comment"]
#         # 拼接数据
#         caihong_tip = "🌈 " + caihong_item0
#         return caihong_tip
#     except Exception as e:
#         print("获取彩虹屁数据错误:", e)
#         return None


# 编写：获取自定义图片
# 以下示例代码通过接口动态获取文字内容，并且接口返回的数据为json类型
# 不适用直接显示图片的接口
# 其他类型接口请自行查看接口提供商文档、示例代码
# 自行百度学习Python request如何获取数据、Python相关语法
# 推荐文章:https://blog.csdn.net/Aai1624/article/details/121614182

# 获取到的图片链接务必包含 http:// 或 https://，没有请自行拼接上，否则无法显示
# 测试成功后，复制此段落代码，粘贴到api.py文件里
# 注意缩进格式，参考下方获取随机图片作为头图
def get_diy_pic():
    try:
        # 接口地址
        XXX_url = "https://XXXX.XXX"
        # 数据结果并转换成json格式，只适用于返回json数据的接口，不适用直接显示图片的接口
        XXX_res = requests.get(XXX_url).json()
        print("获取自定义图片json数据:", XXX_res)

        # 根据数据在列表[]中的第n个（从0开始数）和字典{}中的键名获取数据，至少一条数据
        # 例如获取朝阳区位置id，打印出json数据是：
        # {"code":"200","location":[{"name":"朝阳","id":"101010300","lat":"XXXX"},{...}]...}
        # 需要的id是{}中的 location 后面的[]中的第 0 个{}中的 id 对应的值
        # 获取方式即XXX_item0 = XXX_res["location"][0]["id"]
        # 图片链接务必包含 http:// 或 https:// 没有请自行拼接上，否则无法显示
        XXX_pic = XXX_res["键名"][n]["需要的图片地址键名"]
        print("获取自定义图片链接:", XXX_pic)
        return XXX_pic
    except Exception as e:
        print("获取自定义图片数据错误:", e)
        return None


# # 示例：获取随机图片作为头图(已经自带本功能，填写title、content或通过接口获取文本作为title、content都会触发)
# def get_diy_pic():
#     try:
#         pic_url = f"https://api.btstu.cn/sjbz/api.php?format=json&lx=fengjing"
#         r = requests.get(pic_url).json()
#         return r["imgurl"]
#     except Exception as e:
#         print("获取随机图片数据错误:", e)
#         return None


# 编写:获取XXX自定义图片与文字
# 单图文场景下只显示文字，显示位置取决于handle_message中放置顺序
# 多图文场景下即新增一篇文章，没有图片会获取随机图片。请注意，多图文最多支持总共8条图文
# 获取数据方法参考上方get_diy_text()、get_diy_pic()，仅返回值样式不同，参考下方get_ciba()

# 测试成功后把此函数复制粘贴回api.py，参考获取金山词霸数据get_ciba()位置放置
def get_XXX():
    try:
        XXX_url = "https://XXXX.XXX"
        XXX_res = requests.get(XXX_url).json()
        print("获取XXX自定义图片与文字json数据:", XXX_res)
        XXX_item0 = XXX_res["键名"][n]["需要的数据键名"]
        XXX_item1 = XXX_res["键名"][n]["需要的数据键名"]
        XXX_pic = XXX_res["键名"][n]["需要的数据键名"]
        XXX_tip = "✒️ " + XXX_item0 + "\n" + "🗓️ " + XXX_item1
        res = {
            # 没有图片就删除下面这一句
            "XXX_pic": XXX_pic,
            "XXX_tip": XXX_tip
        }
        print("获取XXX数据:", res)
        return res
    except Exception as e:
        print("获取XXX数据错误:", e)
        return None


# # 参考:获取金山词霸数据
# def get_ciba():
#     try:
#         ciba_url = "http://open.iciba.com/dsapi/"
#         r = requests.get(ciba_url).json()
#         ciba_en = r["content"]
#         ciba_zh = r["note"]
#         ciba_pic = r["fenxiang_img"]
#         ciba_tip = "🔤 "+ciba_en+"\n"+"🀄️ "+ciba_zh
#         res = {
#             "ciba_tip": ciba_tip,
#             "ciba_pic": ciba_pic
#         }
#         print("获取金山词霸数据:", res)
#         return res
#     except Exception as e:
#         print("获取金山词霸数据错误:", e)
#         return None


# 以下是在handle.py文件中handle_msg()中接收数据

# 编写:接收XXX数据
# 上面get_XXX()成功后务必添加下面这一段才能正常显示出来
# 参考 获取金山词霸数据 编写和位置摆放
# 此函数无法本地测试有效性，只能放回云函数的handle.py以后再次部署
def handle_msg():
    XXX_data = get_XXX()
    if XXX_data:
        XXX_tip = XXX_data["XXX_tip"]
        # 没有pic就删除下面这一句
        XXX_pic = XXX_data["XXX_pic"]
        # 单图文添加数据，不需要就删除下面这一句
        info_list.append(XXX_tip)
        # 多图文添加数据，不需要就删除下面这一整句
        extra_content.append(handle_extra(
            out_title, inner_title, content, pic, link))
        # 以上五个参数分别是多图文卡片标题, 多图文展示页内标题, 多图文内容, 多图文头图, 自定义跳转链接
        # 参数没有就填None，不能一个都没有

    # # 参考:获取金山词霸数据
    # ciba_data = get_ciba()
    # if ciba_data:
    #     ciba_tip = ciba_data["ciba_tip"]
    #     ciba_pic = ciba_data["ciba_pic"]
    #     info_list.append(ciba_tip)
    #     extra_content.append(handle_extra(
    #         ciba_tip, "iCiba", ciba_tip, ciba_pic, None))


# 运行程序
if __name__ == '__main__':
    # 测试哪个函数写哪个函数名字

    get_diy_text()
    # # 执行成功后打印出来的语句样式参考:
    # # 获取自定义文字json数据:{"XXX":"XXXXXXXX"}
    # # 获取自定义标题:XXXXXXXXX

    # get_diy_pic()
    # # 执行成功后打印出来的语句样式参考:
    # # 获取自定义图片json数据:{"XXX":"XXXXXXXX"}
    # # 获取自定义图片链接:https://XXX.XXX/XXX.XXX

    # get_XXX()
    # #执行成功后打印出来的语句样式参考:
    # 获取XXX自定义图片与文字json数据:{"XXX":"XXXXXXXX"}
    # 获取XXX数据: {'XXX_tip': "XXXXXX", 'XXXX_pic': "XXXXX"}
