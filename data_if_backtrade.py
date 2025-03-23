import pandas as pd
import tushare as ts
import backtrader as bt
#from datetime import datetime

ts.set_token('7cafaabce3f2ff1d3a034677df002dc4fbd51d6ea908608edc8cf5ed')
pro = ts.pro_api()

def download_stock(stock_code='430090.BJ',start_date='20190101', end_date='20250303'):
    # 获取股票数据（示例：贵州茅台，代码600036.SH）
    #df = pro.daily(ts_code='430090.BJ', start_date='20190101', end_date='20250303')
    df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
    df['openinterest']=0
    df.to_csv(stock_code+'csv')
    # 数据预处理
    df = df[['trade_date', 'open', 'high', 'low', 'close', 'vol','amount','openinterest']]
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df = df.rename(columns={
        'trade_date': 'date',
        'close': 'close1',
        'vol': 'volume'
    }).set_index('date').sort_index()  # 按时间升序排列
    df.to_csv(stock_code + 'new' + '.csv')
    print(df['open'].max(),df['open'].min(),df['open'][-1])
    return df
# 定义 Tushare 数据加载类
class TusharePandasData(bt.feeds.PandasData):
    params = (
        ('datetime', None),    # 使用DataFrame的索引作为时间
        ('open', 'open'),       # 列名映射
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close1'),
        ('volume', 'volume'),
        ('amount', 'amount'),
        ('openinterest', 'openinterest')  # Tushare无持仓量数据
    )