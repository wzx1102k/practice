#! -*-coding:utf-8 -*-

from urllib import request, parse
from bs4 import BeautifulSoup as Bs
import json
import xlwt
import datetime
import re
import os,sys

sys.path.append('../')
from spider import spider

class lagou(spider):
    def __init__(self):
        super(lagou, self).__init__()
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Host': 'www.lagou.com',
        'Cookie': 'user_trace_token=20160610174654-4391abd9-2ef0-11e6-a31a-5254005c3644;',
        'Connection': 'keep-alive',
        'Origin': 'http://www.lagou.com'
        }
        self.url = r'http://www.lagou.com/jobs/positionAjax.json'
        self.excel = 'lagou.xls'
        '''with open('config.txt', 'r') as fd:
            self.conf = json.load(fd)
            self._db = MysqlDb(self.conf['user'], self.conf['password'], self.conf['db'], self.conf['host'], int(self.conf['port'])).set_table(self.conf['table'])
            self._db.create('lagou.sql')
            self._db.create('job.sql')'''
        #excel init

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
        if self.pn == 1:
            boo = 'true'
        else:
            boo = 'false'
        _body = parse.urlencode([
            ('first', boo),
            ('pn', self.pn),
            ('kd', self.keyword),
            ('city', self.city)
        ])
        _url = self.url + '?' + _body
        return _url, _body, self.headers, 'POST'

    def get_job(self, _page, _type):
        js = json.loads(_page.decode('utf-8'))
        if js['success'] == False:
            print("获取工作数据失败！！")
            return False
        if js['content']['positionResult']['result'] == []:
            return
        for item in js['content']['positionResult']['result']:
            item['job_url'] = 'https://www.lagou.com/jobs/'+str(item['positionId'])+'.html'
            self.save2excel(item)
            jsData = self.translate_simple(item)
            print("******************************************")
            print(jsData)
                #self._db.insert(jsData)'''

    def translate_simple(self, jsData):
        for item in jsData:
            if jsData[item] == None:
                jsData[item] = 'NULL'
        self.res = {
            'job_id': jsData['positionId'],
            'job_name': jsData['positionName'],
            'education': jsData['education'],
            'company_full_name': jsData['companyFullName'],
            'finance_stage': jsData['financeStage'],
            'create_time': jsData['createTime'],
        }

        self.res['salary_low'], self.res['salary_high'] = self.split_str2int(jsData['salary'], '-')
        self.res['work_year_low'], self.res['work_year_high'] = self.split_str2int(jsData['workYear'], '-')
        self.res['staffs_low'], self.res['staffs_high'] = self.split_str2int(jsData['companySize'], '-')
        return self.res

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
    lagouSpider = lagou()
    lagouSpider.get_jobs(keyword, city)




