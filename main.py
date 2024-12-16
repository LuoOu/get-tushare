import tushare as ts
from datetime import datetime, timedelta
# 设置tushare的token
ts.set_token('f5cdef02d8473ed826dfce5d8f57bf28f69a8d874a2771ad9ef35e17')

# 初始化pro接口
pro = ts.pro_api()

ts_code='000001.SZ'

def get_data():

# 计算60天前的日期
end_date = datetime.now().strftime('%Y%m%d')
start_date = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')

df = pro.daily(ts_code='000001.SZ',
               start_date=start_date,
               end_date=end_date)

# 打印数据
print(df)

