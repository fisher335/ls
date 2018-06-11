# -*- coding: utf-8 -*-
# @Date    : 2017/11/30 0030 , @Author  : fengshaomin@bjsasc.com
import easygui as g

msg = "选择你喜欢的一种业余生活"
title = ""
b = g.buttonbox(msg="点击确定开始上传", title="上传", choices=["选择文件", "退出"])
if b == "退出":
    exit(0)
a = g.fileopenbox(msg=msg, title=title)
g.msgbox(a)
g.textbox("aaa")
