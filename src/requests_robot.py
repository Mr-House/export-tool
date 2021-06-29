# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: requests_robot.py
from set_time_path import thread_it, get_Date
import robobrowser, pandas, base64, json, uuid
from retrying import retry
import re
# from set_time_path import get_Date
from pipei_file import print_ui
from main_ui import show_progress


@retry()
def getnps(account, start, end):
    print('NPS')
    b = robobrowser.RoboBrowser(parser='lxml')
    b.open('http://crm.hisense.com/HisenseCRM/login.do?method=begin')
    f = b.get_form(action='/HisenseCRM/j_unieap_security_check.do')
    f['j_username'].value = account[0]
    f['j_password'].value = account[1]
    b.submit_form(f)
    str_encrypt = json.dumps({'date_end': start, 'product_id': '', 'ifsw': '',
                              'date_start': end})
    paigong = base64.b64encode(str_encrypt.encode('utf-8'))
    paigong = str(paigong).lstrip("b'")
    crmuuid = str(uuid.uuid4())
    out0 = b.session.post((
                          'http://crm.hisense.com/HisenseReport/Report-CsvAction.do?linage=20&district=20&reportId=c929a939-5722-438a-8f9f-34816c47569e&ctype=1&unieap_report_params=' + paigong + '&isResultant=false&newReport=null&cachedId=' + crmuuid + '&multiDataSegment=true&segmentNumber=null&segmentPosition=null&segmentPage=null&segmentPagesCount=null&parentId=&newName=&caption=null&changePageCount=1&drillThroughContext=&UniEAP_Report_olapcontext=null&excelExporterType=0&goto_page_number=1&ctype=null&all=false&needProgressBar=false'),
                          headers={'Referer': 'http://crm.hisense.com/HisenseReport/Report-ResultAction.do'},
                          allow_redirects=False)
    paigong_resp = out0.text
    ILLEGAL_CHARACTERS_RE = re.compile('[\\000-\\010]|[\\013-\\014]|[\\016-\\037]')
    paigong_resp = ILLEGAL_CHARACTERS_RE.sub('', paigong_resp)
    out0 = paigong_resp.replace('","', 'ZWQ').replace('"', '').split('\r\n')
    pp = []
    for i in out0:
        pp.append(i.split('ZWQ'))

    Nps = pandas.DataFrame(pp)
    columus = Nps.loc[1].tolist()
    Nps.columns = columus
    Nps = Nps[((Nps['推荐主要原因'] == '服务') & (Nps['工单类型'] != '投诉工单') & (Nps['服务类型'] != '鉴定') & (
    (Nps['推荐分值'] == '0') | (Nps['推荐分值'] == '1') | (Nps['推荐分值'] == '2') | (Nps['推荐分值'] == '3') | (Nps['推荐分值'] == '4') | (
    Nps['推荐分值'] == '5') | (Nps['推荐分值'] == '6') | (Nps['推荐分值'] == '7') | (Nps['推荐分值'] == '8') | (Nps['推荐分值'] == '9') | (
    Nps['推荐分值'] == '10')))]
    Nps['推荐分值'] = pandas.to_numeric((Nps['推荐分值']), errors='ignore')
    Nps['回访日期'] = start
    print(Nps)
    show_progress(0)
    if len(Nps) > 0:
        thread_it(print_ui, 2, Nps.loc[:, ['工单编号', '推荐分值']])
    return Nps


@retry()
def getJdl(account, union_param):
    b = robobrowser.RoboBrowser(parser='lxml')
    b.open('http://crm.hisense.com/HisenseCRM/login.do?method=begin')
    f = b.get_form(action='/HisenseCRM/j_unieap_security_check.do')
    f['j_username'].value = account[0]
    f['j_password'].value = account[1]
    b.submit_form(f)
    crmuuid = str(uuid.uuid4())
    out0 = b.session.post((
                          'http://crm.hisense.com/HisenseReport/Report-CsvAction.do?linage=20&district=20&reportId=215869db-c62d-4c09-a74c-3ae65edf8a96&ctype=1&unieap_report_params=' + union_param + '&isResultant=false&newReport=null&cachedId=' + crmuuid + '&multiDataSegment=true&segmentNumber=null&segmentPosition=null&segmentPage=null&segmentPagesCount=null&parentId=&newName=&caption=null&changePageCount=1&drillThroughContext=&UniEAP_Report_olapcontext=null&excelExporterType=0&goto_page_number=1&ctype=null&all=false&needProgressBar=false'),
                          headers={'Referer': 'http://crm.hisense.com/HisenseReport/Report-ResultAction.do'},
                          allow_redirects=False)
    paigong_resp = out0.text
    ILLEGAL_CHARACTERS_RE = re.compile('[\\000-\\010]|[\\013-\\014]|[\\016-\\037]')
    paigong_resp = ILLEGAL_CHARACTERS_RE.sub('', paigong_resp)
    out0 = paigong_resp.replace('","', 'ZWQ').replace('"', '').split('\r\n')
    pp = []
    for i in out0:
        pp.append(i.split('ZWQ'))

    Jdl = pandas.DataFrame(pp)
    columus = Jdl.loc[1].tolist()
    Jdl.columns = columus
    print(Jdl)
    Jdl = Jdl[((Jdl['子公司'] == '家电总部') | (Jdl['子公司'] == '股份总部') | (Jdl['子公司'] == '广东厨电公司') | (Jdl['子公司'] == '通信公司总部'))]
    yestday = get_Date()
    Jdl['序号'] = yestday
    return Jdl


def jdl(account, if_az, if_cancle, pro_type):
    pro_type_list = str(pro_type).split(',')
    out = pandas.DataFrame()
    for i in pro_type_list:
        para_str_list = '{"timeEnd":"","if_az1":"' + if_az + '","require_to":"","unireport_biz_params":"{\\"server\\":\\"\\",\\"serverMode\\":\\"\\",\\"method\\":\\"execute\\",\\"reportId\\":\\"215869db-c62d-4c09-a74c-3ae65edf8a96\\",\\"repair_name\\":\\"\\",\\"cache_logo_id_q\\":\\"\\",\\"prodType\\":\\"\\",\\"if_az\\":\\"\\",\\"if_service_times1\\":\\"0\\",\\"if_cancel\\":\\"\\",\\"IF_WARRANT\\":\\"\\",\\"branch_name\\":\\"\\",\\"SERVICE_TYPE\\":\\"\\"}","serverMode1":"","ringback_start":"","ringback_to":"","prodType1":"' + i + '","num":"1","IF_WARRANT1":"","if_cancel1":"' + if_cancle + '","repair_code":"","server1":"","require_start":"","timeStart":"","branch_id":"","Search":"","perCount":"","settleMonth":"","cache_logo_id1":"","SERVICE_TYPE1":""}'
        bytes_url = para_str_list.encode('utf-8')
        str_url = base64.b64encode(bytes_url)
        union_param = str(str_url).lstrip("b'")
        print(union_param)
        out1 = getJdl(account, union_param)
        if len(out1) > 1:
            thread_it(print_ui, 3, out1.loc[:, ['单据编号']])
        out = out.append(out1, ignore_index=True)

    out['服务周期'] = pandas.to_numeric((out['服务周期']), errors='ignore')
    JDL = out.drop_duplicates(['单据编号'])
    show_progress(0)
    return JDL


@retry()
def getpaigong(account, selectTime):
    print('派工')
    b = robobrowser.RoboBrowser(parser='lxml')
    b.open('http://crm.hisense.com/HisenseCRM/login.do?method=begin')
    f = b.get_form(action='/HisenseCRM/j_unieap_security_check.do')
    f['j_username'].value = account[0]
    f['j_password'].value = account[1]
    b.submit_form(f)
    str_encrypt = json.dumps({'endtime': selectTime, 'product_id': '', 'state': selectTime,
                              'stateN': '', 'is_saiwei': ''})
    paigong = base64.b64encode(str_encrypt.encode('utf-8'))
    paigong = str(paigong).lstrip("b'")
    crmuuid = str(uuid.uuid4())
    out0 = b.session.post((
                          'http://crm.hisense.com/HisenseReport/Report-CsvAction.do?linage=20&reportId=ccbc3297-4317-4941-ad0d-77c3c236be41&ctype=1&unieap_report_params=' + paigong + '&isResultant=false&newReport=null&cachedId=' + crmuuid + '&multiDataSegment=false&segmentPosition=null&segmentPage=null&segmentPagesCount=null&caption=null&changePageCount=1&UniEAP_Report_olapcontext=null&excelExporterType=0&goto_page_number=1&ctype=null&all=false&needProgressBar=false'),
                          headers={'Referer': 'http://crm.hisense.com/HisenseReport/Report-ResultAction.do'},
                          allow_redirects=False)
    paigong_resp = out0.text
    out0 = paigong_resp.replace('"', '').replace(' ', '').split('\r\n')
    pp = []
    for i in out0:
        pp.append(i.split(','))

    pp = pandas.DataFrame(pp).drop(0).drop(axis=1, columns=0)
    pp = pp.drop(len(pp)).drop(len(pp) - 1)
    pp.columns = list(pp.iloc[0][:])
    pp = pp.drop(1).replace('', method='pad')
    pp['安装量'] = pandas.to_numeric((pp['安装量']), errors='ignore')
    pp['维修量'] = pandas.to_numeric((pp['维修量']), errors='ignore')
    pp['总计'] = pandas.to_numeric((pp['总计']), errors='ignore')
    pp = pp.reset_index(drop=True)
    pp.index = pp.index + 1
    show_progress(0)
    return pp


@retry()
def getByl(account, start, end):
    print('BYL')
    b = robobrowser.RoboBrowser(parser='lxml')
    b.open('http://crm.hisense.com/HisenseCRM/login.do?method=begin')
    f = b.get_form(action='/HisenseCRM/j_unieap_security_check.do')
    f['j_username'].value = account[0]
    f['j_password'].value = account[1]
    b.submit_form(f)
    str_encrypt = json.dumps({'cache_timeEnter': '', 'cache_enterStart': start, 'cache_enterEnd': end,
                              'cache_enterStart1': '', 'cache_enterEnd1': ''})
    paigong = base64.b64encode(str_encrypt.encode('utf-8'))
    paigong = str(paigong).lstrip("b'")
    crmuuid = str(uuid.uuid4())
    out0 = b.session.post((
                          'http://crm.hisense.com/HisenseReport/Report-CsvAction.do?linage=20&district=20&reportId=e3f154ad-f7db-40b0-9a86-32b4ecd77000&ctype=1&unieap_report_params=' + paigong + '&isResultant=false&newReport=null&cachedId=' + crmuuid + '&multiDataSegment=true&segmentNumber=null&segmentPosition=null&segmentPage=null&segmentPagesCount=null&parentId=&newName=&caption=null&changePageCount=1&drillThroughContext=&UniEAP_Report_olapcontext=null&excelExporterType=0&goto_page_number=1&ctype=null&all=false&needProgressBar=false'),
                          headers={'Referer': 'http://crm.hisense.com/HisenseReport/Report-ResultAction.do'},
                          allow_redirects=False)
    paigong_resp = out0.text
    ILLEGAL_CHARACTERS_RE = re.compile('[\\000-\\010]|[\\013-\\014]|[\\016-\\037]')
    paigong_resp = ILLEGAL_CHARACTERS_RE.sub('', paigong_resp)
    out0 = paigong_resp.replace('","', 'ZWQ').replace('"', '').split('\r\n')
    pp = []
    for i in out0:
        pp.append(i.split('ZWQ'))

    Byl = pandas.DataFrame(pp)
    columus = Byl.loc[2].tolist()
    Byl.columns = columus
    Byl = Byl[((Byl['子公司'] == '家电总部') | (Byl['子公司'] == '股份总部'))]
    Byl = Byl.reset_index(drop=True)
    Byl.index = Byl.index + 1
    if len(Byl) > 0:
        thread_it(print_ui, 1, Byl.loc[:, ['信息编号']])
    show_progress(0)
    return Byl


@retry()
def gd_yujing_data(account, starttime, endtime, cache_row_id, product_id, service_type_id, wb_type, is_finished):
    b = robobrowser.RoboBrowser(parser='lxml')
    b.open('http://crm.hisense.com/HisenseCRM/login.do?method=begin')
    f = b.get_form(action='/HisenseCRM/j_unieap_security_check.do')
    f['j_username'].value = account[0]
    f['j_password'].value = account[1]
    b.submit_form(f)
    out1 = pandas.DataFrame()
    header1 = {'Referer': 'http://crm.hisense.com/HisenseCRM/BeforehandNotice.do?method=doExcelCount'}
    data = {'cache_row_id': cache_row_id, 'cache_delay_start': starttime,
            'cache_delay_to': endtime,
            'cache_product_id': product_id,
            'cache_service_type_id': service_type_id,
            'cache_wb_type': wb_type,
            'cache_is_finished': is_finished}
    for i in range(1, 20):
        out0 = b.session.post(
            ('http://crm.hisense.com/HisenseCRM/BeforehandNotice.do?method=exportExcel&page=' + str(i)),
            headers=header1,
            data=data,
            allow_redirects=False)
        out2 = pandas.read_html((out0.text), header=0, skiprows=1)
        out2 = pandas.DataFrame(out2[0])
        if len(out2) == 0:
            print('完成换参数----' + str(i))
            break
        else:
            out1 = out1.append(out2, ignore_index=True)
            print('这个参数里的数据有点多啊')

    show_progress(0)
    return out1


def get_unfinshed_param_control(account, starttime, endtime, cache_row_id, sv_product, sv_service_type, sv_wb_type,
                                sv_is_finished):
    cache_product_id = str(sv_product).split(',')
    out = pandas.DataFrame()
    print('工单预警')
    for product_id in cache_product_id:
        out1 = gd_yujing_data(account, starttime, endtime, cache_row_id, product_id, sv_service_type, sv_wb_type,
                              sv_is_finished)
        if len(out1) > 0:
            thread_it(print_ui, 4, out1.loc[:, ['信息编号']])
        out = out.append(out1, ignore_index=True)

    allUnfinished = out.drop_duplicates(['信息编号'])
    return allUnfinished


@retry()
def gd_chaxun_data(account, starttime, endtime, cache_row_id, product_id, service_type_id, wb_type):
    print('chaxun')
    b = robobrowser.RoboBrowser(parser='lxml')
    b.open('http://crm.hisense.com/HisenseCRM/login.do?method=begin')
    f = b.get_form(action='/HisenseCRM/j_unieap_security_check.do')
    f['j_username'].value = account[0]
    f['j_password'].value = account[1]
    b.submit_form(f)
    out1 = pandas.DataFrame()
    b.open('http://crm.hisense.com/HisenseCRM/login.do?method=login')
    b.open('http://crm.hisense.com/HisenseCRM/loginext.do?method=login')
    b.open('http://crm.hisense.com/HisenseCRM/main/pages/indexCRMLink.jsp')
    for i in range(1, 20):
        out0 = b.session.post(('http://crm.hisense.com/HisenseCRM/QueryWb.do?method=doExcel&page=' + str(
            i) + '&cache_row_id=' + cache_row_id + '&cache_second_org=H-JD-00' + '&cache_enter_time_start=' + starttime + '+00%3A00&cache_enter_time_end=' + endtime + '+23%3A59&cache_service_type_id=' + service_type_id + '&cache_product_catalog_id=' + product_id + '&cache_wb_type=' + wb_type),
                              headers={'Referer': 'http://crm.hisense.com/HisenseCRM/QueryWb.do?method=doQueryExcel'},
                              allow_redirects=False)
        out2 = pandas.read_html((out0.text), header=0, skiprows=1)
        out2 = pandas.DataFrame(out2[0])
        if len(out2) == 0:
            print('完成换参数----' + str(i))
            break
        else:
            thread_it(print_ui, 1, out2.loc[:, ['信息编号']])
            out1 = out1.append(out2, ignore_index=True)

    show_progress(0)
    return out1

# okay decompiling .\requests_robot.pyc
