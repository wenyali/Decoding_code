#!/usr/bin/env python
# _*_coding:utf-8 _*_
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions



__title__ = ''
__author__ = "wenyali"
__mtime__ = "2018/5/13"

def get_filml_list_url(url:str)->list:
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    divs = soup.select("body > div.container > div > div")
    div = divs[2:14]
    film_list_url = []
    for item in div :
        film_list_url.append(url+item.a.get("href"))
    return film_list_url

def get_film_watch_url(url:str)->str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    watch_url = soup.select("body > div.container > div.container-fluid > div > div.col-md-9 > div > div.col-md-4 > div.online-button > a")
    return watch_url[0].get("href")

def get_origin_url(url:str)->str:
    chromeOptions = Options()
    prefs = {
        "profile.managed_default_content_settings.images":1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player":1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player":1,

    }
    chromeOptions.add_experimental_option("prefs",prefs)

    # 为了让 chromedriver 支持 falsh，picture 的加载,添加属性 chrome_options
    driver = webdriver.Chrome(executable_path=r"..\depend_soft\chromedriver",chrome_options=chromeOptions)

    if "http://www.m4yy.com" in url:
        driver.get(url)
    else:
        driver.get("http://www.m4yy.com" + url)

    # 获取 cciframe 这个 iframe 框架，并让 driver 使用 switch_to.frame() 方法进入到 cciframe 中，
    # 这样才能获取到 cciframe 所有的元素
    # 备注： 如果是 framerest 框架，则不需要进入
    cciframe = driver.find_element_by_css_selector(".container-fluid #player #cciframe")
    driver.switch_to.frame(cciframe)

    # 设置一个等待时间，知道某个 element 课件  其中 By.(ID/TAG_NAME/CSS_SELECTOR/...) 是通过某种选择器来设置
    wait = WebDriverWait(driver,30)
    wait.until(expected_conditions.visibility_of_element_located((By.ID, "player")))

    # 获取视频播放的最终路径的 iframe 的src 属性获取
    player_iframe = driver.find_element_by_css_selector("#player > iframe")
    origin_url = player_iframe.get_attribute("src")
    return origin_url

if __name__ == "__main__":

    # 电影主页地址
    url = "http://www.m4yy.com"

    #获取主页所有电影 URL
    film_list_url = get_filml_list_url(url)

    # 获取某个电影的播放 URL
    watch_url = get_film_watch_url(film_list_url[0])

    # 获取某个电影最原始的播放 URL
    origin_url = get_origin_url(watch_url)
    print(origin_url)

