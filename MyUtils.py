"""some tools"""

import pandas as pd

def get_realtime_quotes(stock_code):
    """
    获取股票实时分时数据
    :param stock_code: 股票代码（例如：'000001.SZ'）
    :return: DataFrame 包含分时数据
    """
    try:
        # 获取实时行情数据
        df = ts.pro_bar(ts_code=stock_code,
                        freq='min',
                        asset='E',
                        adj='qfq',
                        start_date=pd.Timestamp.now().strftime('%Y%m%d'),
                        end_date=pd.Timestamp.now().strftime('%Y%m%d'))

        # 按时间排序
        df = df.sort_values('trade_time')

        return df
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None


def get_intraday_minute_data(stock_code, pro, interval=5):
    """
    获取当日分钟级K线数据
    :param stock_code: 股票代码（例如：'000001.SZ'）
    :param interval: K线周期（1, 5, 15, 30, 60分钟）
    :return: DataFrame 包含分钟级数据
    """
    try:
        # 获取当日分钟级数据
        df = pro.query('min_daily',
                       ts_code=stock_code,
                       freq=f'{interval}min',
                       trade_date=pd.Timestamp.now().strftime('%Y%m%d'))

        # 按时间排序
        df = df.sort_values('trade_time')

        return df
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None


def calculate_kdj(df: pd.DataFrame, N=9, M1=3, M2=3):
    '''
    计算 KDJ 技术指标。
    参数:
    df (pd.DataFrame): 包含至少 'high', 'low', 'close' 列的 DataFrame，
                       分别代表每日最高价、最低价和收盘价。
    N (int): 用于计算 RSV 的时间窗口大小，默认为9。
    M1 (int): 用于计算 K 值的指数加权移动平均 (EWMA) 的平滑因子，默认为3。
    M2 (int): 用于计算 D 值的指数加权移动平均 (EWMA) 的平滑因子，默认为3。
    返回:
    pd.DataFrame: 包含 K, D, 和 J 值的 DataFrame。
    '''

    # 创建一个df的副本以避免修改原始数据
    data = df.copy()

    # 计算 N 周期内的最低价 LLV 和最高价 HHV
    ln = data['low'].rolling(N, min_periods=1).min()
    hn = data['high'].rolling(N, min_periods=1).max()

    # 计算 RSV (Relative Strength Value)
    rsv = (data['close'] - ln) / (hn - ln) * 100

    # 计算 K 值，使用指数加权移动平均 (EWMA)
    k = rsv.ewm(alpha=1 / M1, adjust=False).mean()

    # 计算 D 值，同样使用指数加权移动平均 (EWMA)
    d = k.ewm(alpha=1 / M2, adjust=False).mean()

    # 计算 J 值
    j = 3 * k - 2 * d

    # 将计算出的 K, D, 和 J 值添加到 DataFrame
    data['k'] = k
    data['d'] = d
    data['j'] = j

    # 返回包含所有计算出指标的 DataFrame
    return data


# 使用示例
if __name__ == "__main__":
    # 设置股票代码（平安银行）
    stock_code = '000001.SZ'

    # 获取实时分时数据
    realtime_data = get_realtime_quotes(stock_code)
    if realtime_data is not None:
        print("实时分时数据:")
        print(realtime_data[['trade_time', 'open', 'high', 'low', 'close', 'vol']].head())

    # 获取5分钟K线数据
    minute_data = get_intraday_minute_data(stock_code, interval=5)
    if minute_data is not None:
        print("\n5分钟K线数据:")
        print(minute_data[['trade_time', 'open', 'high', 'low', 'close', 'vol']].head())