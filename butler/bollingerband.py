
import math
import numpy
from position import Position
from ordertype import OrderType

class Butler():
    #アルゴリズム
    '''
    # 超短期ボリンジャーバンド
     1. 2から8日から期間を選択
     2. 単純移動平均と標準偏差を求める
     3. 転換価格をσの何倍にするか決める
     4. 翌日場が開く前にその転換価格±１ティックの価格(買いは上、売りは下)で逆指値注文を入れる
    '''
    def __init__(self, tick, bollinger_duration):
        self.duration = bollinger_duration
        self.diff_price = 0.0
        self.tick = tick
    
    def _check_quotes(self, q, idx):
        if (
            q.quotes['open'][idx] is None 
                or q.quotes['high'][idx] is None 
                or q.quotes['low'][idx] is None 
                or q.quotes['close'][idx] is None 
                or q.upper_ev_sigma[idx] is None 
                or q.lower_ev_sigma[idx] is None
                or q.upper_ev2_sigma[idx] is None 
                or q.lower_ev2_sigma[idx] is None
                or numpy.isnan(q.quotes['open'][idx])
                or numpy.isnan(q.quotes['high'][idx])
                or numpy.isnan(q.quotes['low'][idx])
                or numpy.isnan(q.quotes['close'][idx])
                or numpy.isnan(q.upper_ev_sigma[idx])
                or numpy.isnan(q.lower_ev_sigma[idx])
                or numpy.isnan(q.upper_ev2_sigma[idx])
                or numpy.isnan(q.lower_ev2_sigma[idx])
                or q.quotes['open'][idx] == 0
                or q.quotes['high'][idx] == 0
                or q.quotes['low'][idx] == 0
                or q.quotes['close'][idx] == 0
                ):
            return False
        else:
            return True

    def check_open_long(self, q, idx):
        #当日高値がevσ以上
        if not self._check_quotes(q, idx):
            return OrderType.NONE_ORDER
        long_flg = q.quotes['high'][idx] >= q.upper_ev_sigma[idx]
        short_flg = q.quotes['low'][idx] <= q.lower_ev_sigma[idx]
        if long_flg == True and short_flg == False:
            return OrderType.STOP_MARKET_LONG
        #elif long_flg == True and short_flg == True:
        #    long_diff = q.quotes['high'][idx] - q.upper_ev_sigma[idx]
        #    short_diff = q.quotes['low'][idx] - q.lower_ev_sigma[idx]
        #    if abs(long_diff) > abs(short_diff):
        #        return OrderType.STOP_MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_open_short(self, q, idx):
        #当日安値がevσ以下
        if not self._check_quotes(q, idx):
            return OrderType.NONE_ORDER
        long_flg = q.quotes['high'][idx] >= q.upper_ev_sigma[idx]
        short_flg = q.quotes['low'][idx] <= q.lower_ev_sigma[idx]
        if long_flg == False and short_flg == True:
            return OrderType.STOP_MARKET_SHORT
        #elif long_flg == True and short_flg == True:
        #    long_diff = q.quotes['high'][idx] - q.upper_ev_sigma[idx]
        #    short_diff = q.quotes['low'][idx] - q.lower_ev_sigma[idx]
        #    if abs(short_diff) > abs(long_diff):
        #        return OrderType.STOP_MARKET_SHORT
        else:
            return OrderType.NONE_ORDER

    def check_close_long(self, pos_price, q, idx):
        if not self._check_quotes(q, idx):
            return OrderType.NONE_ORDER
        return OrderType.CLOSE_STOP_MARKET_LONG

    def check_close_short(self, pos_price, q, idx):
        if not self._check_quotes(q, idx):
            return OrderType.NONE_ORDER
        return OrderType.CLOSE_STOP_MARKET_SHORT

    def create_order_stop_market_long_for_all_cash(self, cash, q, idx):
        if not self._check_quotes(q, idx) or cash <= 0:
            return (-1, -1)
        price = self.create_order_stop_market_long(q, idx)
        vol = math.floor(cash / price)
        return (price, vol)

    def create_order_stop_market_short_for_all_cash(self, cash, q, idx):
        if not self._check_quotes(q, idx) or cash <= 0:
            return (-1, -1)
        price = self.create_order_stop_market_short(q, idx)
        vol = math.floor((cash / price) * -1)
        return (price, vol)

    def create_order_stop_market_long(self, q, idx):
        if not self._check_quotes(q, idx):
            return -1
        price = q.quotes['high'][idx] + self.tick
        #price = q.upper_ev2_sigma[idx]
        return price

    def create_order_stop_market_short(self, q, idx):
        if not self._check_quotes(q, idx):
            return -1
        price = q.quotes['low'][idx] - self.tick
        #price = q.lower_ev2_sigma[idx]
        return price

    def create_order_close_stop_market_long(self, q, idx):
        if not self._check_quotes(q, idx):
            return 0.00
        price = q.quotes['low'][idx] - self.tick
        #price = q.sma[idx]
        #price = q.lower_ev_sigma[idx]
        return price

    def create_order_close_stop_market_short(self, q, idx):
        if not self._check_quotes(q, idx):
            return 0.00
        price = q.quotes['high'][idx] + self.tick
        #price = q.sma[idx]
        #price = q.upper_ev_sigma[idx]
        return price

    def create_order_close_market_long(self, q, idx):
        return 0.00

    def create_order_close_market_short(self, q, idx):
        return 0.00

    def create_order_market_long_for_all_cash(self, cash, q, idx):
        if not self._check_quotes(q, idx) or cash <= 0:
            return (-1, -1)
        price = q.quotes['close'][idx]
        vol = math.floor((cash / price) * -1)
        return (price, vol)

    def create_order_market_short_for_all_cash(self, cash, q, idx):
        if not self._check_quotes(q, idx) or cash <= 0:
            return (-1, -1)
        price = q.quotes['close'][idx]
        vol = math.floor((cash / price) * -1)
        return (price, vol)