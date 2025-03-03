# backtrader2
#20250302：
本次第一步先通过tushare下载股票数据
第二步：通过backtrader选择策略，进行股票回测。

0、主观交易
1、规则类策略交易，买入规则，卖出规则
3、截面分析交易，线性规律
4、机器学习，非线性规律

#20250303
今天通过deepseek完成backtrader的PandasData的使用。通过该函数，tushare下载的数据不需要先保存到硬盘再送给backtrader。从tushare下载完之后，保存在内存的dataframe里面，再送给给backtrader
