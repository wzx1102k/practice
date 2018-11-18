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
            if self.input.query_time == "--" or self.input.query_time == u'全部':
                return False, u'查询全部时间'
            elif self.input.status == u'离职':
                for i in info.keys():
                    if u'离职' in i:
                        flag, msg = self.single_check(info[i])
                        return flag, msg
            elif self.input.status == u'入职':
                pass
            elif info[self.input.query_time] != {}:
                if len(self.input.name) > 1:   ## 通过名字查询
                    flag, msg = self.single_check_by_name(info[self.input.query_time])
                else:
                    flag, msg = self.single_check_by_condition(info[self.input.query_time])           
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
            count = 0
            sum = 0
            sum_count = 0
            result_str = ''
            key_str = ''
            for name in input.keys():
                for i in input[name]:
                    if self.input.age_max >= self.input.age_min:
                        if u'年龄' not in i.main.person_dict.keys() or i.main.person_dict[u'年龄'] < self.input.age_min or i.main.person_dict[u'年龄'] > self.input.age_max:
                            continue                
                    if self.input.gender != '--':
                        if u'性别' not in i.main.person_dict.keys() or i.main.person_dict[u'性别'] != self.input.gender:
                            continue
                    if self.input.depart != '--':
                        if u'部门' not in i.main.person_dict.keys() or i.main.person_dict[u'部门'] != self.input.depart:
                            continue
                    search_list.append(i)
        
            for i in search_list:            
                count += 1
                for key in i.main.person_dict['title']:
                    key_str += key + ': ' + str(i.main.person_dict[key]) + ' '
                key_str += '\r\n'
                salary = i.main.person_dict[u"工资"]
                if salary != None and salary != '':
                    sum += salary
                    sum_count += 1
            
            sum /= sum_count
            #print(sum)
            #print(count)
            if self.output.salary == True:
                result_str += u'平均薪资: \r\n' + str(sum) + '\r\n'
            if self.output.num == True:
                result_str += u'人数: \r\n' + str(count) + '\r\n'
            if self.output.info == True:
                result_str += u'信息: \r\n' + key_str
            #print(result_str)
            return True, result_str


    class Input(object):
        def __init__(self):
            self.name = u'空'
            self.gender = '--'
            self.age_min = 20
            self.age_max = 60
            self.query_time = '--'
            self.depart = '--'
            self.status = '--'

    class Output(object):
        def __init__(self):
            self.salary = False
            self.num = False
            self.info = False
except:
    print "Unexpected error:", sys.exc_info()
    raw_input('press enter key to exit')