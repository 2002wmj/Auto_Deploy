#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Descri:      auto deploy lejiayuan app and config
#
# Author:      WangMinjie
#
# Created:     6/21/2016
# Copyright:   (c) LeJiaYuan 2016
#-------------------------------------------------------------------------------
from py_scripts.tools import *
from py_scripts.config import *
import subprocess

logger = logger()

def AsbTask(app_host_name,operate,app_ints=app_ints_range,full_choice=full_release):
    #吉高Ansible执行程序操作函数
    full_release = "true" if full_choice else "false" #判断是否增量发布，并初始化参数
    if operate == "dubbo_group":
        dubbo_group_id = getLetter()
        asb_commend = '''ansible-playbook %s.yml -i hosts_gigold -l %s -e '{"role_name":"AppDeploy","instances":%s,"full_release":%s,"dubbo_group_id":"%s"}' '''%(operate,app_host_name,app_ints,full_release,dubbo_group_id) #ansible执行命令拼接
    else:
        asb_commend = '''ansible-playbook %s.yml -i hosts_gigold -l %s -e '{"role_name":"AppDeploy","instances":%s,"full_release":%s}' '''%(operate,app_host_name,app_ints,full_release) #ansible执行命令拼接
    logger.info('ansible-cmd: '+asb_commend)   #写入日志文件
    print asb_commend
    sub_commend = subprocess.Popen(asb_commend, shell=True)
    result = sub_commend.wait()
    return result

def SqbjAsbTask(app_host_name,operate,lehome_dict,app_ints=app_ints_range,full_choice=full_release):
    #社区半径Ansible执行程序操作函数
    full_release = "true" if full_choice else "false" #判断是否增量发布，并初始化参数
    if operate == "dubbo_group":
        dubbo_group_id = getLetter()
        asb_commend = '''ansible-playbook %s.yml -i hosts_sqbj -l %s -e '{"role_name":"SqbjDeploy","instances":%s,"full_release":%s,"dubbo_group_id":"%s",%s}' '''%(operate,app_host_name,app_ints,full_release,dubbo_group_id,lehome_dict) #ansible执行命令拼接
    else:
        asb_commend = '''ansible-playbook %s.yml -i hosts_sqbj -l %s -e '{"role_name":"SqbjDeploy","instances":%s,"full_release":%s,%s}' '''%(operate,app_host_name,app_ints,full_release,lehome_dict) #ansible执行命令拼接
    logger.info('ansible-cmd: '+asb_commend)   #写入日志文件
    print asb_commend
    sub_commend = subprocess.Popen(asb_commend, shell=True)
    result = sub_commend.wait()
    return result

class Menu():
    def __init__(self,applist):
        self.applist = applist
        self.lehome_applist = lehome_applist

    def GetHosts(self):
        print '''
请从下面的菜单作选择
--------------------
1. 操作单或多个【吉高】程序
2. 批量操作【吉高】程序组
3. 操作单或多个【社区半径】程序
4. 批量操作【社区半径】程序组
0. 返回
--------------------'''
        commend = raw_input('请输入你的选择:')
        lehome_dict = None
        while 1:
            if commend not in ('1','2','3','4','0'):
                error_print('你的输入有误!')
                commend = raw_input('请输入[0-4]:')
            else:break
        if commend == '1':
            app_host_name = self.GgOneChoice()
        elif commend == '2':
            app_host_name = self.GgMoreChoices()
        elif commend == '3':
            app_host_name,lehome_dict = self.SqbjOneChoice()
        elif commend == '4':
            app_host_name,lehome_dict = self.SqbjMoreChoices()
        else:
            self.HomeMenu()
        print "你选择主机为：%s" %app_host_name
        app_ints = self.IntsChoice()   #选择实例ID
        return app_host_name,lehome_dict,app_ints

    def IntsChoice(self):
        if gray_res:
            print "由于你开启了灰度发布，请输入你要发布的实例ID",
            app_ints = getDigits(app_ints_range)
            if type(app_ints) == int:
                app_ints = [app_ints]
            else:
                app_ints = list(app_ints)
        else:app_ints = app_ints_range
        return  app_ints

    def GgOneChoice(self):
        #选择单个程序
        print "程序列表："
        print "--------------------"
        i = 1
        for (pno, app) in applist:
            print "%d. %s" %(i,app)
            i += 1
        params = range(1,i)
        print "请输入要操作的程序",
        app_choice = getDigits(params)
        if type(app_choice) == int:
            app_host_name = applist[app_choice-1][1]
        else:
            app_host_list = []
            for app_choice_num in app_choice:
                app_host_list.append(applist[app_choice_num-1][1])
            app_host_name = ','.join(app_host_list)
        return app_host_name

    def SqbjOneChoice(self,group_choice=None):
        #选择社区半径单个程序
        print "程序列表："
        print "--------------------"
        i = 1
        for (pno, app) in lehome_applist:
            print "%d. %s" %(i,pno+"_"+app)
            i += 1
        params = range(1,i)
        print "请输入要操作的程序",
        if group_choice:app_choice = group_choice #判断是否来自批量选择程序组
        else:app_choice = getDigits(params)
        lehome_dict = {}
        if type(app_choice) == int:
            #单选后的数据格式处理
            lehome_dict[lehome_applist[app_choice-1][0]] = [lehome_applist[app_choice-1][1]]
            app_host_name = lehome_dict.keys()[0]
        else:
            for app_choice_num in app_choice:
                #多选后的数据格式处理
                a = lehome_applist[app_choice_num-1]
                if a[0] in lehome_dict:
                    lehome_dict[a[0]].append(a[1])
                else:
                    lehome_dict[a[0]] = [a[1]]
            print str(lehome_dict)[1:-1].replace('\'','"')
            app_host_name = ','.join(lehome_dict.keys())
        return app_host_name,str(lehome_dict)[1:-1].replace('\'','"')

    def GgMoreChoices(self):
        #批量选择吉高程序组
        print '''
请选择操作项！
--------------------
1. 批量操作【吉高】所有WEB应用
2. 批量操作【吉高】所有Service应用
3. 批量操作【吉高】所有Gateway应用
4. 批量操作【吉高】所有应用
0. 返回【主页】
--------------------'''
        commend = raw_input('请输入你的选择:')
        while True:
            if commend not in ('1','2','3','4','0'):
                error_print('你的输入有误!')
                commend = raw_input('请输入[0-4]:')
            else:break
        if commend == '1':
            app_choices = "web_group"
        elif commend == '2':
            app_choices = "service_group"
        elif commend == '3':
            app_choices = "gateway_group"
        elif commend == '4':
            app_choices = "web_group,service_group,gateway_group"
        else:self.HomeMenu()
        return app_choices

    def SqbjMoreChoices(self):
        #批量选择社区半径程序组
        print '''
请选择操作项！
--------------------
1. 批量操作【社区半径】所有WEB应用
2. 批量操作【社区半径】所有Service应用
3. 批量操作【社区半径】所有Gateway应用
4. 批量操作【社区半径】所有应用
0. 返回【主页】
--------------------'''
        commend = raw_input('请输入你的选择:')
        while True:
            if commend not in ('1','2','3','4','0'):
                error_print('你的输入有误!')
                commend = raw_input('请输入[0-4]:')
            else:break
        if commend == '1':
            app_choices = "web_group"
            lehome_dict = self.SqbjOneChoice(lehome_web_list)[1]
        elif commend == '2':
            app_choices = "service_group"
            lehome_dict = self.SqbjOneChoice(lehome_service_list)[1]
        elif commend == '3':
            app_choices = "gateway_group"
            lehome_dict = self.SqbjOneChoice(lehome_gateway_list)[1]
        elif commend == '4':
            app_choices = "web_group,service_group,gateway_group"
            #lehome_dict = self.SqbjOneChoice(range(1,len(lehome_applist)+1))[1] #传入列表给批量选择函数并获取更新app的列表
            lehome_dict = self.SqbjOneChoice(lehome_all_list)[1]
        else:self.HomeMenu()
        return app_choices,lehome_dict

    def CtlOperate(self):
        # 程序控制操作选择
        while True:
            ctl_opt = raw_input("请选择操作：启动【L】，停止【S】，重启【R】，查看状态【I】，重新选择【P】")
            if ctl_opt.upper() in ['L', 'S', 'R', 'I','P']:
                if ctl_opt.upper() == 'L':
                    ctl_operate = 'start_app'
                elif ctl_opt.upper() == 'S':
                    ctl_operate = 'stop_app'
                elif ctl_opt.upper() == 'R':
                    ctl_operate = 'restart_app'
                elif ctl_opt.upper() == 'I':
                    ctl_operate = 'status_app'
                elif ctl_opt.upper() == 'P':
                    self.TaskMenu(self.CtlOperate)
            else:
                error_print("输入错误，请重新选择操作！")
                continue
            break
        return ctl_operate

    def DepOperate(self):
        # 程序部署操作选择
        while True:
            ctl_opt = raw_input("请选择操作：安装【I】，更新【U】，升级【A】,回滚【R】，重新选择【P】")
            if ctl_opt.upper() in ['I', 'U','A','R','P']:
                if ctl_opt.upper() == 'I':
                    dep_operate = 'install_app'
                elif ctl_opt.upper() == 'U':
                    dep_operate = 'update_app'
                elif ctl_opt.upper() == 'A':
                    dep_operate = 'upgrade_app'
                elif ctl_opt.upper() == 'R':
                    dep_operate = 'rollback_app'
                elif ctl_opt.upper() == 'P':
                    self.TaskMenu(self.DepOperate)
            else:
                error_print("输入错误，请重新选择操作！")
                continue
            break
        return dep_operate

    def ConfOperate(self):
        # 配置文件操作选择
        while True:
            ctl_opt = raw_input("请选择操作：开始下发配置文件【Y】，修改Dubbo分组【D】，查看Dubbo分组【C】，重新选择【P】")
            if ctl_opt.upper() in ['Y','D','C','P']:
                if ctl_opt.upper() == 'Y':
                    conf_operate = 'app_config'
                elif ctl_opt.upper() == 'D':
                    conf_operate = 'dubbo_group'
                elif ctl_opt.upper() == 'C':
                    conf_operate = 'chk_dubbo_group'
                elif ctl_opt.upper() == 'P':
                    self.TaskMenu(self.ConfOperate)
            else:
                error_print("输入错误，请重新选择操作！")
                continue
            break
        return conf_operate

    def InitOperate(self):
        # Tomcat操作选择
        while True:
            ctl_opt = raw_input("请选择操作：安装TOMCAT【T】，安装JDK【J】，重新选择【P】")
            if ctl_opt.upper() in ['T','J','P']:
                if ctl_opt.upper() == 'T':
                    init_operate = 'install_tomcat'
                elif ctl_opt.upper() == 'J':
                    init_operate = 'install_jdk'
                elif ctl_opt.upper() == 'P':
                    self.TaskMenu(self.InitOperate)
            else:
                error_print("输入错误，请重新选择操作！")
                continue
            break
        return init_operate

    def TaskMenu(self,Operate):
        '''程序控制入口:可【运行，停止，重启】程序'''
        app_host_name,lehome_dict,app_ints = self.GetHosts()
        operate = Operate()
        if lehome_dict:
            #根据循环参数判断是吉高还是社区半径的程序
            result = SqbjAsbTask(app_host_name,operate,lehome_dict,app_ints)
        else:
            result = AsbTask(app_host_name,operate,app_ints)
        if result != 0:
            error_print("xxxxxxxx任务执行失败，请查看执行日志！xxxxxxxx\n\n")
            logger.error('[The ansible is tasks failure!]')
            exit()
        else:
            finish_print("任务运行成功!")
            logger.info('[The ansible is tasks success!]')
            next_opt = raw_input("继续【选择程序】请按Y，返回【主页】请按其余任意键:")
            if next_opt.upper() == "Y":
                self.TaskMenu(Operate)
            else:
                self.HomeMenu()

    def HomeMenu(self):
        #自动化部署程序主页
        print '''
        \033[1;31;40mWelcome to auto_deploy V2.0 program\033[0m
=================================================
请从下面的菜单作选择
1  程序控制入口:可【运行、停止、重启、查看状态】程序
2  程序部署入口:可【安装、更新、升级、回滚】程序
3  程序配置入口:可【下发、修改】配置文件
4  程序TOMCAT和JDK安装入口：WEB项目第一次部署时必须安装TOMCAT
0  退出
================================================='''
        commend = raw_input('请输入你的选择:')
        while True:
            if commend not in ('1','2','3','4','0'):
                error_print('你的输入有误!')
                commend = raw_input('请输入[0-4]:')
            else:break
        if commend == '1':
            print('输入1,进入程序控制入口！')
            self.TaskMenu(self.CtlOperate)
        elif commend == '2':
            print('输入2,进入程序部署入口！')
            self.TaskMenu(self.DepOperate)
        elif commend == '3':
            print('输入3,进入配置文件入口！')
            self.TaskMenu(self.ConfOperate)
        elif commend == '4':
            print('输入4,进入TOMCAT和JDK安装入口！')
            self.TaskMenu(self.InitOperate)
        elif commend == '0':
            exit()


if __name__ == '__main__':
    #Menu = Menu(applist)
    Menu(applist).HomeMenu()
