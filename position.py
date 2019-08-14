
import math
import datetime
import order
from positiontype import PositionType
from ordertype import OrderType 
from orderstatus import OrderStatus

class Position():
    def __init__(self, initial_cash, trade_fee, tick):
       self.position = PositionType.NOTHING
       self.pos_price = 0
       self.pos_vol = 0
       self.trade_fee = 0
       self.cash = initial_cash
       self.order = None
       self.before_cash = 0.00
       self.win_count = 0
       self.lose_count = 0
       self.profit_value_sum = 0
       self.profit_rate_sum = 0
       self.summary = {
             'WinCount':0
            ,'LoseCount':0
            ,'WinValue':0.00
            ,'LoseValue':0.00
            ,'InitValue':initial_cash
            ,'LastValue':initial_cash
            ,'ProfitRateSummary':0.00
            ,'PositionHavingDays':0
            ,'LongWinCount':0
            ,'LongLoseCount':0
            ,'LongWinValue':0.00
            ,'LongLoseValue':0.00
            ,'LongProfitRateSummary':0.00
            ,'LongPositionHavingDays':0
            ,'ShortWinCount':0
            ,'ShortLoseCount':0
            ,'ShortWinValue':0.00
            ,'ShortLoseValue':0.00
            ,'ShortProfitRateSummary':0.00
            ,'ShortPositionHavingDays':0
        }

    def get_position(self):
        return self.position

    def create_order_stop_market_long(self, create_date, price, vol):
        self.order = order.Order()
        self.order.set_order(create_date, OrderType.STOP_MARKET_LONG, price, vol)
    
    def create_order_stop_market_short(self, create_date, price, vol):
        self.order = order.Order()
        self.order.set_order(create_date, OrderType.STOP_MARKET_SHORT, price, vol)
    
    def create_order_stop_market_close_long(self, create_date, price, vol):
        self.order = order.Order()
        self.order.set_order(create_date, OrderType.CLOSE_STOP_MARKET_LONG, price, vol)
    
    def create_order_stop_market_close_short(self, create_date, price, vol):
        self.order = order.Order()
        self.order.set_order(create_date, OrderType.CLOSE_STOP_MARKET_SHORT, price, vol)

    def call_order(self, order_date):
        self.order.order(order_date)

    def clear_order(self):
        self.order = None

    def open_long(self, business_date, order_price):
        self.position = PositionType.LONG
        self.order.price = order_price
        self.pos_price = self.order.price
        self.pos_vol = self.order.vol
        self.before_cash = self.cash
        self.cash = round(self.cash - self.pos_vol * self.pos_price, 2)
        self.order.execution_order(business_date)
        self.order_date = self.order.order_date

    def open_short(self, business_date, order_price):
        self.position = PositionType.SHORT
        self.order.price = order_price
        self.pos_price = self.order.price
        self.pos_vol = self.order.vol
        self.before_cash = self.cash
        self.cash = round(self.cash + (self.pos_vol*-1) * self.pos_price, 2)
        self.order.execution_order(business_date)
        self.order_date = self.order.order_date

    def close_long(self, business_date, order_price):
        self.position = PositionType.NOTHING
        self.order.price = order_price
        self.pos_price = self.order.price
        self.cash = round(self.cash + (self.pos_vol * self.pos_price), 2)
        self.pos_vol = 0
        self.order.execution_order(business_date)
        self.close_date = self.order.close_order_date
        start_date = datetime.datetime.strptime(self.order_date, "%Y-%m-%d")
        close_date = datetime.datetime.strptime(self.close_date, "%Y-%m-%d")
        self.summary['PositionHavingDays'] += (close_date - start_date).days
        self.summary['LongPositionHavingDays'] += (close_date - start_date).days

    def close_short(self, business_date, order_price):
        self.position = PositionType.NOTHING
        self.order.price = order_price
        self.pos_price = self.order.price
        self.cash = round(self.cash + (self.pos_vol * self.pos_price), 2)
        self.pos_vol = 0
        self.order.execution_order(business_date)
        self.close_date = self.order.close_order_date
        start_date = datetime.datetime.strptime(self.order_date, "%Y-%m-%d")
        close_date = datetime.datetime.strptime(self.close_date, "%Y-%m-%d")
        self.summary['PositionHavingDays'] += (close_date - start_date).days
        self.summary['ShortPositionHavingDays'] += (close_date - start_date).days

    def save_trade_perfomance(self, order_type):
        win = 0
        lose = 0
        if self.before_cash < self.cash:
            win = 1
        else:
            lose = 1
        profit_value = self.cash - self.before_cash
        profit_rate = profit_value / self.before_cash * 100
        trade_perfomance = {
              'before_cash': self.before_cash
            , 'cash': self.cash
            , 'win': win
            , 'lose': lose
            , 'profit_value': profit_value
            , 'profit_rate': profit_rate
        }
        self.summary['WinCount'] += win
        self.summary['LoseCount'] += lose
        if order_type == OrderType.STOP_MARKET_LONG:
            self.summary['LongWinCount'] += win
            self.summary['LongLoseCount'] += lose
        if order_type == OrderType.STOP_MARKET_SHORT:
            self.summary['ShortWinCount'] += win
            self.summary['ShortLoseCount'] += lose

        if win == 1:
            self.summary['WinValue'] += profit_value
            if order_type == OrderType.STOP_MARKET_LONG:
                self.summary['LongWinValue'] += profit_value
            if order_type == OrderType.STOP_MARKET_SHORT:
                self.summary['ShortWinValue'] += profit_value
        else:
            self.summary['LoseValue'] += abs(profit_value)
            if order_type == OrderType.STOP_MARKET_LONG:
                self.summary['LongLoseValue'] += abs(profit_value)
            if order_type == OrderType.STOP_MARKET_SHORT:
                self.summary['ShortLoseValue'] += abs(profit_value)
        self.summary['LastValue'] = self.cash + (self.pos_vol * self.pos_price)
        self.summary['ProfitRateSummary'] += profit_rate
        if order_type == OrderType.STOP_MARKET_LONG:
            self.summary['LongProfitRateSummary'] += profit_rate
        if order_type == OrderType.STOP_MARKET_SHORT:
            self.summary['ShortProfitRateSummary'] += profit_rate
        return trade_perfomance

    def get_perfomance(self):
        return (self.before_cash, self.cash)
