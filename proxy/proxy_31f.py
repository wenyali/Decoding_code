#!/usr/bin/env python
# _*_coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup

__title__ = ''
__author__ = "wenyali"
__mtime__ = "2018/5/11"

def get_http_proproxy(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,"html.parser")
    tbody = soup.select("#ip_list > tr")
    proxy_list = []
    for item in tbody:
        try :
            proxy_list.append(item.select("td").__getitem__(1).string+":"+item.select("td").__getitem__(2).string)
        except IndexError:
            pass
    return proxy_list


if __name__ == "__main__":
    http_url = 'http://www.xicidaili.com/wt/'
    https_url = 'http://www.xicidaili.com/wn/'
    # http://31f.cn/http-proxy/ 网站的 http 代理
    proxy_http_list = get_http_proproxy(http_url)
    proxy_https_list = get_http_proproxy(https_url)
    print(proxy_http_list,"\n",proxy_https_list)
    print(len(proxy_http_list),len(proxy_https_list))
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
   #测试当前使用的代理IP 是否有用
    for i in range(len(proxy_http_list)-1):
        try :
            response = requests.get("http://www.whatismyip.com.tw/",headers=headers,proxies={'http':proxy_http_list[i],"https":proxy_https_list[i]})
        except:
            pass
            continue

        if response.status_code == 200:
            soup = BeautifulSoup(response.content.decode("utf-8"),"html.parser")
            ip = soup.select("body > span > b")[0].string
            print("当前的ip :",ip)
            break
