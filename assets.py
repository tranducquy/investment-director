# -*- coding: utf-8 -*-

class Assets():
    def __init__(self, initial_cash, max_leverage=5.0, min_leverage=0.1, margin_remaining_ratio=0.3, loss_cut=0.3):
        self.cash = initial_cash
        self.max_leverage = max_leverage
        self.min_leverage = min_leverage
        self.margin_remaining_ratio = margin_remaining_ratio

    def get_margin_remaining(self):
        return self.cash / self.margin_remaining_ratio
