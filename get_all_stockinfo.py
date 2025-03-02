import tushare as ts
# 初始化pro接口
pro = ts.pro_api('7cafaabce3f2ff1d3a034677df002dc4fbd51d6ea908608edc8cf5ed')

# 拉取数据
df = pro.stock_basic(**{
    "ts_code": "",
    "name": "",
    "exchange": "szse",
    "market": "",
    "is_hs": "",
    "list_status": "",
    "limit": "",
    "offset": ""
}, fields=[
    "ts_code",
    "symbol",
    "name",
    "area",
    "industry",
    "cnspell",
    "market",
    "list_date",
    "act_name",
    "act_ent_type"
])
print(df)