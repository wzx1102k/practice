#! -*-coding:utf-8 -*-

from urllib import request, parse
from urllib.parse import urlencode
from bs4 import BeautifulSoup as Bs
import json
from db import MysqlDb
import xlwt
import httplib2
import datetime
import re
import os,sys
import pinyin

class spider(object):
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
        self.search_type = "DIRECT"
        #excel init
        self.excel = 'job.xls'
        self.res = {
            'job_id': None,
            'job_name': None,
            'education': None,
            'company_full_name': None,
            'finance_stage': None,
            'create_time': None,
            'salary_low': 0,
            'salary_high': 0,
            'work_year_low': 0,
            'staffs_low': 0,
            'staffs_high': 0,
        }
        self.job_type= ['positionName', 'companyFullName', 'financeStage', 'education', 'workYear', 'salary', 'companySize', 'createTime', 'job_url']
        self.job = {
            'positionName': None,
            'companyFullName': None,
            'financeStage': None,
            'education': None,
            'workYear': None,
            'salary': None,
            'companySize': None,
            'createTime': None,
            'job_url': None,
        }
        self.title = ['职位名称', '公司名称', '融资情况', '教育程度', '工作年限', '薪资水平', '员工人数', '创建时间', '职位网址']
        self.workbook = xlwt.Workbook(encoding="utf-8")
        self.booksheet = self.workbook.add_sheet('job', cell_overwrite_ok=True)
        self.booksheet.col(0).width = 256 * 30
        self.booksheet.col(1).width = 256 * 30
        self.booksheet.col(2).width = 256 * 15
        self.booksheet.col(7).width = 256 * 18
        self.booksheet.col(8).width = 256 * 30
        self.excel_cnt = 0
        for j, col in enumerate(self.title):
                self.booksheet.write(self.excel_cnt, j, col)
        self.workbook.save(self.excel)

    def set_url_info(self, _headers=None, _url=None, _pn=None, _keyword=None, _city=None):
        _body = ''
        _type = ''
        return _url, _body, _headers, _type

    def get_job(self, _page, _type):
        pass

    def http_get_header(self, url=None):
        if url == None:
            return None
        else:
            h = httplib2.Http(".cache")
            resp_headers, content = h.request(url, "GET")
            return resp_headers

    def get_page(self, _url=None, _body=None, _type="GET",  _header=None):
        if _url == None:
            return None
        else:
            httplib2.debuglevel = 0
            h = httplib2.Http(".cache")
            if _type == "GET":
                response, content = h.request(uri=_url, method=_type)
            else:
                response, content = h.request(uri=_url, method=_type, body=_body, headers=_header)
            '''
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print(len(content))
            print(response.status)
            print(response.fromcache)
            print(response)
            print(content)
            print("################################")'''
            return content

    def to_city(self, var_str, type):
        if isinstance(var_str, str):
            if var_str == 'None':
                return ''
            else:
                stringHead = ''
                stringFull = ''
                for single in var_str:
                    stringFull += pinyin.get(single, format='strip', delimiter="")
                    stringHead += pinyin.get(single, format='strip', delimiter="")[0]
                if type == "FULL":
                    return stringFull
                elif type == "HEAD":
                    return stringHead
        else:
            return ''

    def split_str2int(self, raw, splitChar):
        if raw == None:
            return(0, 0)
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

    def split_str(self, target, splitStart, splitEnd, eStart=0, eEnd=0):
        stringTarget = str(target)
        if splitStart != '':
            posStart = stringTarget.find(splitStart)
        else:
            posStart = 0
        if splitEnd != '':
            posEnd = stringTarget[posStart:].find(splitEnd)
        else:
            posEnd = -1
        if posStart == -1 or posEnd == -1:
            return None
        else:
            if eEnd != 0:
                posEnd = posEnd + len(splitEnd) + posStart
            else:
                posEnd = posEnd + posStart
            if eStart == 0:
                posStart = posStart + len(splitStart)
            return stringTarget[posStart:posEnd]

    def translate_simple(self, jsData):
        return jsData

    def get_jobs(self, skeyword=None, scity=None):
        for idx in range(0,self.max_pn):
            url, body, header, type = self.set_url_info(_pn=idx, _keyword=skeyword, _city=scity)
            page = self.get_page(_url=url, _body=body, _header=header, _type=type)
            self.get_job(_page=page, _type=self.search_type)

    def save2excel(self, jsData, excel=None):
        if excel == None:
            excel = self.excel
        self.excel_cnt += 1
        for j, col in enumerate(self.job_type):
            self.booksheet.write(self.excel_cnt, j, jsData[col])
        self.workbook.save(excel)


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
    demoSpider = spider()
    demoSpider.get_jobs(keyword, city)




