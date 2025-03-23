import backtrader as bt
import pandas as pd
import tushare as ts
from datetime import datetime

# 设置 Tushare Token（需先注册获取）
ts.set_token('7cafaabce3f2ff1d3a034677df002dc4fbd51d6ea908608edc8cf5ed')
pro = ts.pro_api()
column_name = ['stock','启动资金','最终资金','sharp夏普','最大回测','收益率']
df_result=pd.DataFrame(columns=column_name)
def download_stock(stock_code='430090.BJ',start_date='20190101', end_date='20250303'):
    # 获取股票数据（示例：贵州茅台，代码600036.SH）
    #df = pro.daily(ts_code='430090.BJ', start_date='20190101', end_date='20250303')
    df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
    # 数据预处理
    df = df[['trade_date', 'open', 'high', 'low', 'close', 'vol']]
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df = df.rename(columns={
        'trade_date': 'date',
        'vol': 'volume'
    }).set_index('date').sort_index()  # 按时间升序排列
    #print(df.tail)
    return df

# 定义 Tushare 数据加载类
class TusharePandasData(bt.feeds.PandasData):
    params = (
        ('datetime', None),    # 使用DataFrame的索引作为时间
        ('open', 'open'),       # 列名映射
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'volume'),
        ('openinterest', None)  # Tushare无持仓量数据
    )

# 定义策略：双均线交叉
class SmaCrossStrategy(bt.Strategy):
    params = (
        ('fast_period', 5),    # 短期均线周期
        ('slow_period', 20),    # 长期均线周期
        ('slow_period1', 30)  # 长期均线周期
    )

    def __init__(self):
        # 计算均线
        print('init',self.params.fast_period,self.params.slow_period,self.params.slow_period1)
        self.fast_ma = bt.ind.SMA(period=self.params.fast_period)
        self.slow_ma = bt.ind.SMA(period=self.params.slow_period)
        # 交叉信号
        self.crossover = bt.ind.CrossOver(self.fast_ma, self.slow_ma)

    def next(self):
        if not self.position:  # 无持仓时
            if self.crossover > 0:  # 金叉：短期上穿长期
                self.buy(size=100)   # 买入100股
        elif self.crossover < 0:      # 死叉：短期下穿长期
            self.close()             # 平仓
def my_stratge(df,stockname):
    result = []
    # 初始化回测引擎
    cerebro = bt.Cerebro()

    # 加载数据
    data = TusharePandasData(dataname=df)
    cerebro.adddata(data)

    # 添加策略
    cerebro.addstrategy(SmaCrossStrategy)

    # 设置初始资金
    cerebro.broker.setcash(100000.0)

    # 设置交易费用（佣金+印花税）
    cerebro.broker.setcommission(
        commission=0.0003,   # 万3佣金
        margin=0,            # 无杠杆
        mult=1.0,            # 价格乘数（股票为1）
        #stamp_duty=0.001     # 卖出时千1印花税
    )

    # 添加分析器
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annual_return')

    # 运行回测
    #print('%s 初始资金: %.2f' % (stockname,cerebro.broker.getvalue()))
    result.append(stockname)
    result.append(cerebro.broker.getvalue())
    results = cerebro.run()
    #print('最终资金: %.2f' % cerebro.broker.getvalue())
    result.append(cerebro.broker.getvalue())

    # 输出分析结果
    strat = results[0]
    sharpe = strat.analyzers.sharpe.get_analysis()
    drawdown = strat.analyzers.drawdown.get_analysis()
    annual_return = strat.analyzers.annual_return.get_analysis()
    #print('收益率: %.2f%%' % (strat.analyzers.returns.get_analysis()['rtot'] * 100))
    result.append(sharpe['sharperatio'])
    result.append(drawdown['max']['drawdown'])
    result.append(strat.analyzers.returns.get_analysis()['rtot'] * 100)
    # print('\n========== 回测结果 ==========')
    # print('夏普比率:', sharpe['sharperatio'])
    # print('最大回撤: %.2f%%' % drawdown['max']['drawdown'])
    # print('年化收益率:')
    # for year, ret in annual_return.items():
    #     print(f'  {year}: {ret:.2%}')
    #print(result)
    df_result.loc[len(df_result)]=result
    # 绘制图表
    #cerebro.plot(style='candlestick', barup='red', bardown='green')

stocklist = pd.read_csv('全部A股.csv')
num = 0
nowTime = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
print(nowTime)
filenname='回测结果'+nowTime+ ".xlsx"
for stock in stocklist['证券代码']:
    if num > 2:
        break
    stockname = stock #'430090.BJ'#'600893.SH'
    inp_start = '20170101'
    inp_end = '20250301'
    df = download_stock(stockname,inp_start,inp_end)
    my_stratge(df,stockname)
    num +=1
    with pd.ExcelWriter(filenname) as writer:
        df_result.to_excel(writer, sheet_name='Sheet1')

nowTime1 = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
print(nowTime1)
print(len(df_result))