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

def get_film_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    divs = soup.select("body > div.container > div > div")

    div = divs[2:14]
    film_list_url = []
    for item in div :
        film_list_url.append(url+item.a.get("href"))
    return film_list_url

def get_film_origin(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    origin_url = soup.select("body > div.container > div.container-fluid > div > div.col-md-9 > div > div.col-md-4 > div.online-button > a")
    return origin_url[0].get("href")

def get_origin(url):
    chromeOptions = Options()
    prefs = {
        "profile.managed_default_content_settings.images":1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player":1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player":1,

    }
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path=r".\depend_soft\chromedriver",chrome_options=chromeOptions)
    driver.get(url)
    time.sleep(10)
    iframes = driver.find_element_by_id("")
    print(iframes,len(iframes))

    # driver.switch_to.frame("cciframe")
    # wait = WebDriverWait(driver,60)
    # wait.until(expected_conditions.visibility_of_all_elements_located((By.TAG_NAME,"iframe")))
    # origin = driver.find_element_by_tag_name("iframe")
    # print(origin)
    # print(origin.text)
if __name__ == "__main__":
    url = "http://www.m4yy.com"
    film_list_url = get_film_url(url)
    origin_url = url+get_film_origin(film_list_url[0])
    origin = get_origin(origin_url)

