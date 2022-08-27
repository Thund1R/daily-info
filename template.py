# 函数模板


# 获取XXX数据


def get_XXX():
    try:
        # 接口地址
        XXX_url = "https://XXXX.XXX"
        # 数据结果并转换成json格式
        XXX_res = requests.get(XXX_url).json()
        # 根据数据的层级数和Key获取数据，至少一条数据
        XXX_item0 = XXX_res[1]["需要的数据名称key"]
        XXX_item1 = XXX_res[2]["需要的数据名称key"]

        ......

        # 图片，最多一张，不需要就删除下面这一句
        XXX_pic = XXX_res[数字n]["需要的图片地址名称key"]
        # 拼接数据
        # 根据实际情况，选择直接拼接两个元素，还是emoji加一个元素加换行符再加emoji和下一个元素
        # emoji可以自己去https://www.emojiall.com/zh-hans选，emoji后面加一个空格
        XXX_tip = "✒️ " + XXX_item0 + "\n" + "🗓️ " + XXX_item1
        return {
            # 没有图片就删除下面这一句
            "XXX_pic": XXX_pic,
            "XXX_tip": XXX_tip
        }
    except Exception as e:
        print("获取XXX数据出错:", e)
        return None


# 处理信息


def handle_message():

    ......

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
        # 前三个参数必填。后两个参数pic、link没有就填None
