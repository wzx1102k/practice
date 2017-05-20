from urllib import request, parse
from urllib.parse import urlencode
from bs4 import BeautifulSoup as Bs
import json
import xlwt
import xlrd
from xlutils.copy import copy
import httplib2
import datetime
import re
import os,sys
import pinyin
from os import listdir
import csv


sys.path.append('./lagou')
sys.path.append('./zhilian')
sys.path.append('./job51')
sys.path.append('./liepin')
sys.path.append('./bosszhipin')
from lagou import lagou
from zhilian import zhilian
from job51 import job51
from liepin import liepin
from bosszhipin import bosszhipin

def mergeExcel(path, keyword):
    print("**************************************")
    print("Start to merge excel...")
    print("**************************************")
    list = os.listdir("./")
    title = ['职位名称', '公司名称', '融资情况', '教育程度', '工作年限', '薪资水平', '员工人数', '创建时间', '职位网址']
    workbook = xlwt.Workbook(encoding="utf-8")
    booksheet = workbook.add_sheet('job', cell_overwrite_ok=True)
    booksheet.col(0).width = 256 * 30
    booksheet.col(1).width = 256 * 30
    booksheet.col(2).width = 256 * 15
    booksheet.col(7).width = 256 * 18
    booksheet.col(8).width = 256 * 30
    excel_cnt = 0
    for j, col in enumerate(title):
        booksheet.write(excel_cnt, j, col)
    workbook.save('job.xls')
    job_csv = 'job.csv'
    if os.path.isfile(job_csv) == True:
        os.remove(job_csv)
    csv_file = open(job_csv, "w")
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(title)
    for xls in list:
        if 'xls' in xls:
            rb = xlrd.open_workbook(xls, formatting_info=True)
            table = rb.sheets()[0]
            nrows = table.nrows  # 行数
            for rownum in range(1, nrows):
                row = table.row_values(rownum)
                if keyword == "图像":
                    if '图像' in row[0] \
                        or '算法' in row[0] \
                        or '视觉' in row[0] \
                        or '机器' in row[0] \
                        or '学习' in row[0] \
                        or '智能' in row[0]:
                        excel_cnt += 1
                        for j in range(0, len(title)):
                            booksheet.write(excel_cnt, j, row[j])
                        csv_writer.writerow(row)
                else:
                    excel_cnt += 1
                    for j in range(0, len(title)):
                        booksheet.write(excel_cnt, j, row[j])
                    csv_writer.writerow(row)
    workbook.save('job.xls')
    csv_file.close()

if __name__ == '__main__':
    cnt = len(sys.argv)
    if cnt == 2:
        keyword = sys.argv[1]
        city = None
        spider_type = None
    elif cnt == 3:
        keyword = sys.argv[1]
        city = sys.argv[2]
        spider_type = None
    elif cnt == 4:
        keyword = sys.argv[1]
        city = sys.argv[2]
        spider_type = sys.argv[3]
    else:
        keyword = None
        city = None
        spider_type = None
    if spider_type == None:
        lagouSpider = lagou()
        zhilianSpider = zhilian()
        liepinSpider = liepin()
        bosszhipinSpider = bosszhipin()
        job51Spider = job51()
        lagouSpider.get_jobs(keyword, city)
        zhilianSpider.get_jobs(keyword, city)
        liepinSpider.get_jobs(keyword, city)
        bosszhipinSpider.get_jobs(keyword, city)
        job51Spider.get_jobs(keyword, city)
    mergeExcel("./", keyword)
