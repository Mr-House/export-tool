# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: main_ui.py
from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox
from set_time_path import thread_it, selectPath, clear_user, change_pipei, openmir, change_para
from tkinter import scrolledtext
import pandas, time


def main_ui(object, account, model_parameter):
    global Information_baoyuan
    global Information_end_choose
    global Information_time
    global load_img
    global model_pa
    global myWindow
    global over_img
    global progress_data
    global progress_main
    global select_1
    global select_2
    global select_3
    global start_button
    global start_img
    model_pa = model_parameter.columns.tolist()
    print(model_pa)
    myWindow = Tk()
    myWindow.title('Daily')
    width = 475
    height = 340
    screenwidth = myWindow.winfo_screenwidth()
    screenheight = myWindow.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    myWindow.geometry(alignstr)
    myWindow.resizable(width=False, height=False)
    menubar = Menu(myWindow)
    filemenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='查看', menu=filemenu)
    filemenu.add_command(label='目标文件夹', command=openmir)
    filemenu.add_command(label='任务列表', command=(lambda: tkinter.messagebox.showinfo(title='提示', message='暂未开通')))
    filemenu.add_separator()
    filemenu.add_command(label='退出', command=callbackClose)
    settingmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='选项', menu=settingmenu)
    settingmenu.add_command(label='更改匹配表', command=change_pipei)
    settingmenu.add_command(label='参数设置', command=change_para)
    settingmenu.add_command(label='选择存储路径', command=selectPath)
    settingmenu.add_command(label='清除账户密码', command=clear_user)
    progress_main = ttk.Progressbar(myWindow, length=380, value=0, mode='determinate')
    progress_data = tkinter.Label(myWindow, text='0', font=('微软雅黑', 14), fg='#436EEE', width=3, height=1)
    Information_baoyuan = scrolledtext.ScrolledText(myWindow, width=58, height=16, wrap=(tkinter.WORD))
    Information_time = tkinter.Label(myWindow, text='0s', font=('微软雅黑', 14), width=15, height=1)
    Information_end_choose = tkinter.Label(myWindow, text='', font=('微软雅黑', 14), justify=LEFT, width=10, height=1)
    select_2 = tkinter.Label(myWindow, text=(model_pa[0]), font=('微软雅黑', 18), fg='#6495ED', width=15, height=1)
    select_2.place(x=118, y=125)
    select_2.bind('<MouseWheel>', select_model)
    select_1 = tkinter.Label(myWindow, text=(model_pa[1]), font=('微软雅黑', 30), fg='#3A5FCD', width=15, height=1)
    select_1.place(x=50, y=170)
    select_1.bind('<MouseWheel>', select_model)
    select_3 = tkinter.Label(myWindow, text=(model_pa[2]), font=('微软雅黑', 18), fg='#6495ED', width=15, height=1)
    select_3.place(x=118, y=235)
    select_3.bind('<MouseWheel>', select_model)
    start_img = PhotoImage(file='start_img.png')
    load_img = PhotoImage(file='load_img.png')
    over_img = PhotoImage(file='over_img.png')
    start_button = Button(myWindow, image=start_img, text='0', relief=FLAT, cursor='hand2',
                          command=(lambda: start_your_work(account, model_parameter, select_1['text'])))
    start_button.place(x=165, y=50)
    myWindow.config(menu=menubar)
    myWindow.iconbitmap('ui_img.ico')
    myWindow.protocol('WM_DELETE_WINDOW', callbackClose)
    myWindow.mainloop()


def select_model(event):
    if event.delta < 0:
        a = model_pa.index(select_1['text'])
        b = model_pa.index(select_2['text'])
        c = model_pa.index(select_3['text'])
        try:
            model_pa[(a + 1)]
        except IndexError:
            select_1.config(text=(model_pa[0]))
        else:
            select_1.config(text=(model_pa[(a + 1)]))
        try:
            model_pa[(b + 1)]
        except IndexError:
            select_2.config(text=(model_pa[0]))
        else:
            select_2.config(text=(model_pa[(b + 1)]))
        try:
            model_pa[(c + 1)]
        except IndexError:
            select_3.config(text=(model_pa[0]))
        else:
            select_3.config(text=(model_pa[(c + 1)]))
        myWindow.update()
    else:
        a = model_pa.index(select_1['text'])
        select_1.config(text=(model_pa[(a - 1)]))
        b = model_pa.index(select_2['text'])
        select_2.config(text=(model_pa[(b - 1)]))
        c = model_pa.index(select_3['text'])
        select_3.config(text=(model_pa[(c - 1)]))
        myWindow.update()


def start_your_work(account, model_parameter, currtent_choose):
    if start_button['text'] == '0':
        move_ui()
        from parameter_control import thread_control
        thread_it(thread_control, account, model_parameter, currtent_choose)
    else:
        if start_button['text'] == '1':
            openmir()
            start_button.config(text='0', image=start_img)
            start_button.place(x=165, y=50)
            Information_end_choose.place_forget()
            Information_time.place_forget()
            Information_baoyuan.delete(0.0, END)
            Information_baoyuan.place_forget()
            progress_main.config(value=0)
            progress_data.config(text='0')
            progress_main.place_forget()
            progress_data.place_forget()
            select_1.place(x=50, y=170)
            select_2.place(x=118, y=125)
            select_3.place(x=118, y=235)
            myWindow.update()


def move_ui():
    select_1.place_forget()
    select_2.place_forget()
    select_3.place_forget()
    start_button.config(image=load_img, state=DISABLED)
    Information_end_choose.config(text=(select_1['text']))
    Information_end_choose.place(x=170, y=10)
    myWindow.update()
    for i in range(0, 50):
        start_button.place(x=(165 + i * 2.8), y=(50 - i * 0.8))
        Information_end_choose.place(x=(170 - i * 2.8), y=(10 + i * 0.02))
        Information_baoyuan.config(height=(i * 0.32))
        Information_baoyuan.place(x=25, y=(270 - i * 4.4))
        myWindow.update()

    Information_time.place(x=160, y=11)
    progress_main.place(x=25, y=280)
    progress_data.place(x=405, y=276)
    myWindow.update()


def set_button():
    start_button.config(text='1', image=over_img, state=NORMAL)
    myWindow.update()


def count_time():
    i = 0
    while 1:
        if start_button['text'] == '0':
            Information_time.config(text=(str(i) + 'S'))
            myWindow.update()
            time.sleep(1)
            i = i + 1
    else:
        Information_time.config(text=(str(i - 1) + 'S'))
        myWindow.update()


def callbackClose():
    if tkinter.messagebox.askokcancel(title='警告', message='退出后程序将终止！\n确认退出？'):
        sys.exit(0)


def callback_end():
    tkinter.messagebox.showinfo(title='提示！', message='数据处理完毕!')


def test(content_text):
    Information_baoyuan.insert('end', content_text + '\n')
    Information_baoyuan.update()


def show_progress(now_pro):
    a = int(progress_data['text'])
    if now_pro == 0:
        if a < 90:
            progress_main.config(value=(a + 3))
            progress_data.config(text=(str(a + 3)))
            myWindow.update()
    else:
        progress_main.config(value=now_pro)
        progress_data.config(text=now_pro)
        myWindow.update()


if __name__ == '__main__':
    account = ''
    model_parameter = pandas.DataFrame()
    main_ui(object, account, model_parameter)
# okay decompiling .\main_ui.pyc
