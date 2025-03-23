import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
import tushare as ts
import os
import tushare as ts

import datetime
today=datetime.date.today()
print(today)

# 获取当前时间
now_time = datetime.datetime.now()
print("now time: ", now_time)
now_time=datetime.date.today()
print("now time: ", now_time)
# 获取前一天时间
end_time = now_time + datetime.timedelta(days=-1)
print("end date: ", end_time)
# 前一天时间只保留 年-月-日
enddate = end_time.strftime('%Y-%m-%d')  # 格式化输出
print("end date: ", enddate)

# 获取前 15 天时间
start_time = now_time + datetime.timedelta(days=-15)

# 前 15 天时间只保留 年-月-日
startdate = start_time.strftime('%Y-%m-%d')  # 格式化输出
print("start date: ", startdate)

#ts.set_token('18427aa0a10e23a2bf2bf2de0b240aa0005db0629feea9fa2a3bd6a8')
pro = ts.pro_api()
# 拉取数据
df = pro.daily(**{
    "ts_code": "000001.SZ",
    "trade_date": "",
    "start_date": "2025-01-01",
    "end_date": "2025-03-21",
    "offset": "",
    "limit": ""
}, fields=[
    "ts_code",
    "trade_date",
    "open",
    "high",
    "low",
    "close",
    "pre_close",
    "change",
    "pct_chg",
    "vol",
    "amount"
])
print(df.head)
def downloadHistoryData(code,start,end,utype='hfq'):
    #df=pro.daily(ts_code=code,autype=utype ,start_date=start,end_date=end)
    df = pro.daily(ts_code=code, start_date=start, end_date=end)
    df.index = pd.to_datetime(df.trade_date)
    #设置把日期作为索引
    #df['ma'] = 0.0  # Backtrader需要用到
    #df['openinterest'] = 0.0  # Backtrader需要用到
    #定义两个新的列ma和openinterest
    df = df[['open', 'high', 'low', 'close', 'vol']]
    #重新设置df取值，并返回df
    return df
def acquire_code():   #只下载一只股票数据，且只用CSV保存   未来可以有自己的数据库
    code = pd.read_csv('全部A股.csv')
    num = 0
    for str in code['证券代码']:
        if num > 3:
            break
        inp_code = str #'430090.BJ'#'600893.SH'
        end_time = datetime.date.today() #'2017-01-01'
        inp_end = end_time.strftime('%Y-%m-%d')
        start_time = end_time + datetime.timedelta(days=-430) #'2025-03-01'
        inp_start = start_time.strftime('%Y-%m-%d')
        print('日期 %s %s'%(inp_start,inp_end))
        inp_start = '20250101'
        inp_end = '20250321'
        print('download:',num,inp_code,inp_start,inp_end)
        df = downloadHistoryData(inp_code,inp_start,inp_end)

        print(len(df))
        if len(df) < 10:
            print(inp_code + ' records is less 10')
        #print(df.info())
        #输出统计各列的数据量
        #print("—"*30)
        #分割线
        #print(df.describe())
        #输出常用统计参数

        #创建一个文件，把下载的数据保存起来
        path = os.path.join(os.getcwd(), inp_code + ".csv")
        #print(path)
        #os.path地址拼接，''数据地址''为文件保存路径
        # path = os.path.join(os.path.join(os.getcwd(),"数据地址"),inp_code+"_30M.csv")
        df.to_csv(path)
        #df.sort_index(inplace=True)
        df_new = df.sort_index()
        path = os.path.join(os.getcwd(), inp_code + "_sort.csv")
        df_new.to_csv(path)
        num += 1
    return df
    print('download stocks ',num)


# # 拉取数据
# df = pro.daily(**{
#     "ts_code": "430090.BJ",
#     "trade_date": "",
#     "start_date": "",
#     "end_date": "",
#     "offset": "",
#     "limit": ""
# }, fields=[
#     "ts_code",
#     "trade_date",
#     "open",
#     "high",
#     "low",
#     "close",
#     "pre_close",
#     "change",
#     "pct_chg",
#     "vol",
#     "amount"
# ])
# print(df)

acquire_code()