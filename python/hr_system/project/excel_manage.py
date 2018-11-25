# -*- coding: utf8 -*-
# coding: utf8

import os
import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
    import xlrd
    from xlrd import xldate_as_tuple
    import bisect
    import shutil
    import uniout
    from person import Info
    from datetime import datetime

    excel_type = ['main', 'hurt', 'holiday', 'reward']
    '''
    dict info_dict=--------------
        |-------dict person_dict
                    |-----------list name_list
                           |-------class Info
    '''
    class Manage(object):
        def __init__(self):
            self.path = ''
            self.excel_list = []
            self.info_dict = {}
            #self.person_dict = {}
            self.main_excel = ''
            self.depart = ''
            self.holiday_excel = ''
            self.hurt_excel = ''
            self.reward_excel = ''
        
        def load_main_info(self):
            excel = self.main_excel
            timeChoices = ['--']
            leaveChoices = ['--']
            departChoices = ['--', u'全部']
            with xlrd.open_workbook(excel) as workbook:
                for i in workbook.sheet_names():
                    print(i)
                    if u'离职' not in i:
                        if i not in timeChoices:
                            timeChoices.append(i)
                    else:
                        if i not in leaveChoices:
                            leaveChoices.append(i)
                    self.depart = u''
                    self.info_dict[i] = {}
                    table = workbook.sheet_by_name(i)
                    nrows = table.nrows
                    ncols = table.ncols
                    title = []
                    for j in range(0, nrows):
                        row_data = table.row_values(j)
                        if u"姓名" in row_data:
                            title = row_data
                        elif type(row_data[0]) == unicode and u'部' in row_data[0]:
                            self.depart = row_data[0]
                            if self.depart not in departChoices:
                                departChoices.append(self.depart)
                        elif title != []:
                            self.add_person(title, row_data, 'main', i)
            return timeChoices, leaveChoices, departChoices

        def add_person(self, title, input, excel_type, info_dict_key):
            idx = title.index("姓名")
            name = input[idx]
            if name == None or name == '' or name == u'':
                return
            else:
                if excel_type == 'main':
                    self.add_person_main(title, input, info_dict_key)
        
        def add_person_main(self, title, input, info_dict_key):
            idx = title.index("姓名")
            name = input[idx]
            if name in self.info_dict[info_dict_key]:
                idx1 = title.index("身份证号码")
                id = input[idx1]
                for i in self.info_dict[info_dict_key][name]:
                    if i.main.person_dict[u"身份证号码"] == id:
                        return
                self.info_dict[info_dict_key][name].append(Info(name))
                self.add_info_main(title, input, self.info_dict[info_dict_key][name][-1])
            else:
                self.info_dict[info_dict_key][name] = [Info(name)]
                self.add_info_main(title, input, self.info_dict[info_dict_key][name][-1])

        def add_info_main(self, title, input, info):
            info.main.person_dict['info'] = input
            info.main.person_dict['title'] = title
            info.main.person_dict[u'部门'] = self.depart
            for i in range(0, len(title)):
                info.main.person_dict[title[i]] = input[i]
            if u'入职日期' in info.main.person_dict:
                info.main.person_dict[u'入职日期'] = self.convert_time(info.main.person_dict[u'入职日期'])
            if u'离职日期' in info.main.person_dict:
                info.main.person_dict[u'离职日期'] = self.convert_time(info.main.person_dict[u'离职日期'])
            
            ### 通过身份证计算年龄
            id = info.main.person_dict[u'身份证号码']
            if id != None and id != '' and id != u'' and id != 0 and len(str(id)) == 18:
                birth_year = int(str(id)[6:10])
                now_year = int(datetime.now().year)
                if now_year > birth_year and now_year - birth_year < 100:
                    info.main.person_dict[u'年龄'] = now_year - birth_year

            ### 转换日期和号码格式
            for i in title:
                #print(i)
                idx = title.index(i)
                if input[idx] == None or input[idx] == '':
                    continue
                if '日' in i or '起' in i or '止' in i:
                    info.main.person_dict[i] = self.convert_time(input[idx])
                elif '电话' in i or '工资' in i or '序号' in i:
                    info.main.person_dict[i] = int(input[idx])
                #print(info.main.person_dict[i])
            '''
            for v,k in info.main.person_dict.items():
                print(v)
                print(k)
            '''
        def convert_time(self, input):
            time = xldate_as_tuple(input, 0)
            date = datetime(*time)
            return date.strftime('%Y/%m/%d')

        def check_excel_exist(self, path):
            excel_list = []
            dirs = os.listdir(path)
            for i in dirs:
                type = os.path.splitext(i)[1]
                if type == ".xlsx" or type == ".xls":
                    _path = path + '\\' + i
                    excel_list.append(_path)
            return excel_list

        def sort_excel(self, path):
            search_list = self.check_excel_exist(path)
            if search_list == []:
                return False
            else:
                self.excel_list = search_list
                for excel in search_list:
                    if self.search_excel(excel, u"花名册") == True:
                        self.main_excel = excel
                    elif self.search_excel(excel, u"工伤赔偿费") == True:
                        self.hurt_excel = excel
                    elif self.search_excel(excel, u"年假日期") == True:
                        self.holiday_excel = excel
                    elif self.search_excel(excel, u"奖惩类别") == True:
                        self.reward_excel = excel
            if self.main_excel == None:
                return False
            else:
                return True

        def search_excel(self, excel, excel_type):
            with xlrd.open_workbook(excel) as workbook:
                for i in workbook.sheet_names():
                    table = workbook.sheet_by_name(i)
                    nrows = table.nrows
                    ncols = table.ncols
                    for j in range(0, nrows):
                        row_data = table.row_values(j)
                        for k in row_data:
                            if j<5 and type(k) == unicode and excel_type in k:
                                return True
                            elif j >= 5:
                                return False
            return False

        def load_path(self, path):
            print("花名册:" + self.main_excel)
            print("工伤表:" + self.hurt_excel)
            print("休假表:" + self.holiday_excel)
            print("奖惩表:" + self.reward_excel)
            if self.main_excel != None:
                self.load_main_info()

except:
    print "Unexpected error:", sys.exc_info()
    raw_input('press enter key to exit')
