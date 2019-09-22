# -*- coding: utf-8 -*-

import numpy
import mylogger
from position import Position
from positiontype import PositionType
from ordertype import OrderType
from orderstatus import OrderStatus
from backtest_dumper import BacktestDumper

class Market():
    def __init__(self, logger=None):
        if logger is None:
            self.logger = mylogger.Logger().myLogger()
        else:
            self.logger = logger
        self.dumper = BacktestDumper()

    def simulator_run(self, title, strategy_id, strategy_option, quotes, butler, symbol, assets, trade_fee):
        p = Position(assets)
        backtest_history = list()
        for idx, high in enumerate(quotes.quotes['high']):
            if idx < quotes.ma_duration:
                continue
            current_position = p.get_position()
            low = quotes.quotes['low'][idx]
            open_price = quotes.quotes['open'][idx]
            close_price = quotes.quotes['close'][idx]
            business_date = quotes.quotes['business_date'][idx]
            order_info = { 'create_date':'' ,'order_date':'' ,'order_type':0 ,'order_status':0 ,'vol':0.00 ,'price':0.00 }
            call_order_info = { 'create_date':'' ,'order_date':'' ,'order_type':0 ,'order_status':0 ,'vol':0.00 ,'price':0.00 }
            execution_order_info = { 'close_order_date':'' ,'order_type':0 ,'order_status':0 ,'vol':0.00 ,'price':0.00 }
            trade_perfomance = { 'profit_value': 0.00, 'profit_rate': 0.00 }
            leverage = 0
            try:
                if (open_price is None
                    or low is None
                    or high is None
                    or numpy.isnan(open_price) 
                    or numpy.isnan(low) 
                    or numpy.isnan(high)
                    ):
                    self.logger.warning('[%s][%d] ohlc is None or nan' % (symbol, idx))
                    continue
            except Exception as err:
                self.logger.error('[%s][%d] ohlc is exception value:[%s]' % (symbol, idx, err))
                continue
    
            # 開場 
            # 注文を呼び出す
            if p.order != None:
                p.call_order(business_date)
                self.set_order_info(call_order_info, p.order)
            # 注文がある場合、約定判定
            if current_position == PositionType.NOTHING and p.order != None:
                if p.order.order_type == OrderType.STOP_MARKET_LONG:
                    #約定判定
                    if p.order.price == -1:
                        self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    elif p.order.vol == 0:
                        p.order.fail_order()
                    elif high >= p.order.price and open_price >= p.order.price: #寄り付きが高値の場合
                        #最大volまで購入
                        order_price = open_price
                        (margin_cash, leverage) = assets.get_margin_cash(symbol)
                        order_vol = butler.get_order_vol(symbol, margin_cash, quotes, idx, order_price)
                        p.open_long(business_date, order_price, order_vol)
                    elif high >= p.order.price:
                        order_vol = p.order.vol
                        order_price = p.order.price
                        p.open_long(business_date, order_price, order_vol)
                    else:
                        p.order.fail_order()
                    self.set_order_info(execution_order_info, p.order)
                    #Open約定期間中のロスカット
                    if p.order.order_status == OrderStatus.EXECUTION:
                        #前日安値
                        losscut_price = order_price - (order_price * assets.get_losscut_ratio(symbol))
                        if low <= losscut_price:
                        #if close_price <= losscut_price:
                        #if False:
                        #before_low = quotes.quotes['low'][idx-1]
                        #if before_low >= low:
                            p.order.order_type = OrderType.CLOSE_STOP_MARKET_LONG
                            call_order_info['order_type'] = OrderType.CLOSE_STOP_MARKET_LONG
                            p.close_long(business_date, losscut_price)
                            #p.close_long(business_date, before_low)
                            trade_perfomance = p.save_trade_perfomance(PositionType.LONG)
                            self.set_order_info(execution_order_info, p.order)
                elif p.order.order_type == OrderType.STOP_MARKET_SHORT:
                    #約定判定
                    if p.order.price == -1:
                        self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    elif p.order.vol == 0:
                        p.order.fail_order()
                    elif low <= p.order.price and open_price <= p.order.price: #寄り付きが安値の場合
                        #最大volまで売却
                        order_price = open_price
                        (margin_cash, leverage) = assets.get_margin_cash(symbol)
                        order_vol = butler.get_order_vol(symbol, margin_cash, quotes, idx, order_price)
                        order_vol = order_vol * -1
                        p.open_short(business_date, order_price, order_vol)
                    elif low <= p.order.price:
                        order_price = p.order.price
                        order_vol = p.order.vol
                        p.open_short(business_date, p.order.price, p.order.vol)
                    else:
                        p.order.fail_order()
                    self.set_order_info(execution_order_info, p.order)
                    #Open約定期間中のロスカット
                    if p.order.order_status == OrderStatus.EXECUTION:
                        losscut_price = order_price + (order_price * assets.get_losscut_ratio(symbol))
                        if high >= losscut_price:
                        #if False:
                        #if close_price >= losscut_price:
                        #before_high= quotes.quotes['high'][idx-1]
                        #if before_high <= high:
                            p.order.order_type = OrderType.CLOSE_STOP_MARKET_SHORT
                            call_order_info['order_type'] = OrderType.CLOSE_STOP_MARKET_LONG
                            p.close_short(business_date, losscut_price)
                            #p.close_short(business_date, before_high)
                            trade_perfomance = p.save_trade_perfomance(PositionType.SHORT)
                            self.set_order_info(execution_order_info, p.order)
                elif p.order.order_type == OrderType.MARKET_LONG:
                    #約定判定
                    if p.order.price == -1:
                        self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    else:
                        #最大volまで購入
                        order_vol = assets.get_max_vol(open_price)
                        p.open_long(business_date, open_price, order_vol)
                    self.set_order_info(execution_order_info, p.order)
                elif p.order.order_type == OrderType.MARKET_SHORT:
                    #約定判定
                    if p.order.price == -1:
                        self.logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    else:
                        #最大volまで売却
                        order_vol = assets.get_max_vol(open_price) * -1
                        p.open_short(business_date, open_price, order_vol)
                    self.set_order_info(execution_order_info, p.order)
            elif current_position == PositionType.LONG and p.order != None:
                #約定判定
                if p.order.order_type == OrderType.CLOSE_STOP_MARKET_LONG: #逆指値成行買い返済
                    if low <= p.order.price and open_price <= p.order.price:
                        p.close_long(business_date, open_price)
                        trade_perfomance = p.save_trade_perfomance(PositionType.LONG)
                    elif low <= p.order.price:
                        p.close_long(business_date, p.order.price)
                        trade_perfomance = p.save_trade_perfomance(PositionType.LONG)
                    else:
                        p.order.fail_order()
                elif p.order.order_type == OrderType.CLOSE_MARKET_LONG: #成行買い返済
                    p.close_long(business_date, open_price)
                    trade_perfomance = p.save_trade_perfomance(PositionType.LONG)
                self.set_order_info(execution_order_info, p.order)
            elif current_position == PositionType.SHORT and p.order != None:
                #約定判定
                if p.order.order_type == OrderType.CLOSE_STOP_MARKET_SHORT: #逆指値成行売り返済
                    if high >= p.order.price and open_price >= p.order.price:
                        p.close_short(business_date, open_price)
                        trade_perfomance = p.save_trade_perfomance(PositionType.SHORT)
                    elif high >= p.order.price:
                        p.close_short(business_date, p.order.price)
                        trade_perfomance = p.save_trade_perfomance(PositionType.SHORT)
                    else:
                        p.order.fail_order()
                elif p.order.order_type == OrderType.CLOSE_MARKET_SHORT: #成行売り返済
                    p.close_short(business_date, open_price)
                    trade_perfomance = p.save_trade_perfomance(PositionType.SHORT)
                self.set_order_info(execution_order_info, p.order)
            #注文は1日だけ有効
            p.clear_order()
    
            # 引け後、翌日の注文作成
            current_position = p.get_position()
            if current_position == PositionType.NOTHING:
                long_order_type = butler.check_open_long(quotes, idx)
                short_order_type = butler.check_open_short(quotes, idx)
                if long_order_type == OrderType.STOP_MARKET_LONG:
                    #create stop market long
                    (margin_cash, leverage) = assets.get_margin_cash(symbol)
                    (price, vol) = butler.create_order_stop_market_long_for_all_cash(symbol, margin_cash, quotes, idx)
                    if vol > 0:
                        p.create_order_stop_market_long(business_date, price, vol)
                        self.set_order_info(order_info, p.order)
                elif short_order_type == OrderType.STOP_MARKET_SHORT:
                    #create stop market short
                    (margin_cash, leverage) = assets.get_margin_cash(symbol)
                    (price, vol) = butler.create_order_stop_market_short_for_all_cash(symbol, margin_cash, quotes, idx)
                    if vol < 0:
                        p.create_order_stop_market_short(business_date, price, vol)
                        self.set_order_info(order_info, p.order)
                elif long_order_type == OrderType.MARKET_LONG:
                    (margin_cash, leverage) = assets.get_margin_cash(symbol)
                    (price, vol) = butler.create_order_market_long_for_all_cash(symbol, margin_cash, quotes, idx)
                    if vol > 0:
                        p.create_order_market_long(business_date, price, vol)
                        self.set_order_info(order_info, p.order)
                elif short_order_type == OrderType.MARKET_SHORT:
                    (margin_cash, leverage) = assets.get_margin_cash(symbol)
                    (price, vol) = butler.create_order_market_short_for_all_cash(symbol, margin_cash, quotes, idx)
                    if vol > 0:
                        p.create_order_market_short(business_date, price, vol)
                        self.set_order_info(order_info, p.order)
            elif current_position == PositionType.LONG:
                close_order_type = butler.check_close_long(p.pos_price, quotes, idx)
                if close_order_type == OrderType.CLOSE_STOP_MARKET_LONG:
                    #逆指値成行買い返済注文
                    price = butler.create_order_close_stop_market_long(quotes, idx)
                    p.create_order_close_stop_market_long(business_date, price, p.pos_vol)
                    self.set_order_info(order_info, p.order)
                elif close_order_type == OrderType.CLOSE_MARKET_LONG:
                    #成行買い返済注文
                    price = butler.create_order_close_market_long(quotes, idx)
                    p.create_order_close_market_long(business_date, price, p.pos_vol)
                    self.set_order_info(order_info, p.order)
                else:
                    pass #注文無し
            elif current_position == PositionType.SHORT:
                close_order_type = butler.check_close_short(p.pos_price, quotes, idx)
                if close_order_type == OrderType.CLOSE_STOP_MARKET_SHORT:
                    #逆指値成行売り返済注文
                    price = butler.create_order_close_stop_market_short(quotes, idx)
                    p.create_order_close_stop_market_short(business_date, price, p.pos_vol)
                    self.set_order_info(order_info, p.order)
                if close_order_type == OrderType.CLOSE_MARKET_SHORT:
                    #成行売り返済注文
                    price = butler.create_order_close_market_short(quotes, idx)
                    p.create_order_close_market_short(business_date, price, p.pos_vol)
                    self.set_order_info(order_info, p.order)
                else:
                    pass #注文無し
            #1日の結果を出力
            close = 0
            if quotes.quotes['close'][idx] is None:
                close = 0
            else:
                close = quotes.quotes['close'][idx]
            history = self.dumper.make_history(
                  symbol
                , strategy_id
                , strategy_option
                , business_date
                , quotes
                , idx
                , order_info
                , call_order_info
                , execution_order_info
                , p.position
                , assets.cash
                , p.pos_vol
                , p.pos_price
                , round(assets.cash + p.pos_vol * close, 2)
                , trade_perfomance
                , leverage
                )
            backtest_history.append(history)
        #シミュレーション結果を出力
        summary_msg_log = self.dumper.make_summary_msg(symbol, strategy_id, strategy_option, title, p.summary, quotes)
        self.dumper.save_history(backtest_history)
        self.logger.info(summary_msg_log)
    
    def set_order_info(self, info, order):
        info['create_date'] = order.create_date
        info['order_date'] = order.order_date
        info['close_order_date'] = order.close_order_date
        info['order_type'] = order.order_type
        info['order_status'] = order.order_status
        info['vol'] = order.vol
        info['price'] = order.price

