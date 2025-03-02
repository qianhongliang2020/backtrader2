import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
import tushare as ts
import os
import tushare as ts
ts.set_token('7cafaabce3f2ff1d3a034677df002dc4fbd51d6ea908608edc8cf5ed')
pro = ts.pro_api()
def get_data(code,start,end):
    df=pro.daily(ts_code=code,autype='qfq',start_date=start,end_date=end)
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
        if num > 2:
            break
        inp_code = str #'430090.BJ'#'600893.SH'
        inp_start = '2017-01-01'
        inp_end = '2025-03-01'
        df = get_data(inp_code,inp_start,inp_end)

        print(len(df))
        if len(df) < 10:
            print(inp_code + ' records is less 10')
        #print(df.info())
        #输出统计各列的数据量
        #print("—"*30)
        #分割线
        #print(df.describe())
        #输出常用统计参数
        df.sort_index(inplace=True)
        #把股票数据按照时间正序排列
        path = os.path.join(os.path.join(os.getcwd(),
            "./stock"), inp_code + ".csv")
        #print(path)
        #os.path地址拼接，''数据地址''为文件保存路径
        # path = os.path.join(os.path.join(os.getcwd(),"数据地址"),inp_code+"_30M.csv")
        df.to_csv(path)
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