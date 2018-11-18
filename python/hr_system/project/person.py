# -*- coding: utf-8 -*- 

import os
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
    onship_list = [
            u"序号", u"入职日期", u"职位", u"姓名", u"婚姻状况", u"性别", \
            u"民族", u"籍贯", u'生日', u"身份证号码", u"居住地址", u"户口所在地", \
            u"联系电话", u"紧急联系人", u"紧急联系电话", u"劳动合同起", u"劳动合同止", \
            u"健康证到期日期", u"工资", u"调薪记录", u"年假休假记录", u"警告记录"]

    offship_list = [
            u"离职日期", u"入职日期", u"职位", u"姓名", u"婚姻状况", u"性别", \
            u"民族", u"籍贯", u"生日", u"身份证号码", u"居住地址", u"户口所在地", \
            u"联系电话", u"紧急联系人", u"紧急联系电话", u"劳动合同起", u"劳动合同止", \
            u"健康证到期日期", u"工资", u"调薪记录", u"年假休假记录", u"警告记录"]

    holiday_list = [
            u"登记日期", u"入职日期", u"部门", u"姓名", u"年假日期", u"年假年份", u"其他假日期", u"备注"]

    hurt_list = [
            u"工伤日期", u"部门", u"姓名", u"性别", u"年龄", u"工伤赔偿费", \
            u"休工伤假天数", u"上班时间", u"工伤原因", u"申报工伤方式", u"备注"]

    reward_list = [
            u"序号", u"姓名", u"部门", u"职务", u"奖惩类别", u"奖惩日期", u"备注"]

    class Info(object):
        def __init__(self, name):
            self.name = name
            self.main = Main()
            self.holiday = Holiday()
            self.hurt = Hurt()
            self.reward = Reward()

    class Main (object):
        def __init__(self):
            self.ctype = []
            self.person_dict = {}
            '''
            self.person_dict = {
            u"序号": 0,
            u"入职日期": 0,
            u"职位": '',
            u"姓名": '',
            u"婚姻状况": '',
            u"性别": '',
            u"民族": '',
            u"籍贯": '',
            u"生日": 0,
            u"身份证号码": '',
            u"居住地址": '',
            u"户口所在地": '',
            u"联系电话": '',
            u"紧急联系人": '',
            u"紧急联系电话": '',
            u"劳动合同起": 0,
            u"劳动合同止": 0,
            u"健康证到期日期": 0,
            u"工资": 0,
            u"调薪记录": [],
            u"年假休假记录": [],
            u"警告记录": [],
            u"离职日期": 0,
            }'''

    class Holiday(object):
        def __init__(self):
            self.holiday_dict = {}
            '''
            u"登记日期": [],
            u"入职日期": 0,
            u"部门": '',
            u"姓名": '',
            u"年假日期": [],
            u"年假年份": [],
            u"其他假日期": [],
            u"备注": [],
            }
            '''

    class Hurt(object):
        def __init__(self):
            self.hurt_dict = {}
            '''
            u"工伤日期": [],
            u"部门": '',
            u"姓名": '',
            u"性别": 0,
            u"年龄": 0,
            u"工伤赔偿费": [],
            u"休工伤假天数": [],
            u"上班时间": [],
            u"工伤原因": [],
            u"申报工伤方式": [],
            u"备注": [],
            }
            '''

    class Reward(object):
        def __init__(self):
            self.reward_dict = {}
            '''
            u"序号": 0,
            u"姓名": '',
            u"部门": '',
            u"职务": 0,
            u"奖惩类别": [],
            u"奖惩日期": [],
            u"备注": [],
            }  
            '''
except:
    print "Unexpected error:", sys.exc_info()
    raw_input('press enter key to exit')            