# -*- coding: utf8 -*-
# coding: utf8

import os
import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
    import shutil
    #from utils import CCode
    from excel_manage import Manage

    class Query(object):
        def __init__(self):
            self.input = Input()
            self.output = Output()
            #self.ccode = CCode()
        
        def check(self, info):
            if u'--' in self.input.query_time:
                return False, u'查询全部时间'
            elif len(self.input.query_time) > 1:
                return False, u'多项查询'
            else:
                if info[self.input.query_time[0]] != {}:
                    if len(self.input.name) > 1:   ## 通过名字查询
                        flag, msg = self.single_check_by_name(info[self.input.query_time[0]])
                    else:
                        flag, msg = self.single_check_by_condition(info[self.input.query_time[0]])           
                    return flag, msg
                else:
                    return False, u'列表为空'
        
        def single_check_by_name(self, input):
            if self.input.name in input.keys():
                for i in input[self.input.name]:
                    result_str = ''
                    for key in i.main.person_dict['title']:
                        result_str += key + ': ' + str(i.main.person_dict[key]) + ' '
                    return True, result_str
                    #return True, self.ccode.str(result_str)
            return False, u'名字未搜索到'
        
        def single_check_by_condition(self, input):
            search_list = []
            man_count = 0
            woman_count = 0
            count = 0
            sum = 0
            average = 0
            sum_count = 0
            result_str = '\r\n'
            key_str = ''
            for name in input.keys():
                for i in input[name]:
                    if self.input.age_max >= self.input.age_min:
                        if u'年龄' not in i.main.person_dict.keys() or i.main.person_dict[u'年龄'] < self.input.age_min or i.main.person_dict[u'年龄'] > self.input.age_max:
                            continue                
                    if self.input.gender != '--':
                        if u'性别' not in i.main.person_dict.keys() or i.main.person_dict[u'性别'] != self.input.gender:
                            continue
                    if self.input.depart != '--' and self.input.depart != u'全部':
                        if u'部门' not in i.main.person_dict.keys() or i.main.person_dict[u'部门'] != self.input.depart:
                            continue
                    if self.input.status == u'入职' or self.input.status == u'离职':
                        id = u'入职日期'
                        if self.input.status == u'离职':
                            id = u'离职日期'
                            
                        real_year = int(i.main.person_dict[id][0:4])
                        real_month = int(i.main.person_dict[id][5:7])
                        #print(i.main.person_dict[id])
                        #print(real_year)
                        #print(real_month)
                        if self.input.start_time != '':
                            start_year = int(self.input.start_time[0:4])
                            start_month = int(self.input.start_time[5:7])
                            if real_year < start_year:
                                continue
                            elif real_year == start_year:
                                if real_month < start_month:
                                    continue
                        if self.input.end_time != '':
                            end_year = int(self.input.end_time[0:4])
                            end_month = int(self.input.end_time[5:7])
                            if real_year > end_year:
                                continue
                            elif real_year == end_year:
                                if real_month > end_month:
                                    continue
                    search_list.append(i)
        
            for i in search_list:            
                count += 1
                if i.main.person_dict[u"性别"] == u'男':
                    man_count += 1
                else:
                    woman_count += 1
                
                for key in i.main.person_dict['title']:
                    key_str += key + ': ' + str(i.main.person_dict[key]) + ' '
                key_str += '\r\n'
                salary = i.main.person_dict[u"工资"]
                if salary != None and salary != '':
                    sum += salary
                    sum_count += 1
            if sum_count == 0:
                average = 0
            else:
                average = sum / sum_count
            #print(sum)
            #print(count)
            if self.output.salary_total == True:
                result_str += u'薪资总额: \r\n' + str(sum) + '\r\n'
            if self.output.salary == True:
                result_str += u'平均薪资: \r\n' + str(average) + '\r\n'
            if self.output.num == True:
                result_str += u'人数: ' + str(count) + ' '
                result_str += u'男: ' + str(man_count) + ' '
                result_str += u'女: ' + str(woman_count) + ' '
                if woman_count == 0:
                    result_str += u'男女比例: 全男\r\n'
                elif man_count == 0:
                    result_str += u'男女比例: 全女\r\n'
                else:
                    result_str += u'男女比例: ' + str(format(float(man_count)/float(woman_count), '.2f')) + ':1\r\n'
            if self.output.info == True:
                result_str += u'信息: \r\n' + key_str
            result_str += '\r\n'
            #print(result_str)
            return True, result_str


    class Input(object):
        def __init__(self):
            self.name = u'空'
            self.gender = '--'
            self.age_min = 20
            self.age_max = 60
            self.start_time = ''
            self.end_time = ''
            self.query_time = []
            self.depart = '--'
            self.status = '--'

    class Output(object):
        def __init__(self):
            self.salary = False
            self.num = False
            self.info = False
            self.salary_total = False
except:
    print "Unexpected error:", sys.exc_info()
    raw_input('press enter key to exit')