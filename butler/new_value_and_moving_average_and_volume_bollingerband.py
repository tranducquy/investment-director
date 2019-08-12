
import math
from position import Position

class Butler():
    #アルゴリズム
    '''
    # 新値法+移動平均
     1. ??日移動平均のトレンドに沿った前日高値または安値を更新した場合、順張りでポジションを持つ
     2. ポジションと逆の??日高値または安値を更新した場合、ポジションを解消する
    '''

    def __init__(self, tick, duration):
        self.nv_duration = duration
        self.tick = tick

    def check_open_long(self, q, idx):
        #高値更新, 終値が移動平均より上、出来高がσより上
        if (q.quotes['high'][idx] is None 
                or q.quotes['close'][idx] is None 
                or q.quotes['volume'][idx] is None
                or q.vol_upper_ev_sigma[idx] is None):
            return False
        past_high = self._get_maximum_high_price_for_nv(q, idx)
        today_high = q.quotes['high'][idx]
        today_close = q.quotes['close'][idx]
        today_volume = float(q.quotes['volume'][idx])
        today_sma = q.sma[idx]
        today_vol_sigma = q.vol_upper_ev_sigma[idx]
        if today_high > past_high and today_close > today_sma and today_volume > today_vol_sigma:
            return True
        else:
            return False

    def check_open_short(self, q, idx):
        #安値更新, 終値が移動平均より下、出来高がσより上
        if (q.quotes['low'][idx] is None 
                or q.quotes['close'][idx] is None 
                or q.quotes['volume'][idx] is None
                or q.vol_upper_ev_sigma[idx] is None):
            return False
        past_low = self._get_minimum_low_price_for_nv(q, idx)
        today_low = q.quotes['low'][idx]
        today_volume = float(q.quotes['volume'][idx])
        today_sma = q.sma[idx]
        today_close = q.quotes['close'][idx]
        today_vol_sigma = q.vol_upper_ev_sigma[idx]
        if past_low > today_low and today_sma > today_close and today_volume > today_vol_sigma:
            return True
        else:
            return False

    def check_close_long(self, pos_price, q, idx):
        #新値＋移動平均でポジションがある場合、ポジションクローズの逆指値注文は毎日必ず入れる
        return True

    def check_close_short(self, pos_price, q, idx):
        #新値＋移動平均でポジションがある場合、ポジションクローズの逆指値注文は毎日必ず入れる
        return True

    def create_order_stop_market_long_for_all_cash(self, cash, q, idx):
        if q.quotes['high'][idx] is None or cash <= 0:
            return (-1, -1)
        price = self.create_order_stop_market_close_long(q, idx)
        vol = math.floor(cash / price)
        return (price, vol)

    def create_order_stop_market_long(self, q, idx):
        if q.quotes['high'][idx] is None:
            return -1
        price = q.quotes['high'][idx] + self.tick
        return price

    def create_order_stop_market_short_for_all_cash(self, cash, q, idx):
        if q.quotes['low'][idx] is None or cash <= 0:
            return (-1, -1)
        price = self.create_order_stop_market_close_short(q, idx)
        vol = math.floor((cash / price) * -1)
        return (price, vol)

    def create_order_stop_market_short(self, q, idx):
        if q.quotes['low'][idx] is None:
            return -1
        price = q.quotes['low'][idx] - self.tick
        return price

    def create_order_stop_market_close_long(self, q, idx):
        if q.quotes['low'][idx] is None:
            return -1
        price = q.quotes['low'][idx] - self.tick
        return price

    def create_order_stop_market_close_short(self, q, idx):
        if q.quotes['high'][idx] is None:
            return -1
        price = q.quotes['high'][idx] + self.tick
        return price

    def _get_maximum_high_price_for_nv(self, q, idx):
        maxlength = len(q.quotes)
        if maxlength < self.nv_duration or idx < self.nv_duration:
            return -1
        ary = q.quotes['high'][idx-self.nv_duration:idx]
        return max(ary)

    def _get_minimum_low_price_for_nv(self, q, idx):
        maxlength = len(q.quotes)
        if maxlength < self.nv_duration or idx < self.nv_duration:
            return -1
        ary = q.quotes['low'][idx-self.nv_duration:idx]
        return min(ary)
