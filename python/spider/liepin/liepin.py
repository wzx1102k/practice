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

    def get_page(self, headers=None, url=None, pn=None, keyword=None, city=None):
        if headers == None:
            headers = self.headers
        if pn == None:
            pn = self.pn
        if keyword == None:
            keyword = self.keyword
        if city == None:
            city = self.city
        else:
            self.city = city
            cityHeader = self.to_city(city)
            self.url = r'https://www.liepin.com/' + cityHeader + r'/zhaopin/'
        if url == None:
            url = self.url
        if pn == 1:
            boo = 'true'
        else:
            boo = 'false'
        data = parse.urlencode([
            ('key', keyword),
            ('curPage', pn)
        ])
        #post
        u = url + '?' + data
        req = request.Request(u)
        page = request.urlopen(req).read()
        return page

    def get_job(self, page):
        soup = Bs(page, "lxml")
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

    def to_city(self, var_str):
        if isinstance(var_str, str):
            if var_str == 'None':
                return ''
            else:
                stringHead = ''
                for single in var_str:
                    stringHead += pinyin.get(single, format='strip', delimiter="")[0]
                return stringHead
        else:
            return ''

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





