# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: login.py
import robobrowser, os, re


def inname():
    ifexit = os.path.exists('account0.txt')
    if ifexit == False:
        account = [ '', '']
        return account
    f1 = open('account0.txt', 'r')
    s = f1.read()
    f1.close()
    account = re.split('/-----/', s)
    return account


def login(account):
    b = robobrowser.RoboBrowser(parser='lxml')
    b.open('http://crm.hisense.com/HisenseCRM/login.do?method=begin')
    f = b.get_form(action='/HisenseCRM/j_unieap_security_check.do')
    print(account)
    f['j_username'].value = account[0]
    f['j_password'].value = account[1]
    b.submit_form(f)
    try:
        result = b.find('div', {'class': 'fail_box', 'style': 'line-height: 24px'}).get_text()
        print(result.strip().replace('\xa0[重新登录]', ''))
    except AttributeError:
        test = 'True'
        return test
    else:
        test = 'False'
        return test


if __name__ == '__main__':
    account = inname()
    b = login(account)
# okay decompiling .\login.pyc
