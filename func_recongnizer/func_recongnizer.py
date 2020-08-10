#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/08/10
# @Author  : Sun Zhiron
# @FileName: func_recognizer.py
# @Software: 公式识别
# @微信公众号   ：工科小学生

import os
from base64 import b64encode
from requests import post
import json
from PIL import ImageGrab
from tkinter import *
from tkinter import messagebox

filename = 'log_info.log'

mygui = Tk() #定义窗口

mygui.title("公式识别")    # 设置窗口标题
mygui.iconbitmap("E:\学习\编程\python\公式识别软件\gonshi.ico") # 设置窗口图标
sw = mygui.winfo_screenwidth() # 获取电脑屏幕宽度
sh = mygui.winfo_screenheight() # 获取电脑屏幕宽度
ww = 250 #设置窗口宽度
wh = 200 #设置窗口高度

# 窗口宽高为100

x = int((sw-ww) / 2)
y = int((sh-wh) / 2)
mygui.geometry("{}x{}+{}+{}".format(ww, wh, x, y))    # 设置窗口居中显示
mygui.resizable(width=False, height=False) # 设置窗口无法调整大小

# 创建app_id输入框
varid = StringVar()
uName_box = Entry(mygui, width=80, textvariable=varid)
uName_box.place(x=100, y=5, width=130, height=20)

# 创建app_key输入框
varkey = StringVar()
passw_box = Entry(mygui, show='*', width=30, textvariable=varkey)
passw_box.place(x=100, y=30, width=130, height=20)

#创建app_id,app_key标签
lable_usr = Label(mygui, text="app_id:", bd=5, font=("Arial", 12),)
lable_paw = Label(mygui, text="app_key:", bd=5, font=("Arial", 12))
lable_usr.place(x=10, y=5, width=80, height=20)
lable_paw.place(x=10, y=30, width=80, height=20)

# 定义登陆信息存储函数
var = IntVar()
def save_info():
    if var.get() == 1:
        info = {}
        info['username'] = uName_box.get()
        info['password'] = passw_box.get()
        with open(filename, 'w') as fp:
            fp.write(','.join((info['username'], info['password'])))
        print(info)


# 创建记住我单选框
Check_Save = Checkbutton(mygui, text='记住我', variable=var, onvalue=1, offvalue=0, command=save_info)
Check_Save.place(x=20, y=80, width=80, height=20)

#识别函数
def mathpix():
    try:
        Id = varid.get()
        Key = varkey.get()
        if ImageGrab.grabclipboard():
            im = ImageGrab.grabclipboard()
            im.save('screen.png','PNG')
        file_path ='screen.png'
        image_uri = "data:image/jpg;base64," + b64encode(open(file_path, "rb").read()).decode()
        r = post("https://api.mathpix.com/v3/text",
            data=json.dumps({'src': image_uri,"ocr": [ "math","text"],'formats': ['latex_styled']}),
            headers={"app_id": Id,  "app_key": Key,
                    "Content-type": "application/json"})
        result  = json.loads(r.text)
        # print(result['latex_styled'])
        varresult.set(result['latex_styled'])
        
    except Exception as e:
        if "'NoneType' object has no attribute 'save'"==str(e):
            messagebox.showerror(title='注意', message="剪切板未检测到图像！")
        elif "'latex_styled'"==str(e):
            messagebox.showerror(title='注意', message="请配置app_id,app_key!")
            # print(e)


# 创建识别按钮
log_butt = Button(mygui, text='识别', command=mathpix)
log_butt.place(x=140, y=75, width=40, height=30)

#创建识别结果标签
lable_result = Label(mygui, text="识别结果:", bd=5, font=("宋体", 12),)
lable_result.place(x=10, y=120, width=80, height=20)

#创建多行文本框
varresult = StringVar()
result_box = Entry(mygui, width=30, textvariable=varresult)
result_box.place(x=10, y=150, width=230, height=30)
 
# "insert" 索引表示插入光标当前的位置
# tex.insert(result['latex_styled'])


def main():
    try:
        if os.path.exists(filename):
            with open(filename) as fp:
                n, p = fp.read().strip().split(',')
                varid.set(n)
                varkey.set(p)
    except Exception as e:
        messagebox.showerror(title='注意', message=e)
    mygui.mainloop()


if __name__ == "__main__":
    main()