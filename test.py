import backtrader as bt
import pandas as pd
import tushare as ts

# 设置 Tushare Token（需先注册获取）
ts.set_token('7cafaabce3f2ff1d3a034677df002dc4fbd51d6ea908608edc8cf5ed')
pro = ts.pro_api()

# 获取股票数据（示例：贵州茅台，代码600036.SH）
df = pro.daily(ts_code='600036.SH', start_date='20190101', end_date='20231231')

# 数据预处理
df = df[['trade_date', 'open', 'high', 'low', 'close', 'vol']]
df['trade_date'] = pd.to_datetime(df['trade_date'])
df = df.rename(columns={
    'trade_date': 'date',
    'vol': 'volume'
}).set_index('date').sort_index()  # 按时间升序排列

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
        ('slow_period', 20)    # 长期均线周期
    )

    def __init__(self):
        # 计算均线
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
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annual_return')

# 运行回测
print('初始资金: %.2f' % cerebro.broker.getvalue())
results = cerebro.run()
print('最终资金: %.2f' % cerebro.broker.getvalue())

# 输出分析结果
strat = results[0]
sharpe = strat.analyzers.sharpe.get_analysis()
drawdown = strat.analyzers.drawdown.get_analysis()
annual_return = strat.analyzers.annual_return.get_analysis()

print('\n========== 回测结果 ==========')
print('夏普比率:', sharpe['sharperatio'])
print('最大回撤: %.2f%%' % drawdown['max']['drawdown'])
print('年化收益率:')
for year, ret in annual_return.items():
    print(f'  {year}: {ret:.2%}')

# 绘制图表
cerebro.plot(style='candlestick', barup='red', bardown='green')