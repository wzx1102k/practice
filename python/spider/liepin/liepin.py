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
        print(soup)
        return soup
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
        infoList = []
        for info in jsData:
            splitString = self.split_str(info, 'https://www.liepin.com/zhaopin/', 'htm', eStart=1, eEnd=1)
            if splitString != None:
                infoList.append(splitString)
            elif str(info).find('xiaoyuan') != -1:
                return jsData
            splitString = self.split_str(info, '_blank\">', '</a>', eStart=0, eEnd=0)
            if splitString != None:
                splitString = splitString.replace('</b>', '')
                splitString = splitString.replace('<b>', '')
                infoList.append(splitString)
            splitString = self.split_str(info, '公司规模：', '人', eStart=0, eEnd=1)
            if splitString != None:
                infoList.append(splitString)
                splitString = self.split_str(info, '经验：', '年', eStart=0, eEnd=1)
                if splitString != None:
                    infoList.append(splitString)
                else:
                    infoList.append('')
                splitString = self.split_str(info, '学历：', '</span>', eStart=0, eEnd=0)
                if splitString != None:
                    infoList.append(splitString)
                else:
                    infoList.append('')
                splitString = self.split_str(info, '职位月薪：', '/月', eStart=0, eEnd=1)
                if splitString != None:
                    infoList.append(splitString)
                else:
                    infoList.append('')
                print(infoList)
                self.job['job_url'] = infoList[0]
                self.job['positionName'] = infoList[1]
                self.job['companyFullName'] = infoList[2]
                self.job['companySize'] = infoList[3]
                self.job['workYear'] = infoList[4]
                self.job['education'] = infoList[5]
                self.job['salary'] = infoList[6]
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





