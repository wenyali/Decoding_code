#!/usr/bin/env python
# _*_coding:utf-8 _*_

import requests
from bs4 import BeautifulSoup
import base64
from PIL import Image
from io import BytesIO
import pytesseract

__title__ = ''
__author__ = "wenyali"
__mtime__ = "2018/5/11"

# 发起请求，获取服务器返回的response对象
response = requests.get("http://example.webscraping.com/places/default/user/register")
# 将我们传入的内容进行解析，解析成一个树形的结构。
soup = BeautifulSoup(response.text, "html.parser")
li = soup.select("#recaptcha > img")
src = li[0].get("src")
src = src.replace("data:image/png;base64,", "")
# 对base64字符串进行解码，返回二进制形式。
binary = base64.b64decode(src)
# with open("1.jpg", "wb") as f:
#     f.write(binary)
# 读取本地的图片，返回一个Image类型的对象。
# image = Image.open("1.jpg")
# Image.open函数需要一个文件对象（或者是类文件对象【指的就是像文件一样的对象，即具有read，write等方法的对象。】）
# 很遗憾，不支持
# image = Image.open(binary)
# 可以使用BytesIO这个类文件对象来实现。
image = Image.open(BytesIO(binary))
# 保存Image对象所代表的图片。
image.save("original.jpg")
# 注意：需要执行tesseract文件所在的路径。
# 指定有两种方式：
# 1 设置环境变量
# 2 pytesseract.pytesseract.tesseract_cmd = “tesseract所在的路径”
pytesseract.pytesseract.tesseract_cmd = r'..\depend_soft\tesseract\Tesseract-OCR\tesseract'
# 对图片进行处理，提取验证码的有效信息。【尽可能将验证码与背景色进行分离-区分度越明显越好】
# 将图片转换成灰度图。【该操作是一个复制操作，没有修改原有的Image对象。】
image = image.convert("L")
# 将图片进行二值化。【将图片的所有像素点只含有两个值，0与255，目的是方便OCR进行识别。】
# point方法可以进行图像的像素处理。参数是一个函数，函数具有一个参数值，同时，具有一个返回值，返回值为像素点处理之后的值。
# 图像的每一个像素点调用一次该函数，传入像素点的值。


# def manage(pixel):
#     if pixel == 0:
#         return pixel
#     else:
#         return 255


image = image.point(lambda x: 0 if x == 0 else 255)
image.save("binaryzation.jpg")
# 显示图片
# image.show()
# 传入一个Image对象，返回识别之后的结果。
text = pytesseract.image_to_string(image, config="--psm 7")
print(text)