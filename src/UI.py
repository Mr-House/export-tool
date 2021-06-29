# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: UI.py
from tkinter import *
import tkinter
from tkinter import messagebox
from login import login, inname
from main_ui import main_ui
import os, pandas, requests

model_parameter = pandas.read_excel('model_list.xlsx', index_col='moshi_name', keep_default_na=False)


class Login(object):
    def __init__(self):
        global chVarDis
        self.root = tkinter.Tk()
        self.root.title('Daily')
        width = 400
        height = 200
        self.root.geometry(str(width) + 'x' + str(height))
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        self.alignstr = '%dx%d+%d+%d' % (
        width, height, (self.screenwidth - width) / 2, (self.screenheight - height) / 2)
        self.root.geometry(self.alignstr)
        self.label_account = tkinter.Label((self.root), text='账户: ')
        self.label_password = tkinter.Label((self.root), text='密码: ')
        addr_username = StringVar(value=(account[0]))
        self.input_account = tkinter.Entry((self.root), width=30, textvariable=addr_username)
        addr_pwd = StringVar(value=(account[1]))
        self.input_password = tkinter.Entry((self.root), show='*', width=30, textvariable=addr_pwd)
        chVarDis = IntVar()
        self.remenber_button = tkinter.Checkbutton((self.root), variable=chVarDis, text='记住密码', width=10)
        if account != ['', '']:
            self.remenber_button.select()
        self.siginUp_button = tkinter.Button((self.root), command=(self.siginUp_interface), text='登陆', width=10)
        self.waiting = tkinter.Label((self.root), text='--正在登陆--', font=('微软雅黑', 15))

    def gui_arrang(self):
        self.label_account.place(x=60, y=50)
        self.label_password.place(x=60, y=75)
        self.input_account.place(x=110, y=50)
        self.input_password.place(x=110, y=75)
        self.remenber_button.place(x=115, y=115)
        self.siginUp_button.place(x=220, y=115)
        self.root.iconbitmap('ui_img.ico')

    def siginUp_interface(self):
        user = self.input_account.get()
        passd = self.input_password.get()
        account = [user, passd]
        self.siginUp_button.config(state=DISABLED)
        self.waiting.place(x=150, y=150)
        self.root.update()
        try:
            test = login(account)
        except TypeError:
            self.siginUp_interface()
        except requests.exceptions.ConnectionError:
            call_nonet()
            self.siginUp_button.config(state=NORMAL)
            self.waiting.place_forget()
            self.root.update()
        else:
            if test == 'True':
                if chVarDis.get() == 1:
                    f1 = open('account0.txt', 'w')
                    f1.write(user + '/-----/' + passd)
                    f1.close()
                else:
                    ifexit = os.path.exists('account0.txt')
                    if ifexit == True:
                        os.remove('account0.txt')
                self.root.destroy()
                main_ui(object, account, model_parameter)
            else:
                tkinter.messagebox.showinfo(title='提示', message='登录失败！\n请核对密码')
                self.siginUp_button.config(state=NORMAL)
                self.waiting.place_forget()
                self.root.update()


def main():
    L = Login()
    L.gui_arrang()
    tkinter.mainloop()


def callbackClose():
    if tkinter.messagebox.askokcancel(title='警告', message='退出后程序将终止！\n确认退出？'):
        sys.exit(0)


def call_nonet():
    tkinter.messagebox.showwarning(title='警告', message='无网络连接，请确认网络是否正常！')


if __name__ == '__main__':
    account = inname()
    main()
# okay decompiling .\UI.pyc
