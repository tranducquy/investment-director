
import math
import numpy
from position import Position
from ordertype import OrderType

class Butler():
    def __init__(self, tick, bollinger_duration, order_vol_ratio=0.01):
        self.duration = bollinger_duration
        self.diff_price = 0.0
        self.order_vol_ratio = order_vol_ratio
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

    def get_unit(self, symbol):
        if ('1570.T' in symbol 
            or '1357.T' in symbol
            or '1568.T' in symbol
            or '1356.T' in symbol):
            unit = 1
        elif '.T' in symbol:
            unit = 100
        else:
            unit = 1
        return unit

    def get_order_vol(self, symbol, cash, q, idx, price):
        unit = self.get_unit(symbol)
        order_vol_from_cash = math.floor(cash / price / unit) * unit
        #出来高平均
        current_vol = q.vol_sma[idx]
        if math.isnan(current_vol) or current_vol < 0:
            current_vol = -1
        #出来高平均から発注数量を取得
        temp_vol = current_vol * self.order_vol_ratio
        order_vol_from_sma = math.floor(temp_vol / unit) * unit
        if 'XBTUSD' == symbol or 'ETHUSD' == symbol or 'USDJPY' == symbol or 'GBPJPY' == symbol or 'EURJPY' == symbol or 'EURUSD' == symbol:
            vol = order_vol_from_cash
        elif current_vol == -1:
            vol = 0
        elif order_vol_from_cash < order_vol_from_sma:
            vol = order_vol_from_cash
        else:
            vol = order_vol_from_sma
        return vol

    def create_order_stop_market_long_for_all_cash(self, symbol, cash, q, idx):
        if not self._check_quotes(q, idx) or cash <= 0:
            return (-1, -1)
        price = self.create_order_stop_market_long(q, idx)
        vol = self.get_order_vol(symbol, cash, q, idx, price)
        return (price, vol)

    def create_order_stop_market_short_for_all_cash(self, symbol, cash, q, idx):
        if not self._check_quotes(q, idx) or cash <= 0:
            return (-1, -1)
        price = self.create_order_stop_market_short(q, idx)
        vol = self.get_order_vol(symbol, cash, q, idx, price)
        return (price, vol * -1)

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

    def create_order_market_long_for_all_cash(self, symbol, cash, q, idx):
        if not self._check_quotes(q, idx) or cash <= 0:
            return (-1, -1)
        price = q.quotes['close'][idx]
        vol = self.get_order_vol(symbol, cash, q, idx, price)
        return (price, vol)

    def create_order_market_short_for_all_cash(self, symbol, cash, q, idx):
        if not self._check_quotes(q, idx) or cash <= 0:
            return (-1, -1)
        price = q.quotes['close'][idx]
        vol = self.get_order_vol(symbol, cash, q, idx, price)
        return (price, vol * -1)
