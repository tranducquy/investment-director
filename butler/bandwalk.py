
import math
import numpy
from position import Position
from ordertype import OrderType
from butler import bollingerband

class Butler(bollingerband.Butler):
    #アルゴリズム
    '''
    # ボリンジャーバンドのバンドウォークを判定
    '''
    def __init__(self, tick, bollinger_duration, diff_price, bandwalk_duration):
        self.duration = bollinger_duration
        self.diff_price = diff_price 
        self.tick = tick
        self.only_stop_market_order = True
        self.bandwalk_duration = bandwalk_duration
        self.upper_bandwalk = dict()
        self.lower_bandwalk = dict()
    
    def check_open_long(self, q, idx):
        if not self._check_quotes(q, idx):
            return OrderType.NONE_ORDER
        self.upper_bandwalk[idx] = q.quotes['high'][idx] >= q.upper_ev_sigma[idx]
        #self.upper_bandwalk[idx] = q.quotes['close'][idx] >= q.upper_ev_sigma[idx]
        try:
            if self.upper_hbandwalk[idx-1] and self.upper_bandwalk[idx]:
                return OrderType.STOP_MARKET_LONG
            else:
                return OrderType.NONE_ORDER
        except:
                return OrderType.NONE_ORDER

    def check_open_short(self, q, idx):
        #当日安値がevσ以下
        if not self._check_quotes(q, idx):
            return OrderType.NONE_ORDER
        self.lower_bandwalk[idx] = q.quotes['low'][idx] <= q.lower_ev_sigma[idx]
        #self.lower_bandwalk[idx] = q.quotes['close'][idx] <= q.lower_ev_sigma[idx]
        try:
            if self.lower_bandwalk[idx-1] and self.lower_bandwalk[idx]:
                return OrderType.STOP_MARKET_SHORT
            else:
                return OrderType.NONE_ORDER
        except:
            return OrderType.NONE_ORDER
