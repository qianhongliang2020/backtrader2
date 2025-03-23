import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
import tushare as ts
import os
import tushare as ts
import datetime

ts.set_token('7cafaabce3f2ff1d3a034677df002dc4fbd51d6ea908608edc8cf5ed')
pro = ts.pro_api()

def getStartEndtime(period):
    period *= (-1);
    # 获取当前时间
    now_time = datetime.datetime.now()
    print("now time: ", now_time)
    # 获取前一天时间
    startTime = now_time + datetime.timedelta(days=period)
    print("end date: ", startTime)
    # 前一天时间只保留 年-月-日
    endDate = now_time.strftime('%Y%m%d')  # 格式化输出
    startDate = startTime.strftime('%Y%m%d')  # 格式化输出
    print("end date: ", startDate,endDate)
    return startDate,endDate

def downloadHistoryData(code,start,end):
    # download data
    df=pro.daily(ts_code=code,autype='qfq',start_date=start,end_date=end)

    # 设置把日期作为索引
    df.index = pd.to_datetime(df.trade_date)

    # 定义两个新的列ma和openinterest
    #df['ma'] = 0.0  # Backtrader需要用到
    #df['openinterest'] = 0.0  # Backtrader需要用到

    # 选取列数据
    df = df[['open', 'high', 'low', 'close', 'vol']]
    #重新设置df取值，并返回df
    return df

#只下载一只股票数据，且只用CSV保存   未来可以有自己的数据库
def acquire_code():
    code = pd.read_csv('全部A股.csv')
    num = 0
    for str in code['证券代码']:
        if num > 2:
            break
        inp_code = str #'430090.BJ'#'600893.SH'
        date = getStartEndtime(360)
        inp_start = date[0]#'20170101'
        inp_end = date[1]#'20250301'
        df = downloadHistoryData(inp_code,inp_start,inp_end)

        print(len(df))
        if len(df) < 10:
            print(inp_code + ' records is less 10')

        #输出统计各列的数据量
        #print(df.info())

        # 分割线
        #print("—"*30)

        # 输出常用统计参数
        #print(df.describe())

        # 把股票数据按照时间正序排列
        df.sort_index(inplace=True)

        # os.path地址拼接，''数据地址''为文件保存路径
        path = os.path.join(os.path.join(os.getcwd(),"./stock"), inp_code + ".csv")

        df.to_csv(path)
        num += 1
        print('download stocks ', num)



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

#acquire_code()