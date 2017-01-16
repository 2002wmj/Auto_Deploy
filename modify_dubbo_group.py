#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#用于修改老社区半径Dubbo分组的脚本
import subprocess
from py_scripts.tools import *

def AsbDubboGroup(app_ints,dubbo_group):
    asb_commend = '''ansible-playbook chk_old_sqbj_group.yml -i hosts_old_sqbj -e '{"instances":[%s],"dubbo_group":"%s"}' '''%(app_ints,dubbo_group)
    print asb_commend
    sub_commend = subprocess.Popen(asb_commend, shell=True)
    result = sub_commend.wait()


def Menu():
    print "你正在修改社区半径老应用的Dubbo分组！"
    print "================================================="
    app_ints = raw_input("请输入你要操作的实例ID[1,2]:")
    dubbo_group = getLetter()
    commend = raw_input("是否确认将实例\"%s\"切换成\"%s\"分组，确认请按[Y]:"%(app_ints,dubbo_group))
    if commend.upper() == "Y":
        AsbDubboGroup(app_ints,dubbo_group)
    else:
        exit(1)

if __name__ == '__main__':
    Menu()