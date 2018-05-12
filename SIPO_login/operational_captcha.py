#!/usr/bin/env python
# _*_coding:utf-8 _*_

from PIL import Image
import pytesseract
import requests
from io import BytesIO

__title__ = ''
__author__ = "wenyali"
__mtime__ = "2018/5/11"

# image = Image.open("1.png")
# image = image.convert("L")
# image = image.point(lambda x: 0 if x < 125 else 255)

# 返回图像的大小。返回一个元素。元组中含有两个元素，第1个元素：宽度，第2个元素：高度。
# print(image.size)

# scale = 3
# 重新设置图片的大小。
# 参数是一个元组，元组含有两个元素。第1个元素：图像的宽度。第2个元素：图像的高度
# image = image.resize((round(image.size[0] * scale), round(image.size[1] * scale)))
# image.show()
# text = pytesseract.image_to_string(image, config="--psm 7")
# print(text)


# 过程
# 1 获取并解析验证码
# 2 获取表单所需要的参数，提交表单，进行登录。

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
# 创建Session会话，用来维护Cookie信息。
session = requests.session()

def get_captcha():
    """
    获取并返回验证码
    """
    captcha_url = "http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml"
    response = session.get(captcha_url, headers=headers)
    image = Image.open(BytesIO(response.content))
    image = image.convert("L")
    image = image.point(lambda x: 0 if x < 125 else 255)
    scale = 3
    image = image.resize((round(image.size[0] * scale), round(image.size[1] * scale)))
    image.save("binaryzation.jpg")
    pytesseract.pytesseract.tesseract_cmd = r'D:\soft\tesseract\Tesseract-OCR\tesseract'
    text = pytesseract.image_to_string(image, config="--psm 7")
    print("验证码上获取的运算为：",text)
    text = text[:text.index("=")]
    try:
        result = eval(text)
        print("计算的结果为：{}".format(result))
        return result
    except:
        return None

def log_in(captcha):
    """
    进行登录。
    """
    log_in_url = "http://www.pss-system.gov.cn/sipopublicsearch/wee/platform/wee_security_check"
    data = {"j_loginsuccess_url":"", "j_validation_code": captcha, "j_username": "d2VueWFsaV8xMjM=", "j_password":"d2VueWFsaTEx"}
    response = session.post(log_in_url, headers=headers, data=data)
    return response

def main():
    captcha = get_captcha()
    if captcha:
        response = log_in(captcha)
        if "wenyali_123，欢迎访问！" in response.text:
            print("登录成功")
        else:
            print("登录失败")

if __name__ == "__main__":
    main()