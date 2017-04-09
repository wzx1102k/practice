#! -*-coding:utf-8 -*-

from urllib import request, parse
from bs4 import BeautifulSoup as Bs
import json
from db import MysqlDb
import datetime
import re

class lagou(object):
    def __init__(self):
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Host': 'www.lagou.com',
        'Cookie': 'LGMOID=20160610174652-B505B4662B5ADF9B09C3C257938303AC; user_trace_token=20160610174654-4391abd9-2ef0-11e6-a31a-5254005c3644;',
        'Connection': 'keep-alive',
        'Origin': 'http://www.lagou.com'
        }
        self.pn = 1
        self.max_pn = 30
        self.keyword = "图像"
        #city: 深圳
        self.city = "深圳"
        self.url = r'http://www.lagou.com/jobs/positionAjax.json?city=' + parse.quote(self.city)
        with open('config.txt', 'r') as fd:
            self.conf = json.load(fd)
            self._db = MysqlDb(self.conf['user'], self.conf['password'], self.conf['db'], self.conf['host'], int(self.conf['port'])).set_table(self.conf['table'])
            self._db.create('lagou.sql')
            self._db.create('job.sql')
    def get_page(self, headers=None, url=None, pn=None, keyword=None, city=None):
        if headers == None:
            headers = self.headers
        if url == None:
            if city !=None:
                self.city = city
                self.url = r'http://www.lagou.com/jobs/positionAjax.json?city=' + parse.quote(city)
            url = self.url
        if pn == None:
            pn = self.pn
        if keyword == None:
            keyword = self.keyword
        if pn == 1:
            boo = 'true'
        else:
            boo = 'false'
        data = parse.urlencode([
            ('first', boo),
            ('pn', pn),
            ('kd', keyword)
        ])
        req = request.Request(url, headers=headers)
        page = request.urlopen(req, data=data.encode('utf-8')).read()
        page = page.decode('utf-8')
        return page

    def get_job(self, page):
        js = json.loads(page)
        if js['success'] == False:
            print("获取工作数据失败！！")
            return False
        for item in js['content']['positionResult']['result']:
            if self.conf['table'] == 'simplejob':
                self._db.insert(self.translate_simple(item))
            elif self.conf['table'] == 'job':
                self._db.insert(self.translate(item))


    def split_str2int(self, raw, splitChar):
        if splitChar in raw:
            low, high = raw.split(splitChar)
            low = int(re.sub("\D", "", low))
            high = int(re.sub("\D", "", high))
        else:
            if re.sub("\D", "", raw) == '':
                low = 0
                high = 0
            else:
                low = int(re.sub("\D", "", raw))
                high = low
        return (low, high)

    def translate(self, jsData):
        res = {
            'job_id': jsData['positionId'],
            'job_name': jsData['positionName'],
            'education': jsData['education'],
            'company_id': jsData['companyId'],
            'company_full_name': jsData['companyFullName'],
            'company_short_name': jsData['companyShortName'],
            'industry_field': jsData['industryField'],
            'finance_stage': jsData['financeStage'],
            'job_nature': jsData['jobNature'],
            'city': jsData['city'],
            'plus': 1 if jsData['plus'] == '是' else 0,
            'create_time': jsData['createTime'],
            'advantage': jsData['positionAdvantage']
        }
        if(jsData['companyLabelList'] != None):
            res['company_labels'] = ','.join(jsData['companyLabelList'])
        res['salary_low'], res['salary_high'] = self.split_str2int(jsData['salary'], '-')
        res['work_year_low'], res['work_year_high'] = self.split_str2int(jsData['workYear'], '-')
        res['staffs_low'], res['staffs_high'] = self.split_str2int(jsData['companySize'], '-')
        return res

    def translate_simple(self, jsData):
        res = {
            'job_id': jsData['positionId'],
            'job_name': jsData['positionName'],
            'education': jsData['education'],
            'company_full_name': jsData['companyFullName'],
            'finance_stage': jsData['financeStage'],
            'create_time': jsData['createTime'],
        }
        res['salary_low'], res['salary_high'] = self.split_str2int(jsData['salary'], '-')
        res['work_year_low'], res['work_year_high'] = self.split_str2int(jsData['workYear'], '-')
        res['staffs_low'], res['staffs_high'] = self.split_str2int(jsData['companySize'], '-')
        return res

    def get_jobs(self, scity='深圳'):
        for idx in range(1,8):
            page = self.get_page(pn=idx, city=scity)
            self.get_job(page)

if __name__ == '__main__':
    lagouSpider = lagou()
    lagouSpider.get_jobs()




