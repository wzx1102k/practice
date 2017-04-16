#! -*-coding:utf-8 -*-

from urllib import request, parse
from bs4 import BeautifulSoup as Bs
import json
from db import MysqlDb
import xlwt
import datetime
import re
import os,sys

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

        #excel init
        self.excel = 'job.xls'
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

    def get_page(self, headers=None, url=None, pn=None, keyword=None, city=None):
        pass

    def get_job(self, page):
        pass


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

    def translate_simple(self, jsData):
        return jsData

    def get_jobs(self, skeyword=None, scity=None):
        for idx in range(1,self.max_pn):
            page = self.get_page(pn=idx, keyword=skeyword, city=scity)
            self.get_job(page)

    def save2excel(self, jsData, excel=None):
        jsDataType= ['positionName', 'companyFullName', 'financeStage', 'education', 'workYear', 'salary', 'companySize', 'createTime', 'url']
        if excel == None:
            excel = self.excel
        self.excel_cnt += 1
        for j, col in enumerate(jsDataType):
            if col == 'url':
                url = 'https://www.lagou.com/jobs/'+str(jsData['positionId'])+'.html'
                self.booksheet.write(self.excel_cnt, j, url)
            else:
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




