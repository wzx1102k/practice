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

class job51(spider):
    def __init__(self):
        super(job51, self).__init__()
        self.pn = 0
        self.max_pn = 1
        #self.max_pn = 1
        self.headers = {
            'Server': 'Apache',
            'Set-Cookie': 'guid=14941209152493340079; expires=Tue, 16-Mar-2027 01:35:15 GMT; path=/; domain=.51job.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'Content-Type': 'text/html',
        }
        self.url = r'http://search.51job.com/jobsearch/search_result.php'

    def set_url_info(self, _headers=None, _url=None, _pn=None, _keyword=None, _city=None):
        if _headers == None:
            _headers = self.headers
        if _pn == None:
            _pn = self.pn
        if _keyword == None:
            _keyword = self.keyword
        if _city == None:
            _city = self.city
        else:
            self.city = _city
        if _url == None:
            _url = self.url
        citycode = {
            "深圳": "040000",
            "上海": "020000",
            "北京": "010000",
            "广州": "030200",
            "杭州": "080200"
        }
        if _city not in citycode.keys():
            print("Select city is not support, change to 深圳")
            _city = "深圳"
        para = parse.urlencode([
            ('fromJs', 1),
            ('jobarea', citycode[_city]),
            ('keyword', _keyword),
            ('keywordtype', 2),
            ('lang', 'c'),
            ('stype', 2),
            ('postchannel', '0000'),
            ('fromType', '1'),
            ('startpage', _pn),
        ])
        u = _url + '?' + para
        #return _url, para, 'POST'
        return u, '', 'GET'

    def get_job(self, page):
        __cityname = self.to_city(self.city, "FULL")
        for a in page.find_all('a'):
            aList = a.attrs
            if 'href' in aList.keys():
                if "http://jobs.51job.com/" + __cityname in (a['href']):
                    print(a['href'])
                    url = r'http://jobs.51job.com/shenzhen-lhxq/89018374.html'
                    data = parse.urlencode([
                        ('s', '01'),
                        ('t', '0'),
                    ])
                    u = url + '?' + data
                    '''self.headers = self.get_header(url)
                    print(self.headers)
                    req = request.Request(u, headers=self.headers)
                    page1 =request.urlopen(req).read()'''
                    #page1 = self.get_page(_url=u)
                    #print(page1)
                    break
            #if 'href' in a.attrs():
            #    print(a['href'])

        '''
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
            self.translate_simple(info)'''

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
    job51Spider = job51()
    job51Spider.get_jobs(keyword, city)



