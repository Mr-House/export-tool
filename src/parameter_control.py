# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: parameter_control.py
from requests_robot import getnps, jdl, getpaigong, getByl, get_unfinshed_param_control, gd_chaxun_data
from pipei_file import pipei, to_excel, print_ui
from set_time_path import get_Date, get_Last27, get_Path, thread_it
import pandas, numpy
from main_ui import test, set_button, show_progress
import threading


def parameter_control(account, model_parameters, model_id):
    parameters_list = model_parameters[model_id].to_list()
    yestday = get_Date()
    print(yestday)
    byl_thread = threading.Thread(target=byl_model, args=(account, parameters_list, yestday))
    byl_thread.setDaemon(True)
    byl_thread.start()
    nps_thread = threading.Thread(target=nps_model, args=(account, parameters_list, yestday))
    nps_thread.setDaemon(True)
    nps_thread.start()
    jdl_thread = threading.Thread(target=jdl_modle, args=(account, parameters_list, yestday))
    jdl_thread.setDaemon(True)
    jdl_thread.start()
    gdyujing_thread = threading.Thread(target=gdyujing_model, args=(account, parameters_list, yestday))
    gdyujing_thread.setDaemon(True)
    gdyujing_thread.start()
    paigong_thread = threading.Thread(target=paigong_model, args=(account, parameters_list, yestday))
    paigong_thread.setDaemon(True)
    paigong_thread.start()
    gdchaxun_thread = threading.Thread(target=gdchaxun_model, args=(account, parameters_list, yestday))
    gdchaxun_thread.setDaemon(True)
    gdchaxun_thread.start()
    byl_thread.join()
    nps_thread.join()
    jdl_thread.join()
    gdyujing_thread.join()
    paigong_thread.join()
    gdchaxun_thread.join()


def thread_control(account, model_parameters, model_id):
    global mmm
    mmm = model_id
    from main_ui import callback_end, count_time
    count_how_time = threading.Thread(target=count_time)
    count_how_time.start()
    main_thread0 = threading.Thread(target=parameter_control, args=(account, model_parameters, model_id))
    main_thread0.start()
    main_thread0.join()
    print('子线程结束')
    data_candle_model(model_id, pp, allUnfinished, nps, byl, jdl_data, chaxun_data)
    set_button()
    callback_end()


def paigong_model(account, parameters_list, yestday):
    global pp
    pp = pandas.DataFrame()
    if parameters_list[17] == '1':
        pp = getpaigong(account, yestday)
        print(pp)
        pp = pipei(pp, parameters_list[18])
        to_excel(pp, yestday + '-' + mmm + '-派工量')
    else:
        if parameters_list[17] == '0':
            thread_it(test, '派工量：不执行此模块')
    show_progress(0)
    return pp


def jdl_modle(account, parameters_list, yestday):
    global jdl_data
    jdl_data = pandas.DataFrame()
    if parameters_list[25] == '1':
        threads_zhiliang = []
        cache_product_id = str(parameters_list[26]).split(',')
        count_thread = range(len(cache_product_id))
        for i in count_thread:
            t_zhiliang = MyThread(jdl, args=(account, parameters_list[27], parameters_list[28], cache_product_id[i]))
            t_zhiliang.setDaemon(True)
            t_zhiliang.start()
            threads_zhiliang.append(t_zhiliang)

        for i in count_thread:
            threads_zhiliang[i].join()
            jdl_data = jdl_data.append(threads_zhiliang[i].get_result())

        if parameters_list[29] != '':
            jdl_data = pipei(jdl_data, parameters_list[29])
    elif parameters_list[25] == '0':
        thread_it(test, '质量报表：不执行此模块')
    show_progress(0)
    return jdl_data


def byl_model(account, parameters_list, yestday):
    print('==byl_model start==')
    print('parameters_list 20=' + parameters_list[20])
    print('parameters_list 21=' + parameters_list[21])
    print('parameters_list 23=' + parameters_list[23])
    global byl
    byl = pandas.DataFrame()
    # todo
    if parameters_list[20] == '1':
        if parameters_list[21] == '0':
            a = get_Last27()
            byl = getByl(account, a, yestday)
            if parameters_list[23] != '':
                byl = pipei(byl, parameters_list[23])
        elif parameters_list[21] == '1':
            byl = getByl(account, yestday, yestday)
            if parameters_list[23] != '':
                byl = pipei(byl, parameters_list[23])
                byl = byl.drop_duplicates(['信息编号'])
                byl['投诉安维类型'] = byl['投诉内容'].apply(lambda x: '安装' if '安装' in x else '维修')
        to_excel(byl, yestday + '-' + mmm + '-抱怨明细')
    else:
        if parameters_list[20] == '0':
            thread_it(test, '抱怨率表：不执行此模块')
    show_progress(0)
    print('==byl_model end==')
    return byl


def gdyujing_model(account, parameters_list, yestday):
    global allUnfinished
    allUnfinished = pandas.DataFrame()
    if parameters_list[0] == '1':
        threads_gdyujing = []
        cache_product_id = str(parameters_list[4]).split(',')
        count_thread = range(len(cache_product_id))
        for i in count_thread:
            t_gd = MyThread(get_unfinshed_param_control, args=(
                account, parameters_list[2], parameters_list[3], parameters_list[1], cache_product_id[i],
                parameters_list[5], parameters_list[6],
                parameters_list[7]))
            t_gd.setDaemon(True)
            t_gd.start()
            threads_gdyujing.append(t_gd)

        for i in count_thread:
            threads_gdyujing[i].join()
            allUnfinished = allUnfinished.append(threads_gdyujing[i].get_result())

        if parameters_list[8] != '':
            allUnfinished = pipei(allUnfinished, parameters_list[8])
        allUnfinished = allUnfinished.drop_duplicates(['信息编号'])
        to_excel(allUnfinished, mmm + '今日-待修明细')
    else:
        if parameters_list[0] == '0':
            thread_it(test, '工单预警：不执行此模块')
        show_progress(0)
        return allUnfinished


def gdchaxun_model(account, parameters_list, yestday):
    global chaxun_data
    chaxun_data = pandas.DataFrame()
    if parameters_list[31] == '1':
        a = ''
        b = ''
        if parameters_list[33] == '1':
            a = get_Date()
        if parameters_list[34] == '1':
            b = get_Date()
        threads_gdyujing = []
        cache_product_id = str(parameters_list[35]).split(',')
        count_thread = range(len(cache_product_id))
        for i in count_thread:
            print(cache_product_id[i])
            t_gdcx = MyThread(gd_chaxun_data, args=(
                account, a, b, parameters_list[32], cache_product_id[i], parameters_list[36], parameters_list[37]))
            t_gdcx.setDaemon(True)
            t_gdcx.start()
            threads_gdyujing.append(t_gdcx)

        for i in count_thread:
            threads_gdyujing[i].join()
            chaxun_data = chaxun_data.append(threads_gdyujing[i].get_result())

        print(len(chaxun_data))
        if len(chaxun_data) > 0 and parameters_list[38] != '':
            chaxun_data = pipei(chaxun_data, parameters_list[38])
            chaxun_data = chaxun_data.drop_duplicates(['信息编号'])
            to_excel(chaxun_data, yestday + '-' + mmm + '-工单综合查询')
    elif parameters_list[31] == '0':
        thread_it(test, '工单查询：不执行此模块')
    show_progress(0)
    return chaxun_data


def nps_model(account, parameters_list, yestday):
    global nps
    nps = pandas.DataFrame()
    if parameters_list[10] == '1':
        nps = getnps(account, yestday, yestday)
        if parameters_list[15] != '':
            nps = pipei(nps, parameters_list[15])
        nps.drop_duplicates(['工单编号'])
        to_excel(nps, yestday + mmm + '-NPS明细')
    else:
        if parameters_list[10] == '0':
            thread_it(test, 'NPS：不执行此模块')
    show_progress(0)
    return nps


# todo
def data_candle_model(model_id, pp, allUnfinished, nps, byl, jiedan, chaxun_data):
    print('==data_candle_model start==')
    date_re = get_Date()
    connectTable = pandas.read_excel('connectTable.xlsx')
    fgs = pandas.DataFrame(connectTable['赛维'].drop_duplicates()).dropna()
    fgs = fgs.set_index(['赛维'])
    show_progress(91)
    pg = fgs.copy()
    outRangeSevenCount = fgs.copy()
    nps_pivo = fgs.copy()
    outRange = fgs.copy()
    an_jiedan_pivo = fgs.copy()
    wx_jiedan_pivo = fgs.copy()
    chaxun_pivo = fgs.copy()
    byl_pivo = fgs.copy()
    print('数据处理')
    show_progress(92)
    print('pp=' + pp)
    if len(pp) > 0:
        pp = pp.copy()
        pg = pandas.pivot_table(pp, index=['赛维'], values=['安装量', '维修量'], columns=['合并产品大类'], aggfunc=[numpy.sum], fill_value=0, margins=False)
    else:
        show_progress(93)
        if len(allUnfinished) > 0:
            todayUnfinished = allUnfinished[((allUnfinished['工单类型'] == '普通工单') | (allUnfinished['工单类型'] == '投诉工单'))].copy()
            complaintMessage = allUnfinished[((allUnfinished['工单类型'] == '投诉信息') & (allUnfinished['分公司反馈完成'] == '否') & (allUnfinished['投诉分类'] != '用户体验'))].copy()
            pending_reason_data = allUnfinished[((allUnfinished['延迟天数'] >= 7) & (allUnfinished['要求服务类型'] != '安装') & (allUnfinished['要求服务类型'] != '投诉') & (allUnfinished['要求服务类型'] != '咨询'))].copy()
            if model_id == '厨卫日报':
                if len(todayUnfinished) > 0:
                    todayUnfinished = todayUnfinished.copy()
                    todayUnfinished['待修总量'] = todayUnfinished['延迟天数'].apply(lambda x: 1 if x >= 0 else 0)
                    todayUnfinished['待修超3'] = todayUnfinished['延迟天数'].apply(lambda x: 1 if x > 3 else 0)
                    todayUnfinished['待修超5'] = todayUnfinished['延迟天数'].apply(lambda x: 1 if x > 5 else 0)
                    todayUnfinished['待修超7'] = todayUnfinished['延迟天数'].apply(lambda x: 1 if x > 7 else 0)
                    todayUnfinished['待修超15'] = todayUnfinished['延迟天数'].apply(lambda x: 1 if x > 15 else 0)
                    todayUnfinished['安维类型'] = todayUnfinished['要求服务类型'].apply(lambda x: '安装' if x == '安装' else'维修')
                    todayUnfinished = pandas.DataFrame(todayUnfinished).drop_duplicates(['信息编号'])
                    todayUnfinished = pandas.DataFrame(todayUnfinished)
                    outRangeSevenCount = pandas.pivot_table(todayUnfinished, index=['赛维'], columns=['安维类型', '合并产品大类'], values=['待修总量', '待修超3', '待修超5', '待修超7', '待修超15'], aggfunc=[numpy.sum], fill_value=0, margins=False)
                else:
                    if len(todayUnfinished) > 0:
                        todayUnfinished = todayUnfinished.copy()
                        todayUnfinished['待修总量'] = todayUnfinished['延迟天数'].apply(lambda x: 1 if x >= 0 else 0)
                        todayUnfinished['待修超3'] = todayUnfinished['延迟天数'].apply(lambda x: 1 if x >= 3 else 0)
                        todayUnfinished['待修超5'] = todayUnfinished['延迟天数'].apply(lambda x: 1 if x >= 5 else 0)
                        todayUnfinished['待修超7'] = todayUnfinished['延迟天数'].apply(lambda x: 1 if x >= 7 else 0)
                        todayUnfinished['待修超15'] = todayUnfinished['延迟天数'].apply(lambda x: 1 if x >= 15 else 0)
                        todayUnfinished['安维类型'] = todayUnfinished['要求服务类型'].apply(lambda x: '安装' if x == '安装' else '维修')
                        todayUnfinished = pandas.DataFrame(todayUnfinished).drop_duplicates(['信息编号'])
                        todayUnfinished = pandas.DataFrame(todayUnfinished)
                        outRangeSevenCount = pandas.pivot_table(todayUnfinished, index=['赛维'], columns=['安维类型', '合并产品大类'], values=['待修总量', '待修超3', '待修超5', '待修超7', '待修超15'], aggfunc=[numpy.sum], fill_value=0, margins=False)
                    if len(pending_reason_data) > 0:
                        import openpyxl
                        data = openpyxl.load_workbook('test.xlsx')
                        table = data.get_sheet_by_name('明细')
                        from openpyxl.utils.dataframe import dataframe_to_rows
                        rows_paigong = dataframe_to_rows(pending_reason_data, index=False)
                        for r_idx, row in enumerate(rows_paigong, 1):
                            for c_idx, value in enumerate(row, 1):
                                table.cell(row=r_idx, column=c_idx, value=value)

                        cwd = get_Path()
                        data.save(cwd + '/' + '未完成原因明细及透视.xlsx')
            if model_id == '待修日报':
                thread_it(get_weather)
                if len(complaintMessage) > 0:
                    complaintMessage = complaintMessage.copy()
                    complaintMessage['投诉信息总量'] = complaintMessage['延迟天数'].apply(lambda x: 1 if x >= 0 else 0)
                    complaintMessage['投诉信息超3'] = complaintMessage['延迟天数'].apply(lambda x: 1 if x >= 3 else 0)
                    complaintMessage['投诉信息超5'] = complaintMessage['延迟天数'].apply(lambda x: 1 if x >= 5 else 0)
                    complaintMessage['投诉信息超15'] = complaintMessage['延迟天数'].apply(lambda x: 1 if x >= 15 else 0)
                    complaintMessage = pandas.DataFrame(complaintMessage).drop_duplicates(['信息编号'])
                    complaintMessage = pandas.DataFrame(complaintMessage)
                    outRange = pandas.pivot_table(complaintMessage, index=['赛维'], columns=['合并产品大类'], values=['投诉信息总量', '投诉信息超3', '投诉信息超5', '投诉信息超15'], aggfunc=[numpy.sum], fill_value=0, margins=False)
                    show_progress(94)
        if len(chaxun_data) > 0:
            if model_id == '':
                print('工单查询')
                print(chaxun_data)
                chaxun_data_n = chaxun_data.copy()
                chaxun_data_n = chaxun_data_n[(chaxun_data_n['计入厨卫'] == '是')].copy()
                chaxun_data_n['工单查询'] = chaxun_data_n['信息编号'].apply(lambda x: 1 if len(x) > 0 else 0)
                chaxun_data_n = pandas.DataFrame(chaxun_data_n).drop_duplicates(['信息编号'])
                chaxun_data_n = pandas.DataFrame(chaxun_data_n)
                chaxun_pivo = pandas.pivot_table(chaxun_data_n, index=['赛维'], columns=['合并产品大类'], values=['工单查询'], aggfunc=[numpy.sum], fill_value=0, margins=False)
            else:
                print('工单查询')
                print(chaxun_data)
                chaxun_data_n = chaxun_data.copy()
                chaxun_data_n['工单查询'] = chaxun_data_n['信息编号'].apply(lambda x: 1 if len(x) > 0 else 0)
                chaxun_data_n = pandas.DataFrame(chaxun_data_n).drop_duplicates(['信息编号'])
                chaxun_data_n = pandas.DataFrame(chaxun_data_n)
                chaxun_pivo = pandas.pivot_table(chaxun_data_n, index=['赛维'], columns=['合并产品大类'], values=['工单查询'], aggfunc=[numpy.sum], fill_value=0, margins=False)
                show_progress(95)
        if len(byl) > 0:
            if model_id == '服务质量日报':
                byl = byl[(byl['计入抱怨率'] == '是')].copy()
                byl['抱怨率'] = byl['信息编号'].apply(lambda x: 1 if len(x) > 0 else 0)
                byl = pandas.DataFrame(byl).drop_duplicates(['信息编号'])
                byl = pandas.DataFrame(byl)
                byl_pivo = pandas.pivot_table(byl, index=['赛维'], columns=['合并产品大类', '投诉安维类型'], values=['抱怨率'], aggfunc=[numpy.sum], fill_value=0, margins=False)
            else:
                if model_id == '待修日报':
                    byl = byl[((byl['投诉分类'] != '用户体验') & (byl['投诉分类'] != '用户体验类') & (byl['投诉分类'] != '用户体验差'))].copy()
                    byl['抱怨率'] = byl['信息编号'].apply(lambda x: 1 if len(x) > 0 else 0)
                    byl = pandas.DataFrame(byl).drop_duplicates(['信息编号'])
                    byl = pandas.DataFrame(byl)
                    byl_pivo = pandas.pivot_table(byl, index=['赛维'], columns=['合并产品大类', '投诉安维类型'], values=['抱怨率'], aggfunc=[numpy.sum], fill_value=0, margins=False)
                    show_progress(96)
        if len(nps) > 0:
            nps_data = nps.copy()
            nps_data = nps_data[((nps_data['工单类型'] != '投诉工单') & (nps_data['具体原因'] != '话务环节'))].copy()
            nps_data['NPS'] = nps_data['工单类型'].apply(lambda x: 1 if len(x) > 0 else 0)
            nps_data = pandas.DataFrame(nps_data).drop_duplicates(['工单编号'])
            nps_data = pandas.DataFrame(nps_data)
            nps_pivo = pandas.pivot_table(nps_data, index=['赛维'], columns=['合并产品大类', '用户类型'], values=['NPS'], aggfunc=[numpy.sum], fill_value=0, margins=False)
            show_progress(97)
        if len(jiedan) > 0:
            an_jiedan = jiedan[(jiedan['维修类型'] == '安装')].copy()
            to_excel(an_jiedan, mmm + date_re + '-安装结单量明细')
            if len(an_jiedan) > 0:
                an_jiedan = an_jiedan.copy()
                an_jiedan['安装结单'] = an_jiedan['单据编号'].apply(lambda x: 1 if len(x) > 0 else 0)
                an_jiedan['安装结单超3'] = an_jiedan['服务周期'].apply(lambda x: 1 if x > 3 else 0)
                an_jiedan['安装结单超5'] = an_jiedan['服务周期'].apply(lambda x: 1 if x > 5 else 0)
                an_jiedan['安装结单超7'] = an_jiedan['服务周期'].apply(lambda x: 1 if x > 7 else 0)
                an_jiedan = pandas.DataFrame(an_jiedan).drop_duplicates(['单据编号'])
                an_jiedan = pandas.DataFrame(an_jiedan)
                an_jiedan_pivo = pandas.pivot_table(an_jiedan, index=['赛维'], columns=['合并产品大类'], values=['安装结单', '安装结单超3', '安装结单超5', '安装结单超7'], aggfunc=[numpy.sum], fill_value=0, margins=False)
                show_progress(98)
        if len(jiedan) > 0:
            wx_jiedan = jiedan[(jiedan['维修类型'] != '安装')].copy()
            to_excel(wx_jiedan, mmm + date_re + '-维修结单量明细')
            if len(wx_jiedan) > 0:
                wx_jiedan = wx_jiedan.copy()
                wx_jiedan['维修结单'] = wx_jiedan['单据编号'].apply(lambda x: 1 if len(x) > 0 else 0)
                wx_jiedan['维修结单超3'] = wx_jiedan['服务周期'].apply(lambda x: 1 if x > 3 else 0)
                wx_jiedan['维修结单超5'] = wx_jiedan['服务周期'].apply(lambda x: 1 if x > 5 else 0)
                wx_jiedan['维修结单超7'] = wx_jiedan['服务周期'].apply(lambda x: 1 if x > 7 else 0)
                wx_jiedan = pandas.DataFrame(wx_jiedan).drop_duplicates(['单据编号'])
                wx_jiedan = pandas.DataFrame(wx_jiedan)
                wx_jiedan_pivo = pandas.pivot_table(wx_jiedan, index=['赛维'], columns=['合并产品大类'], values=['维修结单', '维修结单超3', '维修结单超5', '维修结单超7'], aggfunc=[numpy.sum], fill_value=0, margins=False)
                show_progress(99)

        end_table = fgs.join([pg, outRangeSevenCount, nps_pivo, outRange, byl_pivo, an_jiedan_pivo, wx_jiedan_pivo, chaxun_pivo])
        colums_end = end_table.columns.tolist()
        colums_end_now = []
        for i in colums_end:
            i_r_sum_len = str(i).replace("'sum',", '').replace("'", '').replace(',', '-').replace('(','').replace(')', '').replace(' ', '')
            colums_end_now.append(i_r_sum_len)

        cwd = get_Path()
        thread_it(print_ui, 1, end_table)
        end_table.to_excel((cwd + '\\' + model_id + '-今日汇总透视表.xlsx'), header=colums_end_now)
        print('\t————————结束 ！请退出—————————')
        show_progress(100)


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = (self.func)(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return


def get_weather():
    import robobrowser, re
    b = robobrowser.RoboBrowser(parser='lxml')
    b.open('http://www.weather.com.cn/index/zxqxgg1/new_wlstyb.shtml')
    m = re.findall('<!-- 文字展示 start-->(.+?)<!-- 文字展示 end-->', str(b.find_all), re.S)
    out = re.sub('<.*?>', '', m[0].replace('</p>', '\n'))
    out = re.sub('\n图.*?）', '', out)
    out = re.sub('（见图.*?）', '', out)
    out = re.sub('制作.*?\n', '', out)
    out = out.replace('\n\n', '\n')
    from set_time_path import get_Path
    cwd = get_Path()
    f1 = open(cwd + '/' + '天气状况.txt', 'w')
    f1.write(out)
    f1.close()

# okay decompiling .\parameter_control.pyc
