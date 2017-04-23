#! -*-coding:utf-8 -*-
from urllib import request, parse
from bs4 import BeautifulSoup as Bs
import json
#from db import MysqlDb
import xlwt
import datetime
import re
import os,sys

sys.path.append('../')
from db import MysqlDb
from spider import spider

class zhilian(spider):
    def __init__(self):
        super(zhilian, self).__init__()
        self.headers = {
            'Accept-Encoding': 'deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'cache-control': 'no-cache',
        }
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
        info = []
        for td in soup.find_all('td'):
            tdList = td.attrs
            if 'class' in tdList.keys():
                if tdList['class'] == ['zwmc'] or tdList['class'] == ['gsmc']:
                    info.append(td.find_all('a'))
            for li in td.find_all('li'):
                liList = li.attrs
                if liList['class'] == ['newlist_deatil_two']:
                    info.append(li)
                    self.translate_simple(info)
                    info = []

    def translate_simple(self, jsData):
        infoList = []
        #print(jsData)
        for info in jsData:
            splitString = self.split_str(info, 'http://jobs.zhaopin.com/', 'htm', eStart=1, eEnd=1)
            if splitString != None:
                infoList.append(splitString)
            elif str(info).find('xiaoyuan') != -1:
                return jsData
            posStart = str(info).find('_blank\">')
            splitString = self.split_str(info, '_blank\">', '</a>', eStart=0, eEnd=0)
            if splitString != None:
                print(splitString)
                splitString = splitString.replace('</b>', '')
                splitString = splitString.replace('<b>', '')
                infoList.append(splitString)
            splitString = self.split_str(info, '公司规模：', '人', eStart=0, eEnd=1)
            if splitString != None:
                infoList.append(splitString)
            splitString = self.split_str(info, '经验：', '年', eStart=0, eEnd=1)
            if splitString != None:
                infoList.append(splitString)
            splitString = self.split_str(info, '学历：', '职位月薪', eStart=0, eEnd=0)
            if splitString != None:
                splitString1 = self.split_str(splitString, '', '</span>', eStart=0, eEnd=0)
                print(splitString1)
                if splitString1 != None:
                    infoList.append(splitString1)
                else:
                    infoList.append(splitString)
            splitString = self.split_str(info, '职位月薪：', '/月', eStart=0, eEnd=1)
            if splitString != None:
                infoList.append(splitString)
        print(infoList)
        return jsData


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





