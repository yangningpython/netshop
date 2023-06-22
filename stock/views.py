from datetime import *
#import time

from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from stock.resemble_k_line import *

class stock_play(View):
    def get(self, request):
        # 获取请求参数

        zdsx = int(request.GET.get('zdsx', 1))
        ts = int(request.GET.get('ts', 10))
        cursor = connection.cursor()
        cursor.execute("call ljfx38(%d,%d) ;" % (zdsx, ts))
        result1 = cursor.fetchall()

        # cursor.execute("call ljfx39(%d,%d) ;" % (zdsx, ts))
        cursor.execute("call ljfx46(%d,%d) ;" % (zdsx, ts))
        result2 = cursor.fetchall()

        cursor.execute("call ljfx40(%d,%d) ;" % (zdsx, ts))
        result3 = cursor.fetchall()
        print("ceshi-----1", result1)
        print("ceshi-----2", result2)
        print("ceshi-----3", result3)
        # print(zdsx,ts)
        stock_dm_set = set()
        for stock in result1:
            stock_dm_set.add((stock[1], stock[2]))
        # stock2_dm = []
        for stock in result2:
            stock_dm_set.add((stock[1], stock[2]))
        for stock in result3:
            stock_dm_set.add((stock[1], stock[2]))

        # connection.commit()
        stock_dm = list(stock_dm_set)
        startdate = (datetime.now() + timedelta(days=-130)).strftime("%Y-%m-%d")
        enddate = datetime.now().strftime('%Y-%m-%d')
        stock_all_info = []
        # print(startdate,enddate,stock_dm)
        for stock in stock_dm:
            stock_info = {}
            stock_info["dm"] = stock[0]
            stock_info["mz"] = stock[1]

            cursor.execute("select jtkp,dqjg,\
                    zdj,zgj,cjl,\
                    rq from stock.stock_zx where dm='%s' and rq>='%s' and rq<='%s' and jtkp<>'0.00' order by rq;" % (
            stock[0], startdate, enddate))
            # print("select jtkp,dqjg,zdj,zgj,cjl,rq from stock.stock_zx where dm='%s' and rq>='%s' and rq<='%s' order by rq;" % (
            # stock[0], startdate, enddate))
            # cast(jtkp as DECIMAL(10,2)) as jtkp,cast(dqjg as DECIMAL(10,2)) as dqjg,\
            # cast(zdj as DECIMAL(10,2)) as zdj,cast(zgj as DECIMAL(10,2)) as zgj,cast(cjl as DECIMAL(10,2)) as cjl,\
            stock_detail = cursor.fetchall()
            stock_data = []
            stock_volumes = []
            stock_date = set()
            # print(stock_detail)
            for data in stock_detail:
                stock_data.append([data[0], data[1], data[2], data[3], data[4]])
                stock_date.add(data[5])
                stock_volumes.append(data[4])
            datelist = list(stock_date)
            datelist.sort()
            stock_info["date"] = datelist
            stock_info["data"] = stock_data
            stock_info["volumes"] = stock_volumes
            stock_all_info.append(stock_info)
        # stock_all_info1=[]
        stock_all_info.sort(key=lambda s: int(s["dm"]))

        # stock_all_info1.append(stock_all_info[0])
        # print(stock_all_info)

        # 判断用户是否登录
        # return HttpResponse("股票成功")
        return render(request, 'stock_display.html',
                      {'result1': result1, "result2": result2,"result3": result3, "stock_all_info": stock_all_info})

    def post(self, request):
        zdsx = int(float(request.POST.get('zdsx', "1")))
        ts = int(float(request.POST.get('ts', "10")))
        # print("post",zdsx,ts)
        cursor = connection.cursor()
        cursor.execute("call ljfx38(%d,%d) ;" % (zdsx, ts))
        result1 = cursor.fetchall()
        #cursor.execute("call ljfx39(%d,%d) ;" % (zdsx, ts))
        cursor.execute("call ljfx46(%d,%d) ;" % (zdsx, ts))
        result2 = cursor.fetchall()
        cursor.execute("call ljfx40(%d,%d) ;" % (zdsx, ts))
        result3 = cursor.fetchall()
        # print("ceshi-----1", result1)
        # print("ceshi-----2", result2)
        # print("ceshi-----3", result3)
        stock_dm_set = set()
        for stock in result1:
            stock_dm_set.add((stock[1], stock[2]))
        # stock2_dm = []
        for stock in result2:
            stock_dm_set.add((stock[1], stock[2]))
        for stock in result3:
            stock_dm_set.add((stock[1], stock[2]))
        # connection.commit()
        stock_dm = list(stock_dm_set)
        startdate = (datetime.now() + timedelta(days=-130)).strftime("%Y-%m-%d")
        enddate = datetime.now().strftime('%Y-%m-%d')
        stock_all_info = []
        # print(startdate,enddate,stock_dm)
        for stock in stock_dm:
            stock_info = {}
            stock_info["dm"] = stock[0]
            stock_info["mz"] = stock[1]

            cursor.execute("select jtkp,dqjg,\
                    zdj,zgj,cjl,\
                    rq from stock.stock_zx where dm='%s' and rq>='%s' and rq<='%s' and jtkp<>'0.00' order by rq;" % (
            stock[0], startdate, enddate))
            # print("select jtkp,dqjg,zdj,zgj,cjl,rq from stock.stock_zx where dm='%s' and rq>='%s' and rq<='%s' order by rq;" % (
            # stock[0], startdate, enddate))
            # cast(jtkp as DECIMAL(10,2)) as jtkp,cast(dqjg as DECIMAL(10,2)) as dqjg,\
            # cast(zdj as DECIMAL(10,2)) as zdj,cast(zgj as DECIMAL(10,2)) as zgj,cast(cjl as DECIMAL(10,2)) as cjl,\
            stock_detail = cursor.fetchall()
            stock_data = []
            stock_volumes = []
            stock_date = set()
            # print(stock_detail)
            for data in stock_detail:
                stock_data.append([data[0], data[1], data[2], data[3], data[4]])
                stock_date.add(data[5])
                stock_volumes.append(data[4])
            datelist = list(stock_date)
            datelist.sort()
            stock_info["date"] = datelist
            stock_info["data"] = stock_data
            stock_info["volumes"] = stock_volumes
            stock_all_info.append(stock_info)
        # stock_all_info1=[]
        stock_all_info.sort(key=lambda s: int(s["dm"]))

        # stock_all_info1.append(stock_all_info[0])
        # print(stock_all_info)

        # 判断用户是否登录
        # return HttpResponse("股票成功")
        #return JsonResponse( {'result1': result1, "result2": result2, "stock_all_info": stock_all_info})

        return render(request, 'stock_display.html',\
                      {'result1': result1, "result2": result2,"result3": result3, "stock_all_info": stock_all_info})
class k_line_similitude(View):
    def get(self, request):
        # get请求默认参数修改
        # 获取session
        sessionstartdate = request.session.get('startdate', None)

        default_startdate=gettradedays(5)
        default_enddate =gettradedays(1)
        default_reference_security="000001"
        default_back_days="1"
        default_pamart=[default_startdate,default_enddate,default_reference_security,default_back_days]
        # 获取请求参数
        startdate = request.GET.get('startdate', default_startdate)
        #print(startdate)
        startdate_diff=(datetime.strptime(startdate,"%Y-%m-%d")+timedelta(days=-20)).strftime("%Y-%m-%d")
        enddate = request.GET.get('enddate', default_enddate)
        reference_security=request.GET.get('reference_security', default_reference_security)
        back_days=int(request.GET.get('back_days', default_back_days))

        request.session['startdate'] = startdate
        request.session['enddate'] = enddate
        request.session['reference_security'] = reference_security
        request.session['back_days'] = back_days
        #{'002818': {'day1': (-2.75, 0.64), 'day2': (0, 0), 'day3': (0, 0), 'day4': (0, 0), 'day5': (0, 0),
        #            'corr': (Timestamp('2022-07-15 00:00:00'), Timestamp('2022-09-01 00:00:00'), 0.8640000224113464)},
        conn=connection
        cursor = conn.cursor()
        cursor.execute("select rq,dm,mz,wp,\
                            np,hsl,dqjg,zdbfb,round(wp/nullif(np,0),2) as wnb,ltsz,cje,jtkp,\
                    zdj,zgj,cjl from stock.stock_zx where dm='%s' and rq>='%s' and rq<='%s' and jtkp<>'0.00' order by rq;" % (
            reference_security, startdate_diff,enddate))
        fh = cursor.fetchall()
        print(reference_security, startdate_diff,enddate)

        result1=(fh[-1],)
        #print(result1)
        stock_basic_data = []
        stock_volumes = []
        stock_date = set()
        stock_all_info = []

        # print(stock_detail)
        for data in fh:
            # 开盘，收盘，最低，最高，成交量
            stock_basic_data.append([data[11], data[6], data[12], data[13], data[14]])
            # 日期
            stock_date.add(data[0])
            # 成交量
            stock_volumes.append(data[14])
        datelist = list(stock_date)
        datelist.sort()
        enddate_index = datelist.index(enddate)
        k_end_position = round(enddate_index / (len(datelist) - 1), 2) * 100
        stock_info={}
        stock_info["dm"] = fh[0][1]
        stock_info["mz"] = fh[0][2]
        stock_info["date"] = datelist
        stock_info["k_end_position"] = k_end_position
        stock_info["data"] = stock_basic_data
        stock_info["volumes"] = stock_volumes
        stock_all_info.append(stock_info)
        #print(result1)
        # k线数据
        print("超时系列0。。。。。。。。。。。。")
        corr_dic=resemble_k(reference_security,startdate,enddate,back_days,conn)
        dm_list=list(corr_dic.keys())

        data_basic_info=[]
        print("超时系列1。。。。。。。。。。。。")

        for stock in dm_list:
            stock_info = {}


        #+timedelta(days=-days+1)
            cursor.execute("select dm,mz,jtkp,dqjg,\
                    zdj,zgj,cjl,\
                    rq,hsl,zdbfb,round(wp/nullif(np,0),2) as wnb,ltsz,cje from stock.stock_zx where dm='%s' and rq>='%s' and rq<='%s' and jtkp<>'0.00' order by rq;" % (
            stock, (corr_dic[stock]["corr"][0]+timedelta(days=-20)).strftime("%Y-%m-%d"), (corr_dic[stock]["corr"][1]+timedelta(days=10)).strftime("%Y-%m-%d")))
            stock_detail = cursor.fetchall()
            k_endtime=corr_dic[stock]["corr"][1].strftime("%Y-%m-%d")
            end_stock=list(filter(lambda x:x[7]==k_endtime,stock_detail))
            data_basic_info.append(end_stock[0])
            #print(end_stock)
            stock_info["dm"] = stock
            stock_info["mz"] = stock_detail[1][1]

            stock_basic_data = []
            stock_volumes = []
            stock_date = set()
            # print(stock_detail)
            for data in stock_detail:
                # 开盘，收盘，最低，最高，成交量
                stock_basic_data.append([data[2], data[3], data[4], data[5], data[6]])
                # 日期
                stock_date.add(data[7])
                # 成交量
                stock_volumes.append(data[6])
            datelist = list(stock_date)
            datelist.sort()
            enddate_index=datelist.index(k_endtime)
            k_end_position=round(enddate_index/(len(datelist)-1),2)*100
            stock_info["date"] = datelist
            stock_info["k_end_position"] = k_end_position

            stock_info["data"] = stock_basic_data
            stock_info["volumes"] = stock_volumes
            stock_info["corr"] = corr_dic[stock]["corr"]
            stock_all_info.append(stock_info)
            # stock_all_info1=[]

        #a=stock_all_info.sort(key=lambda s: s["corr"][2],reverse=True)
        #rq,dm, mz, hsl, dqjg,zdbfb,wnb,ltsz,cjl,cje
        #dm, mz, jtkp, dqjg,zdj, zgj, cjl, rq, hsl, zdbfb,wnb, ltsz, cje
        result2=[]

        for data in data_basic_info:
            pxdata=(data[7],data[0],data[1],data[8],data[3],data[9],data[10],data[11],data[12],corr_dic[data[0]])
            #corr_dic[data[1]]
            result2.append(pxdata)

        #print(result2)
        # 获取数据库数据
        #result1 = cursor.fetchall()
        print("超时系列2。。。。。。。。。。。。")
        print(request.GET)

        return render(request, 'k_line_similitude.html',{"default_pamart":default_pamart,"result1":result1,"result2": result2,"stock_all_info": stock_all_info})
        #return render(request, 'k_line_similitude.html')


