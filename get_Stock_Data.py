import os
import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
# 设置tushare的token
ts.set_token('f5cdef02d8473ed826dfce5d8f57bf28f69a8d874a2771ad9ef35e17')

# 初始化pro接口
pro = ts.pro_api()

def get_stock_basic():
    # 获取股票基本信息
    basic_df = pro.stock_basic(
        exchange='',  # 交易所 SSE上交所 SZSE深交所 
        list_status='L'  # L上市 D退市 P暂停上市
    )
    return basic_df

def get_chips_data(ts_code):
    #获取1个股筹码分布数据
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')
    chips_df = pro.cyq_chips(ts_code=ts_code,start_date=start_date,end_date=end_date)
    #修改列名为中文
    chips_df.columns = ['日期', '代码', '价格', '百分比']
    return chips_df

def get_stock_min_data(ts_code):
    #获取1个股分钟行情数据
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')
    
    # 使用stk_mins替代min
    min_df = pro.stk_mins(ts_code=ts_code,
                         start_date=start_date,
                         end_date=end_date,
                         freq='1min')  # 指定获取1分钟频率的数据
                         
    #修改列名为中文
    min_df.columns = ['代码', '日期', '时间', '开盘价', '最高价', '最低价', '收盘价', '前收盘价', '涨跌额', '涨跌幅', '成交量', '成交额']
    return min_df


def get_stock_daily_data(ts_code):
    #获取180天的个股数据
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')
    daily_df = pro.daily(ts_code=ts_code,
                   start_date=start_date,
                   end_date=end_date)
    #修改列名为中文
    daily_df.columns = ['代码', '日期', '开盘价', '最高价', '最低价', '收盘价', '前收盘价', '涨跌额', '涨跌幅', '成交量', '成交额']
    return daily_df

def export_data(chips_df, daily_df, filename):
    # 获取今日日期作为文件夹名
    today = datetime.now().strftime('%Y%m%d')
    # 构建文件夹路径 
    folder_path = f'data/get_stock_data/{today}'
    # 如果文件夹不存在则创建
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # 获取股票代码作为文件名
    stock_code = daily_df['代码'].iloc[0]
    
    # 将两份数据分别写入同一个CSV文件的不同sheet
    with pd.ExcelWriter(f'{folder_path}/{stock_code}.xlsx') as writer:
        daily_df.to_excel(writer, sheet_name='日线数据', index=False)
        chips_df.to_excel(writer, sheet_name='筹码数据', index=False)

# 获取数据
#ts_code = '300059.SZ'
ts_code = '301076.SZ'
# 基本信息
basic_info = get_stock_basic()

chips_df = get_chips_data(ts_code)
#min_df = get_stock_min_data(ts_code)
daily_df = get_stock_daily_data(ts_code)
# 创建data目录(如果不存在)



# 导出数据
export_data(chips_df,daily_df, 'stock_data')