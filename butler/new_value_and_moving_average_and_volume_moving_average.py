
import math
from position import Position

class Butler():
    #アルゴリズム
    '''
    # 新値法+移動平均
     1. ??日移動平均のトレンドに沿った前日高値または安値を更新した場合、順張りでポジションを持つ
     2. ポジションと逆の??日高値または安値を更新した場合、ポジションを解消する
    '''

    def __init__(self, duration):
        self.nv_duration = duration

    def check_open_long(self, q, idx):
        #高値更新, 終値が移動平均より上、出来高が移動平均より上
        if q.quotes['high'][idx] is None or q.quotes['close'][idx] is None or q.quotes['volume'][idx] is None:
            return False
        past_high = self.get_maximum_high_price_for_nv(q, idx)
        today_high = q.quotes['high'][idx]
        today_close = q.quotes['close'][idx]
        today_volume = q.quotes['volume'][idx]
        today_sma = q.sma[idx]
        today_vol_ma = q.vol_ma[idx]
        if today_high > past_high and today_close > today_sma and today_volume > today_vol_ma:
            return True
        else:
            return False

    def check_open_short(self, q, idx):
        #安値更新, 終値が移動平均より下、出来高が移動平均より上
        if q.quotes['low'][idx] is None or q.quotes['close'][idx] is None or q.quotes['volume'][idx] is None:
            return False
        past_low = self.get_minimum_low_price_for_nv(q, idx)
        today_low = q.quotes['low'][idx]
        today_volume = q.quotes['volume'][idx]
        today_sma = q.sma[idx]
        today_close = q.quotes['close'][idx]
        today_vol_ma = q.vol_ma[idx]
        if past_low > today_low and today_sma > today_close and today_volume > today_vol_ma:
            return True
        else:
            return False

    def check_close_long(self, pos_price, q, idx):
        #新値＋移動平均でポジションがある場合、ポジションクローズの逆指値注文は毎日必ず入れる
        return True

    def check_close_short(self, pos_price, q, idx):
        #新値＋移動平均でポジションがある場合、ポジションクローズの逆指値注文は毎日必ず入れる
        return True

    def create_order_stop_market_long_for_all_cash(self, cash, price, tick):
        price = round(price + tick, 2)
        vol = math.floor(cash / price)
        return (price, vol)
 
    def get_price_stop_market_long(self, price, tick):
        price = round(price + tick, 2)
        return price

    def get_price_stop_market_short(self, price, tick):
        price = round(price + tick, 2)
        return price

    def create_order_stop_market_short_for_all_cash(self, cash, price, tick):
        price = round(price - tick, 2)
        vol = math.floor((cash / price) * -1)
        return (price, vol)

    def create_order_stop_market_close_long(self, q, idx, tick):
        price = self.get_minimum_low_price_for_nv(q, idx)
        return round(price-tick,2)

    def create_order_stop_market_close_short(self, q, idx, tick):
        price = self.get_maximum_high_price_for_nv(q, idx)
        return round(price+tick,2)

    def get_maximum_high_price_for_nv(self, q, idx):
        maxlength = len(q.quotes)
        if maxlength < self.nv_duration or idx < self.nv_duration:
            return -1
        ary = q.quotes['high'][idx-self.nv_duration:idx]
        return max(ary)

    def get_minimum_low_price_for_nv(self, q, idx):
        maxlength = len(q.quotes)
        if maxlength < self.nv_duration or idx < self.nv_duration:
            return -1
        ary = q.quotes['low'][idx-self.nv_duration:idx]
        return min(ary)
