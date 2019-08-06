
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
        #高値更新, 終値が移動平均より上
        past_high = self.get_maximum_high_price_for_nv(q, idx)
        if q.quotes['high'][idx] > past_high and q.quotes['close'][idx] > q.sma[idx]:
            return True
        else:
            return False

    def check_open_short(self, q, idx):
        #安値更新, 終値が移動平均より下
        past_low = self.get_minimum_low_price_for_nv(q, idx)
        if past_low > q.quotes['low'][idx] and q.sma[idx] > q.quotes['close'][idx]:
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
        if maxlength < self.nv_duration:
            return -1
        ary = q.quotes['high'][idx-self.nv_duration-1:idx-1]
        return max(ary)

    def get_minimum_low_price_for_nv(self, q, idx):
        maxlength = len(q.quotes)
        if maxlength < self.nv_duration:
            return -1
        ary = q.quotes['high'][idx-self.nv_duration-1:idx-1]
        return min(ary)
