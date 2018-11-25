# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import os
import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
    import wx
    import wx.xrc
    import logging 
    from excel_manage import Manage
    from query import Query

    logger = logging.getLogger(__name__)

    class WxTextCtrlHandler(logging.Handler): 
        def __init__(self, ctrl): 
            logging.Handler.__init__(self) 
            self.ctrl = ctrl 

        def emit(self, record): 
            s = self.format(record) + '\n' 
            wx.CallAfter(self.ctrl.WriteText, s) 

    LEVELS = [ 
        logging.DEBUG, 
        logging.INFO, 
        logging.WARNING, 
        logging.ERROR, 
        logging.CRITICAL 
    ] 
###########################################################################
## Class MyFrame1
###########################################################################

    class MyFrame1 ( wx.Frame ):
        def __init__( self, parent ):
            wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1132,673 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
            
            self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
            
            bSizer1 = wx.BoxSizer( wx.VERTICAL )
            
            bSizer1.SetMinSize( wx.Size( 800,600 ) ) 
            self.header = wx.StaticText( self, wx.ID_ANY, u"人事管理系统", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
            self.header.Wrap( -1 )
            self.header.SetFont( wx.Font( 24, 70, 90, 92, False, "宋体" ) )
            
            bSizer1.Add( self.header, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL, 5 )
            
            self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"请确保所有excel未被打开!!", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_staticText3.Wrap( -1 )
            self.m_staticText3.SetFont( wx.Font( 12, 70, 90, 92, True, "宋体" ) )
            
            bSizer1.Add( self.m_staticText3, 0, 0, 5 )
            bSizer8 = wx.BoxSizer( wx.VERTICAL )
            bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
            
            bSizer4.SetMinSize( wx.Size( -1,10 ) ) 
            self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"花名册路径：", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_staticText2.Wrap( -1 )
            self.m_staticText2.SetFont( wx.Font( 16, 70, 90, 90, False, "宋体" ) )
            
            bSizer4.Add( self.m_staticText2, 0, wx.ALL|wx.FIXED_MINSIZE, 5 )
            
            self.m_dirPicker1 = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.Size( 600,50 ), wx.DIRP_DEFAULT_STYLE )
            self.m_dirPicker1.Bind( wx.EVT_DIRPICKER_CHANGED, self.m_dirPicker1OnDirChanged )
            bSizer4.Add( self.m_dirPicker1, 0, wx.ALL|wx.FIXED_MINSIZE|wx.SHAPED, 5 )
            
            
            bSizer8.Add( bSizer4, 1, wx.ALIGN_TOP|wx.EXPAND|wx.FIXED_MINSIZE|wx.TOP, 1 )
            
            
            bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
            
            self.name = wx.StaticText( self, wx.ID_ANY, u"姓名:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.name.Wrap( -1 )
            bSizer6.Add( self.name, 0, wx.ALL, 5 )
            
            self.m_name = wx.TextCtrl( self, wx.ID_ANY, u"空", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer6.Add( self.m_name, 0, wx.ALL, 5 )
            
            self.gender = wx.StaticText( self, wx.ID_ANY, u"性别:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.gender.Wrap( -1 )
            bSizer6.Add( self.gender, 0, wx.ALL, 5 )
            
            m_genderChoices = [ u"男", u"女", u"--" ]
            self.m_gender = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_genderChoices, 0 )
            self.m_gender.SetSelection( 2 )
            bSizer6.Add( self.m_gender, 0, wx.ALL, 5 )
            
            self.age = wx.StaticText( self, wx.ID_ANY, u"年龄段:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.age.Wrap( -1 )
            bSizer6.Add( self.age, 0, wx.ALL, 5 )
            
            self.m_age_min = wx.TextCtrl( self, wx.ID_ANY, u"20", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer6.Add( self.m_age_min, 0, wx.ALL, 5 )
            
            self.internal = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.internal.Wrap( -1 )
            bSizer6.Add( self.internal, 0, wx.ALL, 5 )
            
            self.m_age_max = wx.TextCtrl( self, wx.ID_ANY, u"60", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer6.Add( self.m_age_max, 0, wx.ALL, 5 )
            
            bSizer8.Add( bSizer6, 1, wx.EXPAND, 1 )
            bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

            self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"花名册选择:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_staticText11.Wrap( -1 )
            self.m_staticText11.SetMinSize( wx.Size( 70,-1 ) )
            bSizer7.Add( self.m_staticText11, 0, wx.ALL, 5 )
            
        
            m_tableChoices = [ u"--" ]
            self.m_listBox1 = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_tableChoices, wx.LB_MULTIPLE )
            self.m_listBox1.SetMinSize( wx.Size( 80,-1 ) )
            bSizer7.Add( self.m_listBox1, 0, wx.ALL, 5 )

            self.depart = wx.StaticText( self, wx.ID_ANY, u"部门:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.depart.Wrap( -1 )
            bSizer7.Add( self.depart, 0, wx.ALL, 5 )
            
            m_departChoices = [ u"--", u"行政部", u"客户部", u"营业部", u"酒吧", u"服务部", u"管家部", u"中厨部", u"烧味部", u"点心部" ]
            self.m_depart = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_departChoices, 0 )
            self.m_depart.SetSelection( 0 )
            bSizer7.Add( self.m_depart, 0, wx.ALL, 5 )
            
            self.status = wx.StaticText( self, wx.ID_ANY, u"状态", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.status.Wrap( -1 )
            bSizer7.Add( self.status, 0, wx.ALL, 5 )
            
            m_statusChoices = [ u"--", u"在职", u"入职", u"离职" ]
            self.m_status = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_statusChoices, 0 )
            self.m_status.SetSelection( 0 )
            bSizer7.Add( self.m_status, 0, wx.ALL, 5 )
                  
            self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"时间段:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_staticText13.Wrap( -1 )
            bSizer7.Add( self.m_staticText13, 0, wx.ALL, 5 )
            
            self.m_time_start = wx.TextCtrl( self, wx.ID_ANY, u"2018/01", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer7.Add( self.m_time_start, 0, wx.ALL, 5 )
            
            self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_staticText14.Wrap( -1 )
            bSizer7.Add( self.m_staticText14, 0, wx.ALL, 5 )
            
            self.m_time_end = wx.TextCtrl( self, wx.ID_ANY, u"2018/09", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer7.Add( self.m_time_end, 0, wx.ALL, 5 )
            bSizer8.Add( bSizer7, 1, wx.EXPAND, 1 )
            
            bSizer51 = wx.BoxSizer( wx.HORIZONTAL )
            
            self.m_checkBox4 = wx.CheckBox( self, wx.ID_ANY, u"薪资总额", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer51.Add( self.m_checkBox4, 0, wx.ALL, 5 )
            self.m_checkBox1 = wx.CheckBox( self, wx.ID_ANY, u"平均薪资", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer51.Add( self.m_checkBox1, 0, wx.ALL, 5 )
            
            self.m_checkBox2 = wx.CheckBox( self, wx.ID_ANY, u"人数", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer51.Add( self.m_checkBox2, 0, wx.ALL, 5 )
            
            self.m_checkBox3 = wx.CheckBox( self, wx.ID_ANY, u"详细信息", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer51.Add( self.m_checkBox3, 0, wx.ALL, 5 )
            
            self.query = wx.Button( self, wx.ID_ANY, u"查询", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer51.Add( self.query, 0, wx.ALL, 5 )
            
            self.m_button3 = wx.Button( self, wx.ID_ANY, u"清除输出", wx.DefaultPosition, wx.DefaultSize, 0 )
            bSizer51.Add( self.m_button3, 0, wx.ALL, 5 )
            bSizer8.Add( bSizer51, 1, wx.EXPAND, 1 )
            
            #self.log = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY )
            self.log = wx.TextCtrl(self, id=wx.ID_ANY, value=wx.EmptyString, pos=(-1, -1), size=(250, 150), style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)
            bSizer8.Add( self.log, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5 )
            
            
            bSizer1.Add( bSizer8, 1, wx.EXPAND, 1 )
            self.SetSizer( bSizer1 )
            self.Layout()
            self.m_menubar1 = wx.MenuBar( 0 )
            self.m_menu1 = wx.Menu()
            self.m_menubar1.Append( self.m_menu1, u"Open" ) 
            
            self.m_menu11 = wx.Menu()
            self.m_menubar1.Append( self.m_menu11, u"Search" ) 
            
            self.SetMenuBar( self.m_menubar1 )
            
            self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
            
            self.Centre( wx.BOTH )
            # Connect Events
            self.m_status.Bind( wx.EVT_CHOICE, self.f_status )
            self.query.Bind( wx.EVT_BUTTON, self.f_query )
            self.m_button3.Bind( wx.EVT_BUTTON, self.f_clear )
            
            self.manager = Manage()
            self.validate = False
            self.queryer = Query()
            self.timeChoices = ['--']
            self.leaveChoices = ['--']
            self.departChoices = ['--']
        
            handler = WxTextCtrlHandler(self.log) 
            logger.addHandler(handler) 
            FORMAT = "%(asctime)s %(levelname)s %(message)s" 
            handler.setFormatter(logging.Formatter(FORMAT)) 
            logger.setLevel(logging.DEBUG) 
        
        # Virtual event handlers, overide them in your derived class
        def m_dirPicker1OnDirChanged( self, event ):
            path = self.m_dirPicker1.GetPath()
            if self.manager.sort_excel(path) == False:
                self.validate = False
                print(u"未找到花名册")
            else:
                self.validate = True
                self.timeChoices, self.leaveChoices, self.departChoices = self.manager.load_main_info()
                
                self.m_depart.SetItems(self.departChoices)
                self.m_depart.SetSelection( 0 )
                
                if self.queryer.input.status != u'离职':
                    self.m_listBox1.SetItems(self.timeChoices)
                else:
                    self.m_listBox1.SetItems(self.leaveChoices)

        
        # Virtual event handlers, overide them in your derived class      
        def f_status( self, event ):
            self.queryer.input.status = event.GetString()
            if self.queryer.input.status != u'离职':
                self.m_listBox1.SetItems(self.timeChoices)
            else:
                self.m_listBox1.SetItems(self.leaveChoices)
            print(self.queryer.input.status)
        
        
        def f_query( self, event ):
            self.f_load_info()
            if self.queryer.input.query_time == []:
                wx.MessageBox(u'请选择花名册!!','Error',wx.OK|wx.ICON_INFORMATION)
                logger.log(logging.INFO, msg)
                return
            flag, msg = self.queryer.check(self.manager.info_dict)
            print(self.m_listBox1.GetSelections())
            if self.validate == False or flag == False:
                wx.MessageBox(msg,'Error',wx.OK|wx.ICON_INFORMATION)
                logger.log(logging.INFO, msg)
            else:
                wx.MessageBox(u'查询OK！！','Info',wx.OK|wx.ICON_INFORMATION)
                logger.log(logging.INFO, msg)
        
        def f_clear( self, event ):
            self.log.SetLabel("")
        
        def f_load_info(self):
            #input
            self.queryer.input.name = self.m_name.GetValue()
            self.queryer.input.gender = self.m_gender.GetString(self.m_gender.GetSelection())
            self.queryer.input.age_min = self.m_age_min.GetValue()
            if self.queryer.input.age_min == '' or self.queryer.input.age_min == u'':
                self.queryer.input.age_min = 0
            else:
                self.queryer.input.age_min = int(self.queryer.input.age_min)
            self.queryer.input.age_max = self.m_age_max.GetValue()
            if self.queryer.input.age_max == '' or self.queryer.input.age_max == u'':
                self.queryer.input.age_max = 0
            else:
                self.queryer.input.age_max = int(self.queryer.input.age_max)
            self.queryer.input.depart = self.m_depart.GetString(self.m_depart.GetSelection())
            
            self.queryer.input.start_time = self.m_time_start.GetValue()
            self.queryer.input.end_time = self.m_time_end.GetValue()
            #output
            self.queryer.output.salary_total = self.m_checkBox4.GetValue()
            self.queryer.output.info = self.m_checkBox3.GetValue()
            self.queryer.output.num = self.m_checkBox2.GetValue()
            self.queryer.output.salary = self.m_checkBox1.GetValue()
            
            self.queryer.input.query_time = []
            if self.queryer.input.status != u'离职':
                for i in self.m_listBox1.GetSelections():
                    self.queryer.input.query_time.append(self.timeChoices[i])
            else:
                for i in self.m_listBox1.GetSelections():
                    self.queryer.input.query_time.append(self.leaveChoices[i])

            print(self.queryer.input.query_time)
            print(self.queryer.input.status)
            print(self.queryer.input.name)
            print(self.queryer.input.gender)
            print(self.queryer.input.age_min)
            print(self.queryer.input.age_max)
            print(self.queryer.input.depart)
            print(self.queryer.output.salary_total)
            print(self.queryer.output.info)
            print(self.queryer.output.num)
            print(self.queryer.output.salary)
            print(self.queryer.input.start_time)
            print(self.queryer.input.end_time)
            
            
        
      
        def __del__( self ):
            pass
        
    if __name__ == "__main__":
        app = wx.App(False) 
        frame = MyFrame1(None)
        frame.Show()
        app.MainLoop()

except:
    print "Unexpected error:", sys.exc_info()
    raw_input('press enter key to exit')
    

