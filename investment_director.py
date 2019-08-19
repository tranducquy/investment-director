
import sys
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy
import common
import my_logger
import quotes
from butler import bollingerband
from butler import new_value_and_moving_average
import tick
from position import Position
from positiontype import PositionType
from ordertype import OrderType

s = my_logger.Logger()
logger = s.myLogger()

def get_last_backtestdate(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    #バックテストの最終登録日を取得
    c.execute("""
    select
    max(regist_date)
    from backtest_result""")
    max_date = c.fetchone()
    conn.close()
    return max_date[0]

def _get_symbols(db, regist_date, today, end_date):
    #3ヶ月、1,3,15年のバックテストで利益の出ている銘柄のみ探す
    start_date_3month = (today - relativedelta(months=3)).strftime("%Y-%m-%d")
    start_date_1year = (today - relativedelta(years=1)).strftime("%Y-%m-%d")
    start_date_3year = (today - relativedelta(years=3)).strftime("%Y-%m-%d")
    start_date_15year = (today - relativedelta(years=15)).strftime("%Y-%m-%d")

    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql = """
    select
     m3.symbol
    ,m3.strategy
    ,m3.regist_date
    ,m3.rate_of_return as 騰落率3か月
    ,y1.rate_of_return as 騰落率1年
    ,y3.rate_of_return as 騰落率3年
    ,y15.rate_of_return as 騰落率15年
    ,m3.expected_rate as トレード当たりの期待値3か月
    ,y1.expected_rate as トレード当たりの期待値1年
    ,y3.expected_rate as トレード当たりの期待値3年
    ,y15.expected_rate as トレード当たりの期待値15年
    ,m3.expected_rate_per_1day as トレード1日当たりの期待値3か月
    ,y1.expected_rate_per_1day as トレード1日当たりの期待値1年
    ,y3.expected_rate_per_1day as トレード1日当たりの期待値3年
    ,y15.expected_rate_per_1day as トレード1日当たりの期待値15年
    ,m3.average_period_per_trade as 平均取引期間3か月
    ,y1.average_period_per_trade as 平均取引期間1年
    ,y3.average_period_per_trade as 平均取引期間3年
    ,y15.average_period_per_trade as 平均取引期間15年
    ,m3.win_rate as 勝率3か月
    ,y1.win_rate as 勝率1年
    ,y3.win_rate as 勝率3年
    ,y15.win_rate as 勝率15年
    ,m3.long_expected_rate as 期待利益率long3か月
    ,y1.long_expected_rate as 期待利益率long1年
    ,y3.long_expected_rate as 期待利益率long3年
    ,y15.long_expected_rate as 期待利益率long15年
    ,m3.long_expected_rate_per_1day as 一日当たりの期待利益率long3か月
    ,y1.long_expected_rate_per_1day as 一日当たりの期待利益率long1年
    ,y3.long_expected_rate_per_1day as 一日当たりの期待利益率long3年
    ,y15.long_expected_rate_per_1day as 一日当たりの期待利益率long15年
    ,m3.long_win_count+m3.long_loss_count as 取引数long3か月
    ,y1.long_win_count+y1.long_loss_count as 取引数long1年
    ,y3.long_win_count+y3.long_loss_count as 取引数long3年
    ,y15.long_win_count+y15.long_loss_count as 取引数long15年
    ,m3.short_expected_rate as 期待利益率short3か月
    ,y1.short_expected_rate as 期待利益率short1年
    ,y3.short_expected_rate as 期待利益率short3年
    ,y15.short_expected_rate as 期待利益率short15年
    ,m3.short_expected_rate_per_1day as 一日当たりの期待利益率short3か月
    ,y1.short_expected_rate_per_1day as 一日当たりの期待利益率short1年
    ,y3.short_expected_rate_per_1day as 一日当たりの期待利益率short3年
    ,y15.short_expected_rate_per_1day as 一日当たりの期待利益率short15年
    ,m3.short_win_count+m3.short_loss_count as 取引数short3か月
    ,y1.short_win_count+y1.short_loss_count as 取引数short1年
    ,y3.short_win_count+y3.short_loss_count as 取引数short3年
    ,y15.short_win_count+y15.short_loss_count as 取引数short15年
    ,m3.win_count+m3.loss_count as 取引数3か月
    ,y1.win_count+y1.loss_count as 取引数1年
    ,y3.win_count+y3.loss_count as 取引数3年
    ,y15.win_count+y15.loss_count as 取引数15年
   from backtest_result m3
   left outer join (
   select
    *
   from backtest_result
   where start_date = '%s'
   and end_date = '%s'
   and backtest_period > 300*1
   and rate_of_return > 0
   ) y1
   on m3.symbol = y1.symbol and m3.strategy = y1.strategy
   left outer join (
   select
    *
   from backtest_result
   where start_date = '%s'
   and end_date = '%s'
   and backtest_period > 300*3
   and rate_of_return > 0
   ) y3
   on m3.symbol = y3.symbol and m3.strategy = y3.strategy
   left outer join (
   select
    *
   from backtest_result
   where start_date = '%s'
   and end_date = '%s'
   and backtest_period > 300*15
   and rate_of_return > 0
   ) y15
   on m3.symbol = y15.symbol and m3.strategy = y15.strategy
   where m3.start_date = '%s'
   and m3.end_date = '%s'
   and m3.rate_of_return > 0
   and 
   (
       --(m3.rate_of_return < y1.rate_of_return and y1.rate_of_return < y3.rate_of_return and y3.rate_of_return < y15.rate_of_return)
       --or 
       (y1.rate_of_return > 15 and y3.rate_of_return > 45 and y15.rate_of_return > 225)
   )
   order by m3.rate_of_return desc
       """ % (
             start_date_1year, end_date
           , start_date_3year, end_date
           , start_date_15year, end_date
           , start_date_3month, end_date
           )
    logger.info(sql)
    c.execute(sql)
    symbols = c.fetchall()
    conn.close()
    return symbols

def direct_open_order(dbfile):
    conf = common.read_conf()
    s = my_logger.Logger()
    logger = s.myLogger(conf['logger'])
    logger.info('direct_open_order.')
    max_regist_date = get_last_backtestdate(dbfile)
    today = datetime.strptime(max_regist_date, "%Y-%m-%d")
    start_date = (today - relativedelta(months=3)).strftime("%Y-%m-%d")
    end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    symbols = _get_symbols(dbfile, max_regist_date, today, end_date)
    #ポジション無し
    for s in symbols:
        symbol = s[0]
        strategy = s[1]
        t = tick.get_tick(symbol)
        if strategy == '新値1日_移動平均4日_出来高移動平均20日':
            q = quotes.Quotes(dbfile, symbol, start_date, end_date, 4, 2, 3, 20, 1)
            butler = new_value_and_moving_average.Butler(t, 1)
        elif strategy == '超短期ボリンジャー5日_1.20倍_決済差額0.00':
            q = quotes.Quotes(dbfile, symbol, start_date, end_date, 5, 1.2, 3, 20, 1)
            butler = bollingerband.Butler(t, 1, 0.0001, True)
        elif strategy == '超短期ボリンジャー3日_1.00倍_決済差額0.00':
            q = quotes.Quotes(dbfile, symbol, start_date, end_date, 3, 1.0, 3, 20, 1)
            butler = bollingerband.Butler(t, 1, 0.0001, True)
        else:
            continue
        p = Position(1000000, 0.1, 1)
        for idx, high in enumerate(q.quotes['high']):
            if idx < q.ma_duration:
                continue
            current_position = p.get_position()
            low = q.quotes['low'][idx]
            open_price = q.quotes['open'][idx]
            business_date = q.quotes['business_date'][idx]
            if (numpy.isnan(open_price) 
                or numpy.isnan(low) 
                or numpy.isnan(high)):
                logger.warning('[%s][%d] ohlc is nan' % (symbol, idx))
                continue

            # 開場 
            # 注文を呼び出す
            if p.order != None:
                p.call_order(business_date)
            # 注文がある場合、約定判定
            if current_position == PositionType.NOTHING and p.order != None:
                if p.order.order_type == OrderType.STOP_MARKET_LONG:
                    #約定判定
                    if p.order.price == -1:
                        logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    elif high >= p.order.price and open_price >= p.order.price: #寄り付きが高値の場合
                        if open_price * p.order.vol < p.cash: #現金以上に購入しない
                            p.open_long(business_date, open_price)
                        else:
                            p.order.fail_order()
                    elif high >= p.order.price:
                        p.open_long(business_date, p.order.price)
                    else:
                        p.order.fail_order()
                elif p.order.order_type == OrderType.STOP_MARKET_SHORT:
                    #約定判定
                    if p.order.price == -1:
                        logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                        p.order.fail_order()
                    elif low <= p.order.price and open_price <= p.order.price: #寄り付きが安値の場合
                        if open_price * p.order.vol < p.cash: #現金以上に空売りしない
                            p.open_short(business_date, open_price)
                        else:
                            p.order.fail_order()
                    elif low <= p.order.price:
                        p.open_short(business_date, p.order.price)
                    else:
                        p.order.fail_order()
            elif current_position == PositionType.LONG and p.order != None:
                #約定判定
                if p.order.order_type == OrderType.CLOSE_STOP_MARKET_LONG: #逆指値成行買い返済
                    if low <= p.order.price and open_price <= p.order.price:
                        p.close_long(business_date, open_price)
                    elif low <= p.order.price:
                        p.close_long(business_date, p.order.price)
                    else:
                        p.order.fail_order()
                elif p.order.order_type == OrderType.CLOSE_MARKET_LONG: #成行買い返済
                    p.close_long(business_date, open_price)
            elif current_position == PositionType.SHORT and p.order != None:
                #約定判定
                if p.order.order_type == OrderType.CLOSE_STOP_MARKET_SHORT: #逆指値成行売り返済
                    if high >= p.order.price and open_price >= p.order.price:
                        p.close_short(business_date, open_price)
                    elif high >= p.order.price:
                        p.close_short(business_date, p.order.price)
                    else:
                        p.order.fail_order()
                elif p.order.order_type == OrderType.CLOSE_MARKET_SHORT: #成行売り返済
                    p.close_short(business_date, open_price)
            #注文は1日だけ有効
            p.clear_order()
            # 引け後、翌日の注文作成
            business_date = q.quotes['business_date'][idx]
            max_business_date = max(q.quotes['business_date'])
            current_position = p.get_position()
            if current_position == PositionType.NOTHING:
                long_order_type = butler.check_open_long(q, idx)
                short_order_type = butler.check_open_short(q, idx)
                if long_order_type == OrderType.STOP_MARKET_LONG:
                    #create stop market long
                    t = butler.create_order_stop_market_long_for_all_cash(p.cash, q, idx)
                    p.create_order_stop_market_long(business_date, t[0], t[1])
                    if business_date == max_business_date:
                        price = butler.create_order_stop_market_long(q, idx)
                        logger.info("[%s]に逆指値でlong(最終営業日%s) 逆指値:[%f] (%s)" % (symbol, business_date, price, strategy))
                elif short_order_type == OrderType.STOP_MARKET_SHORT:
                    #create stop market short
                    t = butler.create_order_stop_market_short_for_all_cash(p.cash, q, idx)
                    p.create_order_stop_market_short(business_date, t[0], t[1])
                    if business_date == max_business_date:
                        price = butler.create_order_stop_market_short(q, idx)
                        logger.info("[%s]に逆指値でshort(最終営業日%s) 逆指値:[%f] (%s)" % (symbol, business_date, price, strategy))
                elif long_order_type == OrderType.NONE_ORDER and short_order_type == OrderType.NONE_ORDER:
                    pass
                else:
                    logger.info("[%s]不明なOrderType(最終営業日%s) (%s)" % (symbol, business_date, strategy))
            elif current_position == PositionType.LONG:
                close_order_type = butler.check_close_long(p.pos_price, q, idx)
                if close_order_type == OrderType.CLOSE_STOP_MARKET_LONG: #逆指値成行買い返済
                    price = butler.create_order_close_stop_market_long(q, idx)
                    p.create_order_close_stop_market_long(business_date, price, p.pos_vol)
                elif close_order_type == OrderType.CLOSE_MARKET_LONG: #成行買い返済
                    price = butler.create_order_stop_market_long(q, idx)
                    p.create_order_close_market_long(business_date, price, p.pos_vol)
                else:
                    pass #注文なし
            elif current_position == PositionType.SHORT:
                close_order_type = butler.check_close_short(p.pos_price, q, idx)
                if close_order_type == OrderType.CLOSE_STOP_MARKET_SHORT:
                    price = butler.create_order_close_stop_market_short(q, idx)
                    p.create_order_close_stop_market_short(business_date, price, p.pos_vol)
                elif close_order_type == OrderType.CLOSE_MARKET_SHORT:
                    price = butler.create_order_close_market_short(q, idx)
                    p.create_order_close_market_short(business_date, price, p.pos_vol)

def _check_close_order(butler, q, position, position_price, symbol, strategy):
    for idx, close_price in enumerate(q.quotes['close']):
        business_date = q.quotes['business_date'][idx]
        if business_date == max(q.quotes['business_date']):
            if position == 'long':
                close_order_type = butler.check_close_long(position_price, q, idx)
                if close_order_type == OrderType.CLOSE_STOP_MARKET_LONG:
                    close_long_price = butler.create_order_close_stop_market_long(q, idx)
                    logger.info("[%s][%s] 逆指値[%f]でclose_long position:[%f]" % (symbol, strategy, close_long_price, position_price))
                elif close_order_type == OrderType.CLOSE_MARKET_LONG:
                    logger.info("[%s][%s] 成行でclose_long position:[%f]" % (symbol, strategy, position_price))
                elif close_order_type == OrderType.NONE_ORDER:
                    logger.info("[%s][%s] longはまだcloseの注文をしません position:[%f] close:[%f]" % (symbol, strategy, position_price, close_price))
                else:
                    logger.warning("[%s][%s] 不明なOrderType position:[%f] close:[%f]" % (symbol, strategy, position_price, close_price))
            if position == 'short':
                close_order_type = butler.check_close_short(position_price, q, idx)
                if close_order_type == OrderType.CLOSE_STOP_MARKET_SHORT:
                    close_short_price = butler.create_order_close_stop_market_short(q, idx)
                    logger.info("[%s][%s] 逆指値[%f]でclose_short position:[%f]" % (symbol, strategy, close_short_price, position_price))
                elif close_order_type == OrderType.CLOSE_MARKET_SHORT:
                    logger.info("[%s][%s] 成行でclose_short position:[%f]" % (symbol, strategy, position_price))
                elif close_order_type == OrderType.NONE_ORDER:
                    logger.info("[%s][%s] shortはまだcloseの注文をしません position:[%f] close:[%f]" % (symbol, strategy, position_price, close_price))
                else:
                    logger.warning("[%s][%s] 不明なOrderType position:[%f] close:[%f]" % (symbol, strategy, position_price, close_price))

def direct_close_order(dbfile, symbol, position, position_price):
    conf = common.read_conf()
    s = my_logger.Logger()
    logger = s.myLogger(conf['logger'])
    logger.info('direct_close_order.')
    max_regist_date = _get_last_backtestdate(dbfile)
    today = datetime.strptime(max_regist_date, "%Y-%m-%d")
    start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    t = tick.get_tick(symbol)
    #ポジションあり
    #'新値1日_移動平均4日_出来高移動平均20日':
    strategy = '新値1日_移動平均4日_出来高移動平均20日'
    q = quotes.Quotes(dbfile, symbol, start_date, end_date, 4, 2, 3, 20, 1)
    butler = new_value_and_moving_average.Butler(t, 1)
    _check_close_order(butler, q, position, position_price, symbol, strategy)
    #'超短期ボリンジャー5日_1.20倍_決済差額0.00':
    strategy = '超短期ボリンジャー5日_1.20倍_決済差額0.00'
    q = quotes.Quotes(dbfile, symbol, start_date, end_date, 5, 1.2, 3)
    butler = bollingerband.Butler(t, 1, 0.0001, True)
    _check_close_order(butler, q, position, position_price, symbol, strategy)
    #'超短期ボリンジャー3日_1.00倍_決済差額0.00':
    strategy = '超短期ボリンジャー3日_1.00倍_決済差額0.00'
    q = quotes.Quotes(dbfile, symbol, start_date, end_date, 3, 1.0, 3)
    butler = bollingerband.Butler(t, 1, 0.0001, True)
    _check_close_order(butler, q, position, position_price, symbol, strategy)

