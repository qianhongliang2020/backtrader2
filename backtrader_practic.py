import datetime  #
import os.path  # 路径管理
import sys  # 获取当前运行脚本的路径 (in argv[0])
# 导入backtrader框架
import backtrader as bt
import data_if_backtrade

# 创建策略继承bt.Strategy
# 创建策略继承bt.Strategy
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        # 记录策略的执行日志
        dt = self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 保存收盘价的引用
        self.dataclose = self.datas[0].close
        # 跟踪挂单
        self.order = None
        # 买入价格和手续费
        self.buyprice = None
        self.buycomm = None
        self.profit = 0
        # 订单状态通知，买入卖出都是下单

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # broker 提交/接受了，买/卖订单则什么都不做
            return
        # 检查一个订单是否完成
        # 注意: 当资金不足时，broker会拒绝订单
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '已买入, 价格: %.2f, 费用: %.2f, 佣金 %.2f, vol: %.2f' %
                    (order.executed.price,
                    order.executed.value,
                    order.executed.comm,self.position.size))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('已卖出, 价格: %.2f, 费用: %.2f, 佣金 %.2f, vol: %.2f' %
                    (order.executed.price,
                    order.executed.value,
                    order.executed.comm,self.position.size))
            # 记录当前交易数量
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/拒绝')

        # 其他状态记录为：无挂起订单
        self.order = None


    # 交易状态通知，一买一卖算交易
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.profit += trade.pnlcomm
        self.log('交易利润, 毛利润 %.2f, 净利润 %.2f, 总净利润 %.2f' %
            (trade.pnl, trade.pnlcomm,self.profit))

    def next(self):
        # 记录收盘价
        #self.log('Close, %.2f' % self.dataclose[0])
        # 如果有订单正在挂起，不操作
        if self.order:
            return
    # 如果没有持仓则买入
        if not self.position:
            # 今天的收盘价 < 昨天收盘价
            if self.dataclose[0] < self.dataclose[-1]:
                # 昨天收盘价 < 前天的收盘价
                if self.dataclose[-1] < self.dataclose[-2]:
                    # 买入
                    self.log('买入单, %.2f' % self.dataclose[0])
                    # 跟踪订单避免重复
                    self.order = self.buy(size=1000)
        else:
            #self.log('卖出单1, %.2f %.2f %.2f' % ((self.dataclose[0]), len(self), (self.bar_executed + 5)))
            # 如果已经持仓，且当前交易数据量在买入后5个单位后
            #if len(self) >= (self.bar_executed + 5):
            if (self.dataclose[0] > self.dataclose[-1]) | len(self) >= (self.bar_executed + 5):
                # 全部卖出
                self.log('卖出单, %.2f %.2f %.2f' % ((self.dataclose[0]),len(self),(self.bar_executed + 5)))
                # 跟踪订单避免重复
                self.order = self.sell(size=1000)
cerebro = bt.Cerebro()
# Cerebro引擎在后台创建broker(经纪人)，系统默认资金量为10000
# 为Cerebro引擎添加策略
cerebro.addstrategy(TestStrategy)
# 加载交易数据,把dataframe的数据转换成backtrader需要的格式
df = data_if_backtrade.download_stock()
data = data_if_backtrade.TusharePandasData(dataname=df)

cerebro.adddata(data)

# 设置投资金额100000.0
cerebro.broker.setcash(100000.0)
#设置佣金为0.001,除以100去掉%号
cerebro.broker.setcommission(commission=0.0002)

#print("\n\t#2-5,设置每手交易数目为：10，不再使用默认值：1手")
#cerebro.addsizer(bt.sizers.FixedSize, stake=1)

# 引擎运行前打印期出资金
print('组合期初资金: %.2f' % cerebro.broker.getvalue())
cerebro.run()
#cerebro.plot(style='candlestick', barup='red', bardown='green')
# 引擎运行后打期末资金
print('组合期末资金0: %.2f' % cerebro.broker.getvalue())
print('组合期末资金1: %.2f' % cerebro.broker.getvalue())
print('组合期末资金2: %.2f' % cerebro.broker.getvalue())