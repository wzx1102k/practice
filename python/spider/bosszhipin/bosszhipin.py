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
from spider import spider

class bosszhipin(spider):
    def __init__(self):
        super(bosszhipin, self).__init__()
        self.pn = 1
        self.max_pn = 10
        #self.max_pn = 1
        self.headers = {
            'Accept-Encoding': 'deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'cache-control': 'no-cache',
        }
        self.excel = 'bosszhipin.xls'
        self.url = r'https://www.zhipin.com/job_detail/'

    def set_url_info(self, _headers=None, _url=None, _pn=None, _keyword=None, _city=None):
        if _headers != None:
            self.headers = _headers
        if _city !=None:
            self.city = _city
        if _pn != None:
            self.pn = _pn
        if _keyword != None:
            self.keyword = _keyword
        if _url != None:
            self.url = _url

        citycode = {
            "深圳": "101280600",
            "上海": "101020100",
            "北京": "101010100",
            "广州": "101280100",
            "杭州": "101210100"
        }
        if self.city not in citycode.keys():
            print("Select city is not support, change to 深圳")
            self.city = "深圳"

        _body = parse.urlencode([
            ('scity', citycode[self.city]),
            ('query', self.keyword),
            ('page', self.pn)
        ])

        _u = self.url + '?' + _body
        return _u, _body, self.headers, 'GET'

    def get_job(self, _page, _type):
        soup = Bs(_page, "lxml")
        for li in soup.find_all('li'):
            info = []
            h3 = li.find('h3', {"class": "name"})
            if h3 == None:
                continue
            a = li.find('a')
            aList = a.attrs
            info.append(r'https://www.zhipin.com' + aList['href'])
            div = li.find('div', {"class": "company-text"})
            info.append(div.find('h3', {"class": "name"}).string)
            splitString = self.split_str(div, '</em>', '</p>', eStart=0, eEnd=1)
            if splitString != None:
                splitString1 = self.split_str(splitString, '', '<em', eStart=0, eEnd=0)
                if splitString1 == None:
                    splitString1 = ''
                info.append(splitString1)
                splitString1 = self.split_str(splitString, '</em>', '</p>', eStart=0, eEnd=0)
                if splitString1 == None:
                    splitString1 = ''
                info.append(splitString1)
            div = li.find('div', {"class": "info-primary"})
            splitString = self.split_str(div, 'name\">', '<span', eStart=0, eEnd=0)
            if splitString == None:
                splitString = ''
            info.append(splitString)
            span = div.find('span', {"class": "red"})
            info.append(span.string)
            splitString = self.split_str(div, '</em>', '</p>', eStart=0, eEnd=1)
            if splitString != None:
                splitString1 = self.split_str(splitString, '', '<em', eStart=0, eEnd=0)
                if splitString1 == None:
                    splitString1 = ''
                info.append(splitString1)
                splitString1 = self.split_str(splitString, '</em>', '</p>', eStart=0, eEnd=0)
                if splitString1 == None:
                    splitString1 = ''
                info.append(splitString1)
            self.translate_simple(info)

    def translate_simple(self, jsData):
        infoList = jsData
        self.job['job_url'] = infoList[0]
        self.job['positionName'] = infoList[4]
        self.job['companyFullName'] = infoList[1]
        self.job['companySize'] = infoList[3]
        self.job['workYear'] = infoList[6]
        self.job['education'] = infoList[7]
        self.job['salary'] = infoList[5]
        self.job['financeStage'] = infoList[2]
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
    bosszhipinSpider = bosszhipin()
    bosszhipinSpider.get_jobs(keyword, city)