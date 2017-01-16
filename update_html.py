#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#用于更新社区半径静态项目的脚本
import subprocess
def AsbHtmlTask(app_name):
    asb_commend = '''ansible-playbook update_app.yml -i hosts_sqbj -l LH_web01 -e '{"role_name":"SqbjDeploy","instances":[1, 2],"full_release":true,"LH_web01":[%s],"group_name":"html"}' '''%(app_name)
    print asb_commend
    sub_commend = subprocess.Popen(asb_commend, shell=True)
    result = sub_commend.wait()


def AppChoice():
    print """程序列表：
-----------------------
1. lehome-html-linkManage
2. lehome-html-merchant
3. lehome-html-public
4. lehome-html-wechat
5. smart-html-centerConsole
-----------------------
"""
    choice_id = raw_input("请选择你要更新静态项目[1-5]:")
    choice_name = []
    if "1" in choice_id:
        choice_name.append("linkManage")
    if "2" in choice_id:
        choice_name.append("merchant")
    if "3" in choice_id:
        choice_name.append("public")
    if "4" in choice_id:
        choice_name.append("wechat")
    if "5" in choice_id:
        choice_name.append("centerConsole")
    AsbHtmlTask(str(choice_name)[1:-1].replace('\'','"'))

if __name__ == '__main__':
    AppChoice()