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
        self.max_pn = 5
        #self.max_pn = 1
        self.headers = {
            'Server': 'Apache',
            'Set-Cookie': 'guid=14946128161423380040; path=/; domain=.51job.com; httponly',
            'Set-Cookie': 'usign=DTRTOQZlAipcPF01Uj9dcAMzByhVZwJhB30CYV1jAjtcYFs1AmkAMlA1WjNSN1BlAjkCNgN5VUIBNF19CnRRZQ%3D%3D; path=/; httponly',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'Location': 'http://m.51job.com/search/jobsearch.php',
            'Cache-control': 'no-cache, no-store',
            'Pragma' : 'no-cache',
            'Content-Type': 'text/html',
        }
        self.excel = 'job51.xls'
        self.url = r'http://search.51job.com/jobsearch/search_result.php'

    def set_url_info(self, _headers=None, _url=None, _pn=None, _keyword=None, _city=None):
        if _headers != None:
            self.headers = _headers
        if _pn != None:
            self.pn = _pn
        if _keyword != None:
            self.keyword = _keyword
        if _city != None:
            self.city
        if _url != None:
            self.url = _url
        citycode = {
            "深圳": "040000",
            "上海": "020000",
            "北京": "010000",
            "广州": "030200",
            "杭州": "080200"
        }
        if self.city not in citycode.keys():
            print("Select city is not support, change to 深圳")
            self.city = "深圳"
        _body = parse.urlencode([
            ('jobarea', citycode[self.city]),
            ('keyword', self.keyword),
            ('keywordtype', 2),
            ('startpage', self.pn),
        ])
        u = self.url + '?' + _body
        return u, _body, self.headers, 'GET'

    def get_job(self, _page, _type):
        soup = Bs(_page, "lxml")
        __cityname = self.to_city(self.city, "FULL")
        for a in soup.find_all('a'):
            aList = a.attrs
            if 'href' in aList.keys():
                if "http://m.51job.com/search/jobdetail.php" in (a['href']):
                    self.job['job_url'] = a['href']
                    #print(a['href'])
                    data = parse.urlencode([
                        ('s', '01'),
                        ('t', '0'),
                    ])
                    url = self.job['job_url']+'&'+data
                    print(url)
                    req = request.Request(url, headers=self.headers)
                    page = request.urlopen(req, data=data.encode('utf-8'), timeout=10).read()
                    #page = self.get_page(_url=self.job['job_url']+'&'+data, _type='GET')
                    soup = Bs(page, "lxml")
                    #print(soup)
                    self.job['positionName'] = soup.find('p', {"class": "xtit"}).string
                    self.job['companyFullName'] = soup.find('a', {"class": "xqa"}).string
                    t = soup.find_all('label')
                    for t_temp in t:
                        tSingle = str(t_temp)
                        if "性质" in tSingle:
                            self.job['financeStage'] = self.split_str(tSingle, '</span>', '</label>', eStart=0, eEnd=0)
                        elif "薪资" in tSingle:
                            self.job['salary'] = self.split_str(tSingle, '</span>', '</label>', eStart=0, eEnd=0)
                        elif "规模" in tSingle:
                            self.job['companySize'] = self.split_str(tSingle, '</span>', '</label>', eStart=0, eEnd=0)
                        elif "招聘" in tSingle:
                            tempString = self.split_str(tSingle, '|', '</', eStart=0, eEnd=1).replace(' ', '')
                            self.job['education'] = self.split_str(tempString, '', '|', eStart=1, eEnd=0)
                            tempString = self.split_str(tempString, '|', '</', eStart=0, eEnd=0)
                            tempString1 = self.split_str(tempString, '', '|', eStart=1, eEnd=0)
                            if tempString1 == None:
                                self.job['workYear'] = tempString
                            else:
                                self.job['workYear'] = tempString1
                    print("*********************************************")
                    print(self.job)
                    self.save2excel(self.job)


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



