
import math
from position import Position

class Butler():
    #アルゴリズム
    '''
    # 超短期ボリンジャーバンド
     1. 2から8日から期間を選択
     2. 単純移動平均と標準偏差を求める
     3. 転換価格をσの何倍にするか決める
     4. 翌日場が開く前にその転換価格±１ティックの価格(買いは上、売りは下)で逆指値注文を入れる
    '''
    def __init__(self, bollinger_duration, diff_price):
        self.duration = bollinger_duration
        self.diff_price = diff_price 

    def check_open_long(self, q, idx):
        #当日高値がevσ以上かつ出来高がevσ以上
        if (q.quotes['high'][idx] is None 
                or q.upper_ev_sigma[idx] is None 
                or q.quotes['low'][idx] is None 
                or q.lower_ev_sigma[idx] is None
                or q.vol_ma[idx] is None):
            return False
        long_flg = q.quotes['high'][idx] >= q.upper_ev_sigma[idx]
        short_flg = q.quotes['low'][idx] <= q.lower_ev_sigma[idx]
        volume_flg = int(q.quotes['volume'][idx]) >= q.vol_ma[idx]
        if long_flg == True and short_flg == False and volume_flg == True:
            return True
        else:
            return False

    def check_open_short(self, q, idx):
        #当日安値がevσ以下かつ出来高がevσ以上
        if (q.quotes['high'][idx] is None 
                or q.upper_ev_sigma[idx] is None 
                or q.quotes['low'][idx] is None 
                or q.lower_ev_sigma[idx] is None
                or q.vol_ma[idx] is None):
            return False
        long_flg = q.quotes['high'][idx] >= q.upper_ev_sigma[idx]
        short_flg = q.quotes['low'][idx] <= q.lower_ev_sigma[idx]
        volume_flg = int(q.quotes['volume'][idx]) <= q.vol_ma[idx]
        if long_flg == False and short_flg == True and volume_flg == True:
            return True
        else:
            return False

    def check_close_long(self, pos_price, q, idx):
        if q.quotes['close'][idx] is None:
            return False
        if abs(pos_price - q.quotes['close'][idx]) > self.diff_price:
            return True
        else:
            return False

    def check_close_short(self, pos_price, q, idx):
        if q.quotes['close'][idx] is None:
            return False
        if abs(pos_price - q.quotes['close'][idx]) > self.diff_price:
            return True
        else:
            return False

    def create_order_stop_market_long_for_all_cash(self, cash, price, tick):
        if cash == 0 or price == 0:
            return (-1, -1)
        price = price + tick
        vol = math.floor(cash / price)
        return (price, vol)

    def create_order_stop_market_short_for_all_cash(self, cash, price, tick):
        if cash == 0 or price == 0:
            return (-1, -1)
        price = price - tick
        vol = math.floor((cash / price) * -1)
        return (price, vol)

    def create_order_stop_market_close_long(self, q, idx, tick):
        if q.quotes['low'][idx] is None:
            return 0.00
        price = q.quotes['low'][idx]
        return price-tick

    def create_order_stop_market_close_short(self, q, idx, tick):
        if q.quotes['high'][idx] is None:
            return 0.00
        price = q.quotes['high'][idx]
        return price+tick

