# -*- coding: utf-8 -*-

import math

class Assets():
    def __init__(self, initial_cash, max_leverage=3.0, min_leverage=0.1, margin_remaining_ratio=0.33):
        self.initial_cash = initial_cash
        self.before_cash = initial_cash
        self.cash = initial_cash
        self.max_leverage = max_leverage
        self.min_leverage = min_leverage
        self.margin_remaining_ratio = margin_remaining_ratio

    def get_losscut_ratio(self, symbol):
        losscut_ratio = 0.03
        if 'XBTUSD' == symbol or 'ETHUSD' == symbol:
            losscut_ratio = 0.05
        elif 'GBPJPY' == symbol or 'USDJPY' == symbol:
            losscut_ratio = 0.005 #TODO:調整
        return losscut_ratio

    def _calc_leverage(self, factor):
        #TODO:factor対応
        return 3

    def get_margin_cash(self, factor=1):
        leverage = self._calc_leverage(factor)
        return math.floor(self.cash * leverage)

    def get_max_vol(self, price, factor=1):
        #TODO:最小単元
        margin_cash = self.get_margin_cash(factor)
        return math.floor(margin_cash / price)

    def open_long(self, price, vol):
        self.before_cash = self.cash
        self.cash = round(self.cash - price * vol, 2)

    def open_short(self, price, vol):
        self.before_cash = self.cash
        self.cash = round(self.cash + price * (vol*-1), 2)

    def close_long(self, price, vol):
        self.cash = round(self.cash + (price * vol), 2)

    def close_short(self, price, vol):
        self.cash = round(self.cash + (price * vol), 2)

