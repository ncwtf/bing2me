#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tkinter as tk

window = tk.Tk()  # 创建窗口对象的背景色window = tk.Tk()
window.title("bing2me")
window.geometry("200x300")

tk.Label(window, text='开机自动启动').place(x=50, y=50)
tk.Checkbutton(window).place(x=140, y=50)

# canvas = tk.Canvas(window, height=300, width=500)
# # image_file = tk.PhotoImage(file="./bing-pic/1573122967.7625408.jpg")
# # image = canvas.create_image(0, 0, anchor='nw', image=image_file)
# canvas.pack(side='top')
#
# tk.Label(window, text='User name:').place(x=50, y=200)
# tk.Label(window, text='Password:').place(x=50, y=250)
#
# var_usr_name = tk.StringVar()
# var_usr_name.set('请输入用户名')
#
# var_usr_pwd = tk.StringVar()
# # var_usr_pwd.set('请输入密码')
#
# entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
# entry_usr_name.place(x=160, y=200)
# entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
# entry_usr_pwd.place(x=160, y=250)
#
#
#
# # login and sign up
# btn_login = tk.Button(window, text="Login")
# btn_login.place(x=155, y=300)
#
# btn_sign_up = tk.Button(window, text="Sign up")
# btn_sign_up.place(x=270, y=300)
window.mainloop()  # 进入消息循环
