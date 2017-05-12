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