#! -*-coding:utf-8 -*-
from urllib import request, parse
from bs4 import BeautifulSoup as Bs
import json
#from db import MysqlDb
import xlwt
import datetime
import re
import os,sys
import pinyin

sys.path.append('../')
from db import MysqlDb
from spider import spider

class liepin(spider):
    def __init__(self):
        super(liepin, self).__init__()
        self.pn = 0
        self.max_pn = 5
        #self.max_pn = 1
        self.headers = {
            'Accept-Encoding': 'deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'cache-control': 'no-cache',
        }
        self.url = r'https://www.liepin.com/sz/zhaopin/'

    def set_url_info(self, _headers=None, _url=None, _pn=None, _keyword=None, _city=None):
        if _headers != None:
            self.headers = _headers
        if _city !=None:
            self.city = _city
            cityHeader = self.to_city(self.city, "HEAD")
            self.url = r'https://www.liepin.com/' + cityHeader + r'/zhaopin/'
        if _pn != None:
            self.pn = _pn
        if _keyword != None:
            self.keyword = _keyword
        if _url != None:
            self.url = _url

        _body = parse.urlencode([
            ('key', self.keyword),
            ('curPage', self.pn)
        ])

        _u = self.url + '?' + _body
        return _u, _body, self.headers, 'GET'

    def get_job(self, _page, _type):
        soup = Bs(_page, "lxml")
        for li in soup.find_all('li'):
            info = []
            span = li.find('span', {"class": "job-name"})
            if span == None:
                continue
            a = span.find('a')
            if a != None:
                info.append(a['href'])
            else:
                continue
            info.append(span.span.string)
            p = li.find('p', {"class": "company-name"})
            a = p.find('a')
            info.append(a.string.split(' ')[-1])
            p = li.find('p', {"class": "condition clearfix"})
            for element in p.find_all('span'):
                info.append(element.string)
            self.translate_simple(info)

    def translate_simple(self, jsData):
        infoList = jsData
        self.job['job_url'] = infoList[0]
        self.job['positionName'] = infoList[1]
        self.job['companyFullName'] = infoList[2]
        self.job['companySize'] = None
        self.job['workYear'] = infoList[6]
        self.job['education'] = infoList[5]
        self.job['salary'] = infoList[3]
        if (self.job['positionName'] != None):
            print("************************")
            print(self.job)
            self.save2excel(self.job)
        infoList=[]
        return self.job


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
    liepinSpider = liepin()
    liepinSpider.get_jobs(keyword, city)





