# 本Python代码主要用于策略交易
# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
from PythonApi import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib



#  在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。--(必须实现)
def init(context):
    handle_bar(context)
    

    

# before_trading此函数会在每天基准合约的策略交易开始前被调用，当天只会被调用一次。--（选择实现）
def before_trading(context):
    print("before")



# 你选择的品种的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新。--(必须实现)
def handle_bar(context):
    sh_code = get_blocks ('上海A股',0)
    sz_code = get_blocks ('深圳A股',0)
    sz_cy_code = get_blocks ('深圳创业',0)


    #代码列表
    code_list = sh_code+sz_code+sz_cy_code  

    #剔除数据量小于一个月的品种
    stock = []
    stocks = []
    for i in code_list:
        close=history_bars(i,22,'1d','CLOSE',True,False,True)
        get_fin=get_finance(i,60,1,0,0)
        if len(close)==22 and len(get_fin)>0:
            stock.append(i)

    if len(stock)>0:
        for i in stock:
            li4 = fin_profit_std(i,'NIncome',4,4,0)
            if i == len(stock)-4:
                break
            if len(li4) >= 4 and li4[0]*li4[1]*li4[2]*li4[3] > 0:
                if (li4[3] - li4[2]) / li4[2] > 0.2 and (li4[2] - li4[1]) / li4[1] > 0.2 and (li4[1] - li4[0]) / li4[0] > 0.2:
                    stocks.append(i)
        for j in stocks:
            df = history_bars(j, 100, 'self', 'close',True)
            diff, dea, macd = talib.MACD(df, fastperiod=12, slowperiod=26, signalperiod=9)
            if diff[99]>dea[99] and diff[98]<dea[98]:
                buy_open(j, "market", volume=100)
            if diff[99]<dea[99] and diff[98]>dea[98]:#最后一个元素就是现在 死叉
                portfolio = get_portfolio(j,0)
                sell_close(j,"market", volume=portfolio.buy_quantity)                

# after_trading函数会在每天交易结束后被调用，当天只会被调用一次。 --（选择实现）
def after_trading(context):
    pass


    
# exit函数会在测评结束或者停止策略运行时会被调用。---（选择实现）
def exit(context):
    pass