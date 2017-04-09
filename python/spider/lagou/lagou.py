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
            conf = json.load(fd)
            self._db = MysqlDb(conf['user'], conf['password'], conf['db'], conf['host'], int(conf['port'])).set_table(conf['table'])
            self._db.create('lagou.sql')
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
        print(js)
        for item in js['content']['positionResult']['result']:
            self._db.insert(self.translate(item))
            #print(item)
            #print(item['positionId'])

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
        print(jsData['companyLabelList'])
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

    def get_pages(self):
        pass


if __name__ == '__main__':
    lagouSpider = lagou()
    page = lagouSpider.get_page(pn=4, city="深圳")
    lagouSpider.get_job(page)
    #print(page)



