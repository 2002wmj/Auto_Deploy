#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#脚本目的：检查当前目录的更新包，根据应用列表输出需要更新的应用序号列表
import commands
import sys
sys.path.append("../../../py_scripts/")
import tools
CMD = 'ls |grep gigold|awk -F "[-.]" \'{print $2 "-" $3}\''
update_app = commands.getoutput(CMD).split('\n')
num_list = []
update_list = []
for i in update_app:
    new_name = "SH_" + i[0].upper() + "_" + i.split("-")[1]
    app_num = 1
    for app_name in tools.applist:
        if new_name == app_name[1]:
            num_list.append(str(app_num))
            update_list.append(new_name)
            break
        app_num += 1
print "本次需要更新应用的序号列表："
print ','.join(num_list)
#print ','.join(update_list)