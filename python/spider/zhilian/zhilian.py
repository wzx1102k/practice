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
        self.url = r'http://sou.zhaopin.com/jobs/searchresult.ashx'

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
            ('jl', city),
            ('kw', keyword),
            ('p', pn)
        ])
        #post
        u = url + '?' + data
        req = request.Request(u)
        page = request.urlopen(req).read()
        return page

    def get_job(self, page):
        soup = Bs(page, "lxml")
        cnt = 0
        for td in soup.find_all('td'):
            #print(td)
            tdList = td.attrs
            if 'class' in tdList.keys():
                if tdList['class'] == ['zwmc'] or tdList['class'] == ['gsmc']:
                    print(td.find_all('a'))
            for li in td.find_all('li'):
                liList = li.attrs
                if liList['class'] == ['newlist_deatil_two']:
                    print(li)

    def get_jobs(self, skeyword=None, scity=None):
        for idx in range(1,self.max_pn):
            page = self.get_page(pn=idx, keyword=skeyword, city=scity)
            self.get_job(page)

if __name__ == '__main__':
    cnt = len(sys.argv)
    if cnt == 2:
        keyword = sys.argv[1]
        city = None
    elif cnt == 3:
        keyword = sys.argv[1]
        city = sys.argv[2]
    else:
        keyword = None
        city = None
    zhilianSpider = zhilian()
    zhilianSpider.get_jobs(keyword, city)





