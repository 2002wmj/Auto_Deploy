#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Descri:      auto deploy lejiayuan app and config
#
# Author:      WangMinjie
#
# Created:     6/8/2016
# Copyright:   (c) LeJiaYuan 2016
#-------------------------------------------------------------------------------
import logging

def error_print(info):
    print '\033[1;31;40m' + info + '\033[0m'

def finish_print(info):
    print '\033[1;32;40m' + info + '\033[0m'

# add by dengqy
def getDigit(params=None):
    '''
    作用：从键盘获取一个数字，并做规范性检查
    参数：params列表或元组，为可选，如果给出，则输入的数字必须在params内。
    '''
    while True:
        num_str = raw_input("[%d-%d]："%(params[0],params[-1]))
        if num_str.isdigit():
            num_int = int(num_str)
            if isinstance(params, (tuple, list)) and len(params) > 0:
                if num_int in params:
                    break
                else:
                    error_print("输入的不是一个有效选项！")
            else:
                break
        else:
            error_print("输入的不是一个数字！")
            continue
    return num_int

def getDigits(params=None):
    '''
    作用：从键盘获取一组或者一个数字，并做规范性检查
    参数：params列表或元组，为可选，如果给出，则输入的数字必须在params内。
    '''
    while True:
        num_strs = raw_input("[%d-%d](多选请以逗号分开)："%(params[0],params[-1]))
        if num_strs.isdigit():
            num_tuple = int(num_strs)
            if isinstance(params, (tuple, list)) and len(params) > 0:
                if num_tuple in params:
                    break
                else:
                    error_print("输入的不是一个有效选项！")
            else:
                break
        else:
            try:
                num_tuple = tuple(eval(num_strs))
            except:
                error_print("输入的格式错误！")
                continue
            if isinstance(params, (tuple, list)) and len(params) > 0:
                if len(num_tuple) != len(set(num_tuple)):
                    error_print("输入的列表中存在重复选项！")
                    continue
                elif set(num_tuple).issubset(set(params)):
                    break
                else:
                    error_print("输入的不是一个有效选项！")
            else:
                break
    return num_tuple

def getLetter():
    while True:
        let_str = raw_input("请输入Dubbo分组名称[A-Z]：")
        if len(let_str) == 1 and let_str.isalpha():
            let_str = let_str.upper()
            break
        else:
            error_print("输入的不是一个字母！")
            continue
    return let_str


# 默认app配置单
applist = [('1','SH_S_cashier'),
         ('2', 'SH_S_customer'),
         ('1', 'SH_S_dispatchingMonitor'),
         ('1', 'SH_S_fdc'),
         ('1', 'SH_S_fdcBatch'),
         ('1', 'SH_S_riskControl'),
         ('1', 'SH_S_foundationBatch'),
         ('1', 'SH_S_fundBatch'),
         ('1', 'SH_S_merchant'),
         ('1', 'SH_S_account'),
         ('1', 'SH_S_runManager'),
         ('1', 'SH_S_trade'),
         ('1', 'SH_S_repeat'),
         ('1', 'SH_S_industrypay'),
         ('1', 'SH_S_cardpos'),
         ('2', 'SH_S_posp'),
         ('2', 'SH_S_billCenter'),
         ('2', 'SH_G_smsBC'),
         ('2', 'SH_G_citic'),
         ('2', 'SH_G_htfFund'),
         ('2', 'SH_G_unionpay'),
         ('2', 'SH_G_weixin'),
         ('2', 'SH_G_trade'),
         ('2', 'SH_G_pospBusiness'),
         ('2', 'SH_G_pospManage'),
         ('2', 'SH_G_cardpos'),
         ('2', 'SH_G_fdcDownload'),
         ('2', 'SH_G_applepay'),
         ('2', 'SH_G_voiceCL'),
         ('2', 'SH_G_quickpay'),
		 ('2', 'SH_G_guardRoute'),
		 ('2', 'SH_G_guard'),
         ('2', 'SH_G_payment'),
         ('2', 'SH_W_batchMonitor'),
         ('2', 'SH_W_cashier'),
         ('3', 'SH_W_dispatchingCenter'),
         ('3', 'SH_W_fdc'),
         ('3', 'SH_W_foundation'),
         ('3', 'SH_W_htfFund'),
         ('3', 'SH_W_industrypay'),
         ('3', 'SH_W_runManager'),
         ('3', 'SH_W_trade'),
         ('3', 'SH_W_guard'),
         ('3', 'test')
         ]

lehome_applist = [
        ('LH_web01', 'ast'),
        ('LH_web01', 'business'),
        ('LH_web01', 'mapi'),
        ('LH_web01', 'property'),
        ('LH_web01', 'link'),
        ('LH_web01', 'linkManager'),
        ('LH_web01', 'dispatchingCenter'),
        ('LH_web01', 'merchant'),
        ('LH_web02', 'mkt'),
        ('LH_web02', 'baseGW'),
        ('LH_web02', 'open'),
        ('LH_web02', 'wechat'),
        ('LH_service01', 'mq'),
        ('LH_service01', 'user'),
        ('LH_service01', 'message'),
        ('LH_service01', 'business'),
        ('LH_service02', 'ast'),
        ('LH_service02', 'astjob'),
        ('LH_service02', 'dispatcher'),
        ('LH_service02', 'event'),
        ('LH_service02', 'link'),
        ('LH_service02', 'operation'),
        ('LH_service02', 'statistics'),
        ('LH_service02', 'log'),
        ('LH_service02', 'mkt'),
        ('LH_service02', 'mktjob'),
        ('LH_service03', 'open'),
        ('LH_service03', 'wechat'),
        ('LH_gateway01', 'gigoldpay'),
        ('LH_gateway01', 'thirdparty'),
        ('LH_gateway01', 'property'),
        ('LH_gateway01', 'wechat'),
        ('LH_gateway01', 'message'),
        ('SM_web01', 'centerConsole'),
        ('SM_web01', 'dispatchingCenter'),
        ('SM_service01', 'centerConsole'),
        ('SM_service01', 'monitorRoute'),
        ('SM_gateway01', 'monitor'),
        ('SM_gateway01', 'centerConsole'),
        ('SM_gateway01', 'guardManager')
]

def GetAppGroupList(applist,group):
    #根据传入社区半径应用组名，返回所有符合组名的应用序列列表
    app_list = []
    app_nu = 1
    for a in applist:
        if group in a[0]:
            app_list.append(app_nu)
        app_nu += 1
    return app_list

lehome_all_list = GetAppGroupList(lehome_applist,"LH")  #所有社区半径web应用的序号列表
lehome_web_list = GetAppGroupList(lehome_applist,"web")  #所有社区半径web应用的序号列表
lehome_service_list = GetAppGroupList(lehome_applist,"service")  #所有社区半径service应用的序号列表
lehome_gateway_list = GetAppGroupList(lehome_applist,"gateway")    #所有社区半径gateway应用的序号列表

tomcatList = ['tomcat-gigold-web-batchMonitor',
            'tomcat-gigold-web-cashier',
            'tomcat-gigold-web-dispatchingCenter',
            'tomcat-gigold-web-fdc',
            'tomcat-gigold-web-foundation',
            'tomcat-gigold-web-htfFund',
            'tomcat-gigold-web-industrypay',
            'tomcat-gigold-web-runManager',
            'tomcat-gigold-web-trade',
            'tomcat-gigold-web-upload']


class logger():
    '''
        日志写入模块
    '''
    def __init__(self):
        logger = logging.getLogger('AutoDeploy')
        logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler('py_scripts/AutoDeploy.log')
        fh.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(fh)
        self.logger = logger

    def info(self,message):
         # 记录一条INFO日志
        self.logger.info(message)

    def error(self,message):
         # 记录一条INFO日志
        self.logger.error(message)


if __name__ == '__main__':
    print "程序调用文件,无法直接运行!"