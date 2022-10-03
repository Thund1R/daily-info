'''
Author: thund1r thuncoder@foxmail.com
Date: 2022-08-22 15:41:27
LastEditTime: 2022-09-22 18:01:34
Description: 主程序

Copyright (c) 2022 by thund1r thuncoder@foxmail.com, All Rights Reserved. 
'''
# -*- coding: utf8 -*-
import send
import handle


# 腾讯云入口函数
def main_handler(event, context):
    show_data = event.get("queryString")
    if show_data:
        show_html = handle.handle_html(show_data)
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": show_html
        }
    else:
        res = main()
        if res["code"]:
            return {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": {"Content-Type": "text/html"},
                "body": res
            }
        else:
            return {
                "isBase64Encoded": False,
                "statusCode": 404,
                "headers": {"Content-Type": "text/html"},
                "body": res
            }


# 其他云函数入口
def handler(event, context):
    main()


# 主函数
def main():
    return send.send_msg()


# 本地运行入口
if __name__ == "__main__":
    main()
