#! -*-coding:utf-8 -*-
from urllib import request, parse
from bs4 import BeautifulSoup as Bs
import json
#from db import MysqlDb
import xlwt
import datetime
import re
import os,sys

class zhilian(object):
    def __init__(self):
        self.headers = {
            'Accept-Encoding': 'deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'cache-control': 'no-cache',
        }
        self.pn = 1
        self.max_pn = 30
        self.city='深圳'
        self.keyword = "图像"
        self.url = r'http: // sou.zhaopin.com / jobs / searchresult.ashx'

    def get_page(self, headers=None, url=None, pn=None, keyword=None, city=None):
        if headers == None:
            headers = self.headers
        if pn == None:
            pn = self.pn
        if keyword == None:
            keyword = self.keyword
        if city == None:
            city = self.city
        if url == None:
            url = self.url
        if pn == 1:
            boo = 'true'
        else:
            boo = 'false'
        data = parse.urlencode([
            ('first', boo),
            ('jl', city),
            ('pn', pn),
            ('kd', keyword)
        ])
        req = request.Request(url, data, headers)
        #page = request.urlopen(req).read()
        page = request.urlopen(req).read()
        page = page.decode('utf-8')
        #request = urllib.Request(url)
        #page = urllib.urlopen(request)
        print(page)
        return page


if __name__ == '__main__':
    cnt = len(sys.argv)
    if cnt == 2:
        skeyword = sys.argv[1]
        scity = None
    elif cnt == 3:
        skeyword = sys.argv[1]
        scity = sys.argv[2]
    else:
        skeyword = None
        scity = None
    zhilianSpider = zhilian()
    zhilianSpider.get_page(keyword=skeyword, city=scity)




