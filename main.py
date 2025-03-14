import backtrader as bt
import backtrader.analyzers as btanalyzers
import os
import pandas as pd
import getdata

class DualMovingAverageStrategy(bt.Strategy):
    params = (
        ('short_period', 5),  # 短期均线周期
        ('long_period', 20),  # 长期均线周期
    )

    def __init__(self):
        # 计算指标
        self.short_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.short_period)
        self.long_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.long_period)
        self.crossover = bt.indicators.CrossOver(self.short_ma, self.long_ma)

    def next(self):
        if not self.position:  # 没有持仓
            if self.crossover > 0:  # 短期均线上穿长期均线
                self.order = self.buy()  # 买入
        elif self.crossover < 0:  # 短期均线下穿长期均线
            self.order = self.sell()  # 卖出

def test(code):
    cerebro = bt.Cerebro()
    # 加载数据（需要替换为实际数据路径）
    data = bt.feeds.GenericCSVData(
        dataname=code ,
        dtformat=('%Y-%m-%d'),
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1
    )

    #data=bt.feeds.PandasData(dataname=code,fromdate='2017-01-01',todate='2025-03-01')
    cerebro.adddata(data)
    cerebro.addstrategy(DualMovingAverageStrategy)
    cerebro.broker.setcash(100000.0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=90)  # 90%仓位

    # 添加分析指标
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')

    # 运行回测
    results = cerebro.run()

    # 输出结果
    strat = results[0]
    print('最终资金: %.2f' % cerebro.broker.getvalue())
    print('收益率: %.2f%%' % (strat.analyzers.returns.get_analysis()['rtot'] * 100))
    print('夏普比率:', strat.analyzers.sharpe.get_analysis()['sharperatio'])
    print('最大回撤: %.2f%%\r\n' % strat.analyzers.drawdown.get_analysis()['max']['drawdown'])

    # 可视化（需要安装matplotlib）
    #cerebro.plot(style='candlestick')

def pasrse_files(filepath):
    for filepath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            df = getdata.acquire_code()
            filePath = os.path.join(filepath, filename)
            print(filePath)
            test(filePath)


if __name__ == '__main__':
    pasrse_files(r'./stock')
    # inp_code =  '430090.BJ'#'600893.SH'
    # inp_start = '2017-01-01'
    # inp_end = '2025-03-01'
    # df = getdata.get_data(inp_code,inp_start,inp_end)
    # print(df.head)
    # #test('600893.SH.csv')
    # test(df)
    # cerebro = bt.Cerebro()
    #
    # # 加载数据（需要替换为实际数据路径）
    # data = bt.feeds.GenericCSVData(
    #     dataname='./600893.SH.csv',
    #     dtformat=('%Y-%m-%d'),
    #     datetime=0,
    #     open=1,
    #     high=2,
    #     low=3,
    #     close=4,
    #     volume=5,
    #     openinterest=-1
    # )
    #
    # cerebro.adddata(data)
    # cerebro.addstrategy(DualMovingAverageStrategy)
    # cerebro.broker.setcash(100000.0)
    # cerebro.addsizer(bt.sizers.PercentSizer, percents=90)  # 90%仓位
    #
    # # 添加分析指标
    # cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
    # cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe')
    # cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')
    #
    # # 运行回测
    # results = cerebro.run()
    #
    # # 输出结果
    # strat = results[0]
    # print('最终资金: %.2f' % cerebro.broker.getvalue())
    # print('收益率: %.2f%%' % (strat.analyzers.returns.get_analysis()['rtot'] * 100))
    # print('夏普比率:', strat.analyzers.sharpe.get_analysis()['sharperatio'])
    # print('最大回撤: %.2f%%' % strat.analyzers.drawdown.get_analysis()['max']['drawdown'])
    #
    # # 可视化（需要安装matplotlib）
    # cerebro.plot(style='candlestick')