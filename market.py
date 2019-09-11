# -*- coding: utf-8 -*-

import numpy
import my_logger
from position import Position
from ordertype import OrderType

class Market():
    def __init__(self, logger=None):
        if logger is None:
            self.logger = my_logger.Logger().logger
        else:
            self.logger = logger
        self.logger.info('Market()')

    def simulator_run(self, title, strategy_id, strategy_option, quotes, butler, symbol, initial_cash, trade_fee, tick):
        P = Position(initial_cash, trade_fee, tick)
        backtest_history = list()
        for idx, high in enumerate(quotes.quotes['high']):
            if idx < quotes.ma_duration:
                continue
            current_position = p.get_position()
            low = quotes.quotes['low'][idx]
            open_price = quotes.quotes['open'][idx]
            business_date = quotes.quotes['business_date'][idx]
            order_info = { 'create_date':'' ,'order_date':'' ,'order_type':0 ,'order_status':0 ,'vol':0.00 ,'price':0.00 }
            call_order_info = { 'create_date':'' ,'order_date':'' ,'order_type':0 ,'order_status':0 ,'vol':0.00 ,'price':0.00 }
            execution_order_info = { 'close_order_date':'' ,'order_type':0 ,'order_status':0 ,'vol':0.00 ,'price':0.00 }
            trade_perfomance = { 'profit_value': 0.00, 'profit_rate': 0.00 }
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
                set_order_info(call_order_info, p.order)
            # 注文がある場合、約定判定
            if current_position == PositionType.NOTHING and p.order != None:
                if p.order.order_type == OrderType.STOP_MARKET_LONG:
                    #約定判定
                    if p.order.price == -1:
                        logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    elif high >= p.order.price and open_price >= p.order.price: #寄り付きが高値の場合
                        #最大volまで購入
                        p.open_long(business_date, open_price)
                    elif high >= p.order.price:
                        p.open_long(business_date, p.order.price)
                    else:
                        p.order.fail_order()
                    set_order_info(execution_order_info, p.order)
                elif p.order.order_type == OrderType.STOP_MARKET_SHORT:
                    #約定判定
                    if p.order.price == -1:
                        logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    elif low <= p.order.price and open_price <= p.order.price: #寄り付きが安値の場合
                        #最大volまで購入
                        p.open_short(business_date, open_price)
                    elif low <= p.order.price:
                        p.open_short(business_date, p.order.price)
                    else:
                        p.order.fail_order()
                    set_order_info(execution_order_info, p.order)
                elif p.order.order_type == OrderType.MARKET_LONG:
                    #約定判定
                    if p.order.price == -1:
                        logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    else:
                        #最大volまで購入
                        p.open_long(business_date, open_price)
                    set_order_info(execution_order_info, p.order)
                elif p.order.order_type == OrderType.MARKET_SHORT:
                    #約定判定
                    if p.order.price == -1:
                        logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    else:
                        #最大volまで購入
                        p.open_short(business_date, open_price)
                    set_order_info(execution_order_info, p.order)
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
                set_order_info(execution_order_info, p.order)
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
                set_order_info(execution_order_info, p.order)
            #注文は1日だけ有効
            p.clear_order()
    
            # 引け後、翌日の注文作成
            current_position = p.get_position()
            if current_position == PositionType.NOTHING:
                long_order_type = butler.check_open_long(quotes, idx)
                short_order_type = butler.check_open_short(quotes, idx)
                if long_order_type == OrderType.STOP_MARKET_LONG:
                    #create stop market long
                    t = butler.create_order_stop_market_long_for_all_cash(p.cash, quotes, idx)
                    p.create_order_stop_market_long(business_date, t[0], t[1])
                    set_order_info(order_info, p.order)
                elif short_order_type == OrderType.STOP_MARKET_SHORT:
                    #create stop market short
                    t = butler.create_order_stop_market_short_for_all_cash(p.cash, quotes, idx)
                    p.create_order_stop_market_short(business_date, t[0], t[1])
                    set_order_info(order_info, p.order)
                elif long_order_type == OrderType.MARKET_LONG:
                    t = butler.create_order_market_long_for_all_cash(p.cash, quotes, idx)
                    p.create_order_market_long(business_date, t[0], t[1])
                    set_order_info(order_info, p.order)
                elif short_order_type == OrderType.MARKET_SHORT:
                    t = butler.create_order_market_short_for_all_cash(p.cash, quotes, idx)
                    p.create_order_market_short(business_date, t[0], t[1])
                    set_order_info(order_info, p.order)
            elif current_position == PositionType.LONG:
                close_order_type = butler.check_close_long(p.pos_price, quotes, idx)
                if close_order_type == OrderType.CLOSE_STOP_MARKET_LONG:
                    #逆指値成行買い返済注文
                    price = butler.create_order_close_stop_market_long(quotes, idx)
                    p.create_order_close_stop_market_long(business_date, price, p.pos_vol)
                    set_order_info(order_info, p.order)
                elif close_order_type == OrderType.CLOSE_MARKET_LONG:
                    #成行買い返済注文
                    price = butler.create_order_close_market_long(quotes, idx)
                    p.create_order_close_market_long(business_date, price, p.pos_vol)
                    set_order_info(order_info, p.order)
                else:
                    pass #注文無し
            elif current_position == PositionType.SHORT:
                close_order_type = butler.check_close_short(p.pos_price, quotes, idx)
                if close_order_type == OrderType.CLOSE_STOP_MARKET_SHORT:
                    #逆指値成行売り返済注文
                    price = butler.create_order_close_stop_market_short(quotes, idx)
                    p.create_order_close_stop_market_short(business_date, price, p.pos_vol)
                    set_order_info(order_info, p.order)
                if close_order_type == OrderType.CLOSE_MARKET_SHORT:
                    #成行売り返済注文
                    price = butler.create_order_close_market_short(quotes, idx)
                    p.create_order_close_market_short(business_date, price, p.pos_vol)
                    set_order_info(order_info, p.order)
                else:
                    pass #注文無し
            #1日の結果を出力
            close = 0
            if quotes.quotes['close'][idx] is None:
                close = 0
            else:
                close = quotes.quotes['close'][idx]
            history = make_history(
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
                , p.cash
                , p.pos_vol
                , p.pos_price
                , round(p.cash + p.pos_vol * close, 2)
                , trade_perfomance
                )
            backtest_history.append(history)
        #シミュレーション結果を出力
        summary_msg_log = make_summary_msg(symbol, strategy_id, strategy_option, title, p.summary, quotes)
        save_history(backtest_history)
        logger.info(summary_msg_log)
    
