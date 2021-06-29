# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: set_time_path.py
import datetime, threading
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import tkinter, winreg, os


def thread_it(func, *args):
    """将函数打包进线程"""
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


def get_Last27():
    now = datetime.datetime.now()
    now_year = now.strftime('%Y')
    now_Mouth = now.strftime('%m')
    now_day = now.strftime('%d')
    if int(now_day) <= 27:
        if int(now_Mouth) == 1:
            year = str(int(now_year) - 1)
            Mouth = str(12)
        else:
            Mouth = str(int(now_Mouth) - 1)
            year = now_year
    else:
        Mouth = now_Mouth
        year = now_year
    strt_time = year + '-' + Mouth + '-27'
    return strt_time


def get_Date():
    now = datetime.datetime.now()
    delt = datetime.timedelta(days=(-1))
    n_days = now + delt
    yestday = n_days.strftime('%Y-%m-%d')
    return yestday


def get_Path():
    ifexit = os.path.exists('save_path.txt')
    if ifexit == False:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders')
        desk = winreg.QueryValueEx(key, 'Desktop')[0]
        cwd = desk + '\\DailyToday'
        if not os.path.exists(cwd):
            os.mkdir(cwd)
        return cwd
    f1 = open('save_path.txt', 'r', encoding='gbk')
    cwd = f1.read()
    f1.close()
    return cwd


def selectPath():
    path = askdirectory()
    if path != '':
        path = path.replace('/', '\\\\')
        f1 = open('save_path.txt', 'w')
        f1.write(path)
        f1.close()


def clear_user():
    ifexit = os.path.exists('account0.txt')
    if ifexit == True:
        os.remove('account0.txt')
        tkinter.messagebox.showinfo('', '账号信息已清除！')
    else:
        tkinter.messagebox.showinfo('', '没有信息！')


def change_pipei():
    path_pipei = 'connectTable.xlsx'
    os.system('explorer.exe %s' % path_pipei)


def change_para():
    path_pipei = 'model_list.xlsx'
    os.system('explorer.exe %s' % path_pipei)


def openmir():
    ifexit = os.path.exists('save_path.txt')
    if ifexit == False:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders')
        desk = winreg.QueryValueEx(key, 'Desktop')[0]
        cwd = desk + '\\DailyToday'
        os.path.exists(cwd) or os.mkdir(cwd)
    else:
        f1 = open('save_path.txt', 'r')
        cwd = f1.read()
        f1.close()
    cwd = cwd.replace('\\\\', '\\')
    os.system('explorer.exe %s' % cwd)

# okay decompiling .\set_time_path.pyc
