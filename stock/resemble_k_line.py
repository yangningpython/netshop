import json
from django.db import connection
from datetime import *
import time as tm

from pandas import Timestamp

import stock.connectDB as conndb
import numpy as np
import pandas as pd
import os
import tushare as ts
import gc
pd.set_option("display.max_rows",None)

def gettradedays(days):
    '''

    :param n: 总共获取多少天的交易日期
    :param enddate: 结束日期
    :return: 返回n个交易日日期列表
    '''
    nowdate = datetime.now()
    # enddate=nowdate+timedelta(days=-days+1)
    enddate = nowdate.strftime("%Y%m%d")
    print(enddate)
    pro = ts.pro_api(token="f39d6551514a1a00780149004dd8f77bf328d9d68a3d197598bfb6dd")
    date = pro.query('trade_cal', start_date="20200504", end_date=enddate).sort_values(by=['cal_date'],ascending=True)
    date.reset_index(inplace=True)
    #print(date)
    date_list = []
    # print(date)
    # 获取行start_date=now_date,
    for i in range(0, len(date)):
        if date.loc[i, 'is_open'] == 1:
            datestr = datetime.strptime(date.loc[i, 'cal_date'], "%Y%m%d")
            datestr = datestr.strftime("%Y-%m-%d")
            date_list.append(str(datestr))
    #print(date_list,-days)
    return date_list[-days]


def df_norm(df, *cols):
    df_n = df.copy()
    for col in cols:
        ma = df_n[col].max()
        mi = df_n[col].min()
        df_n[col + '_n'] = (df_n[col] - mi) / (ma - mi)
    return (df_n)



# df_norm = df_norm(df,'col1')
# print(df_norm)


def resemble_k(security, startdate, enddate, days,conn=None):
    # cur.execute("""select rq,dm,mz,dqjg,jtkp,zgj,zdj,cjl,cje,ltsz from stock_zx where dm="600511";""")
    # result=cur.fetchall()
    # datelist=np.array([np.datetime64(result[0]) for result in result])
    path = "./stockdata/origin_data.csv"
    origin_source = "db"
    tradedates = gettradedays(days)
    #print(conn)
    if conn==None:
        connobj = conndb.ConnectDB()
        conn, cur = connobj.connectmysql()
    else:
        cur=conn.cursor()
    cur.execute("""select symbol from stock.stockinfo ;""")
    stock_num = len(cur.fetchall())
    sqlcmd = """select rq,dm,mz,dqjg,jtkp,zgj,zdj,zdbfb,zf,ma5,ma10,ma30,ma20,cjl,cje,case when ltsz="" then 0 else ltsz end as ltsz from stock.stock_zx where dm="%s" and rq>="%s" and rq<="%s" ;""" % (
        security, startdate, enddate)
    security_df = pd.read_sql(sqlcmd, conn)
    security_df['rq'] = security_df['rq'].astype('datetime64[ns]')
    #print(security_df)
    # pd.to_datetime(security_df["rq"],format = '%Y-%m-%d').dt.strftime('%Y-%m-%d')
    # security_df["rq"] = pd.to_datetime(security_df['rq'], yearfirst=True)
    security_df[["dm", "mz"]] = security_df[["dm", "mz"]].astype(str)
    security_df.loc[:, "dqjg":"ltsz"] = security_df.loc[:, "dqjg":"ltsz"].fillna(0).astype("float64")
    #security_df.loc[:, "dqjg":"ltsz"] = security_df.loc[:, "dqjg":"ltsz"].fillna(0).apply(pd.to_numeric)
    security_df.sort_values(by="rq", inplace=True)
    # 固定选取每个股多少条数据
    GROUPLINESSUM = security_df.index.max() + 1
    alllines = stock_num * (GROUPLINESSUM + 5)
    # sql语句
    sqlcmd = """select rq,dm,mz,dqjg,jtkp,zgj,zdj,zdbfb,zf,ma5,ma10,ma30,ma20,cjl,cje,case when ltsz="" then 0 else ltsz end as ltsz from stock.stock_zx where rq<="%s"  order by id desc limit %s ;""" % (
        tradedates, alllines)

    print(sqlcmd)
    result_df = pd.read_sql(sqlcmd, conn, parse_dates="rq")
    #print(result_df)
    result_df["rq"] = pd.to_datetime(result_df['rq'], yearfirst=True)
    result_df[["dm", "mz"]] = result_df[["dm", "mz"]].astype(str)
    #result_df.loc[:, "dqjg":"ltsz"] = result_df.loc[:, "dqjg":"ltsz"].fillna(0).apply(pd.to_numeric)
    result_df.sort_values(by="rq", inplace=True)
    result_df.drop(result_df.index[(result_df['cje'] == 0.0)], inplace=True)
    result_df.dropna(axis=0, how='any', inplace=True)
    result_df['rq'] = result_df['rq'].astype('datetime64[ns]')
    #print(result_df[result_df.isin([''])].stack())
    result_df.loc[:, "dqjg":"ltsz"] = result_df.loc[:, "dqjg":"ltsz"].fillna(0).astype("float64")
    allstock = result_df.groupby('dm').count() >= GROUPLINESSUM

    result_df = result_df[result_df["dm"].isin(list(allstock[allstock["rq"] == True].index))]
    result_df.sort_values(by="rq", ascending=False, inplace=True)

    result_df["cumcount"] = result_df.groupby('dm').cumcount()
    result_df = result_df[result_df['cumcount'] < GROUPLINESSUM]
    result_df.sort_values(['rq'], ascending=True, inplace=True)
    result_df["px"] = result_df.groupby(['dm']).cumcount() + 1
    indexlist = list(result_df[result_df["dm"] == security].index)
    security_df["index"] = indexlist
    security_df.set_index("index", inplace=True)
    result_df.update(security_df.loc[:, "rq":"ltsz"])

    # 重新排一次
    result_df["px"] = result_df.groupby(['dm']).cumcount() + 1
    min_value = result_df["px"].min()
    max_value = result_df["px"].max()
    min_date = result_df[result_df["px"] == min_value].loc[:, "rq":"dm"].set_index("dm", drop=True).to_dict()["rq"]
    max_date = result_df[result_df["px"] == max_value].loc[:, "rq":"dm"].set_index("dm", drop=True).to_dict()["rq"]
    x = [(i, j) for i, j in zip(list(min_date.values()), list(max_date.values()))]
    k_date_range_dic = dict(zip(list(min_date.keys()), x))
    # print(k_date_range_dic)

    result_df = result_df[["px", "dm", "dqjg", "zgj", "zdj", "zdbfb", "jtkp", "ma5"]]
    #print(result_df.dtypes)

    result_df = result_df.set_index(['px', 'dm']).unstack().reset_index(drop=True)
    #print(result_df)
    #print(result_df.dtypes)
    # zf_mean = result_df.mean().to_frame().T
    # zf_mean = zf_mean.loc[zf_mean.index.repeat(result_df.shape[0])].reset_index(drop=True)
    # zf_std = result_df.std().to_frame().T
    # zf_std = zf_std.loc[zf_std.index.repeat(result_df.shape[0])].reset_index(drop=True)
    # result_df = (result_df - zf_mean) / zf_std
    # result_df = result_df
    # dm_list = [tp[1] for tp in result_df.columns.values.tolist()]

    # result_df.columns=dm_list
    # result_df.index = result_df.index.rename('dm', level=1)  # 二级索引命命
    # result_df.name = 'dqjg'
    # result_df = result_df.reset_index()  # 将索引转化为Series
    # indexs = df._stat_axis.values.tolist()  # 行名称
    # result_df.columns.values.tolist()
    del indexlist,security_df,allstock
    gc.collect()
    corrclose = round((result_df["dqjg"].corr(method="pearson"))[security].astype("float64"),2)
    #print("占据内存约: {:.2f} GB".format(corrclose.memory_usage().sum()/ (1024**3)))
    corrhigh = round(result_df["zgj"].corr(method="pearson")[security].astype("float64"),2)
    corrlow = round(result_df["zdj"].corr(method="pearson")[security].astype("float64"),2)
    corropen = round(result_df["jtkp"].corr(method="pearson")[security].astype("float64"),2)
    # corrma20 = result_df["ma20"].corr(method="pearson")
    corrma5 = round(result_df["ma5"].corr(method="pearson")[security].astype("float64"),2)

    # corrcjl = result_df["cjl"].corr(method="pearson")
    # (value - value.mean()) / value.std()

    # corrzdbfb = result_df["zdbfb"].corr(method="pearson")
    # corrzf = result_df["zf"].corr(method="pearson")
    # mean_df=pd.DataFrame(result_df["zdbfb"].mean(),index=None,columns=result_df["zdbfb"].mean().index)
    # print(mean_df)
    # print(result_df["ma20"]["833819"])
    # corrclose=corrclose.dropna(how='any', inplace=True)
    # 最新三天相关系数
    finalCorr = (corrclose + corrhigh + corrlow + corrma5+corropen) / 5.0
    result_df_3 = result_df[-3:].reset_index(drop=True)

    del result_df,corrclose,corrhigh,corrlow,corrma5
    gc.collect()
    # print(result_df_3)
    corrclose3 = round(result_df_3["dqjg"].corr(method="pearson")[security].astype("float64"),2)
    corrhigh3 = round(result_df_3["zgj"].corr(method="pearson")[security].astype("float64"),2)
    corrlow3 = round(result_df_3["zdj"].corr(method="pearson")[security].astype("float64"),2)
    corropen3 = round(result_df_3["jtkp"].corr(method="pearson")[security].astype("float64"),2)
    # corrma203 = result_df_3["ma20"].corr(method="pearson"),2)
    corrma53 = round(result_df_3["ma5"].corr(method="pearson")[security].astype("float64"),2)
    finalCorr3 = (corrclose3 + corrhigh3  + corropen3 + corrma53+corrlow3) / 5.0
    del corrclose3,corrhigh3,corropen3,corrma53
    gc.collect()
    # 三日相关系数和全相关系数平均找出相似k线
    finalCorr = (finalCorr + finalCorr3) / 2
    #finalCorr = finalCorr[security]
    finalcorr = round(pd.Series(finalCorr).fillna(0).sort_values(ascending=False)[1:6],2).to_dict()
    #print(finalcorr)
    final_dict = {}
    for dm in finalcorr:
        final_dict[dm] = k_date_range_dic[dm] + (finalcorr[dm],)
    # print(final_dict)
    # final_dict数据
    # connobj = conndb.ConnectDB()
    # conn, cur = connobj.connectmysql()
    #
    # print(type(dic["300015"][1]))
    # dic={'300015': (Timestamp('2022-08-22 00:00:00'), Timestamp('2022-08-26 00:00:00'), 0.9139999747276306),}
    return_dic = {}
    for dm in final_dict:
        sqlcmd = """select rq,dm,mz,dqjg,jtkp,zgj,zdj,zdbfb from stock.stock_zx where dm in ("%s") and rq>="%s" and cje<>"0" limit 6 ;""" % (
            dm, final_dict[dm][1].strftime("%Y-%m-%d"))
        security_df = pd.read_sql(sqlcmd, conn)
        security_df["rq"] = pd.to_datetime(security_df['rq'], yearfirst=True)
        # result_df["rq"]=result_df["rq"].astype(np.datetime64)
        security_df[["dm", "mz"]] = security_df[["dm", "mz"]].astype(str)
        security_df.loc[:, "dqjg":"zdbfb"] = security_df.loc[:, "dqjg":"zdbfb"].fillna(0).astype("float64")
        pre_price = security_df.loc[:, "dqjg"][0]
        security_df["cum_close_rate_df"] = security_df["dqjg"].apply(lambda x: round((x / pre_price - 1) * 100, 2))
        security_df["cum_high_rate_df"] = security_df["zgj"].apply(lambda x: round((x / pre_price - 1) * 100, 2))
        cum_close_rate_df_dic = security_df[1:]["cum_close_rate_df"].to_dict()
        cum_high_rate_df_dic = security_df[1:]["cum_high_rate_df"].to_dict()
        # print(security_df)
        dic_len = len(cum_close_rate_df_dic)
        if dic_len < 5:
            for i in range(5 - dic_len):
                # print(i)
                cum_close_rate_df_dic[dic_len + i + 1] = 0
                cum_high_rate_df_dic[dic_len + i + 1] = 0
        norkey = cum_close_rate_df_dic.keys() & cum_high_rate_df_dic.keys()
        # print(norkey)
        zdlb = {}
        for key in norkey:
            zdlb["day" + str(key)] = (cum_close_rate_df_dic[key], cum_high_rate_df_dic[key])
        zdlb["corr"] = final_dict[dm]
        # dic={a:(cum_close_rate_df_dic[a],cum_high_rate_df_dic[b])for a,b in zip(cum_close_rate_df_dic,cum_high_rate_df_dic)}
        # print(dic)
        return_dic[dm] = zdlb

    # return_dic["close_rate_dic"]=return_close_rate_dic
    # return_dic["high_rate_dic"] = return_high_rate_dic
    #
    # a={a:b for a,b in zip(return_close_rate_dic,return_high_rate_dic)}
    #print(return_dic)
    #return return_dic


    return return_dic


if __name__ == '__main__':
    #dic = {'300015': (Timestamp('2022-08-22 00:00:00'), Timestamp('2022-08-10 00:00:00'), 0.9139999747276306), '603598': (Timestamp('2022-08-22 00:00:00'), Timestamp('2022-08-26 00:00:00'), 0.9139999747276306)}
    #df_syl=df_syl(dic)
    #{'002818': {'day1': (-2.75, 0.64), 'day2': (0, 0), 'day3': (0, 0), 'day4': (0, 0), 'day5': (0, 0), 'corr': (Timestamp('2022-07-15 00:00:00'), Timestamp('2022-09-01 00:00:00'), 0.8640000224113464)},
    final_dict = resemble_k(security="600603", startdate="2022-07-10", enddate="2022-08-26", days=2)
    print(final_dict)
