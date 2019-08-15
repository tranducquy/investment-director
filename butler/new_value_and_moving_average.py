
import math
import numpy
from position import Position
from ordertype import OrderType

class Butler():
    #アルゴリズム
    '''
    # 新値法+終値移動平均+出来高移動平均
     1. ??日終値移動平均+??日出来高移動平均のトレンドに沿った前日高値または安値を更新した場合、順張りでポジションを持つ
     2. ポジションと逆の??日高値または安値を更新した場合、ポジションを解消する
    '''

    def __init__(self, tick, nv_duration):
        self.nv_duration = nv_duration
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

    def _check_volume(self, q, idx):
        if (
            q.quotes['volume'][idx] is None 
                or q.sma[idx] is None
                or q.vol_upper_ev_sigma[idx] is None 
                or q.vol_lower_ev_sigma[idx] is None
                or numpy.isnan(q.quotes['volume'][idx])
                or numpy.isnan(q.sma[idx])
                or numpy.isnan(q.vol_upper_ev_sigma[idx])
                or numpy.isnan(q.vol_lower_ev_sigma[idx])
                or q.quotes['volume'][idx] == 0
                ):
            return False
        else:
            return True

    def check_open_long(self, q, idx):
        #高値更新, 終値が移動平均より上、出来高が移動平均以上
        if not self._check_quotes(q, idx):
            return OrderType.NONE_ORDER
        if not self._check_volume(q, idx):
            return OrderType.NONE_ORDER
        past_high = self._get_maximum_high_price_for_nv(q, idx)
        today_high = q.quotes['high'][idx]
        today_close = q.quotes['close'][idx]
        today_volume = int(q.quotes['volume'][idx])
        today_sma = q.sma[idx]
        today_vol_ma = q.vol_ma[idx]
        if today_high > past_high and today_close > today_sma and today_volume >= today_vol_ma:
            return OrderType.STOP_MARKET_LONG
        else:
            return OrderType.NONE_ORDER

    def check_open_short(self, q, idx):
        #安値更新, 終値が移動平均より下、出来高が移動平均より上
        if not self._check_quotes(q, idx):
            return OrderType.NONE_ORDER
        if not self._check_volume(q, idx):
            return OrderType.NONE_ORDER
        past_low = self._get_minimum_low_price_for_nv(q, idx)
        today_low = q.quotes['low'][idx]
        today_volume = int(q.quotes['volume'][idx])
        today_sma = q.sma[idx]
        today_close = q.quotes['close'][idx]
        today_vol_ma = q.vol_ma[idx]
        if past_low > today_low and today_sma > today_close and today_volume >= today_vol_ma:
            return OrderType.STOP_MARKET_SHORT
        else:
            return OrderType.NONE_ORDER

    def check_close_long(self, pos_price, q, idx):
        #新値＋移動平均でポジションがある場合、ポジションクローズの逆指値注文は毎日必ず入れる
        return OrderType.CLOSE_STOP_MARKET_LONG

    def check_close_short(self, pos_price, q, idx):
        #新値＋移動平均でポジションがある場合、ポジションクローズの逆指値注文は毎日必ず入れる
        return OrderType.CLOSE_STOP_MARKET_SHORT

    def create_order_stop_market_long_for_all_cash(self, cash, q, idx):
        if not self._check_quotes(q, idx) or cash <= 0:
            return (-1, -1)
        price = self.create_order_stop_market_long(q, idx)
        vol = math.floor(cash / price)
        return (price, vol)

    def create_order_stop_market_long(self, q, idx):
        if not self._check_quotes(q, idx):
            return -1
        price = q.quotes['high'][idx] + self.tick
        return price

    def create_order_stop_market_short_for_all_cash(self, cash, q, idx):
        if not self._check_quotes(q, idx) or cash <= 0:
            return (-1, -1)
        price = self.create_order_stop_market_short(q, idx)
        vol = math.floor((cash / price) * -1)
        return (price, vol)

    def create_order_stop_market_short(self, q, idx):
        if not self._check_quotes(q, idx):
            return -1
        price = q.quotes['low'][idx] - self.tick
        return price

    def create_order_close_stop_market_long(self, q, idx):
        if not self._check_quotes(q, idx):
            return -1
        price = q.quotes['low'][idx] - self.tick
        return price

    def create_order_close_stop_market_short(self, q, idx):
        if not self._check_quotes(q, idx):
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


