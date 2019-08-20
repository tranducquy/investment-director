
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

def get_max_businessdate(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    #ohlcの最終登録日を取得
    c.execute("""
    select
    max(business_date)
    from ohlc""")
    max_date = c.fetchone()
    conn.close()
    return max_date[0]

def get_strategy_name(db, strategy_id):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""
    select
    name
    from m_strategy
    where id = {sid}
    """.format(sid=strategy_id))
    name = c.fetchone()
    conn.close()
    return name[0]

def _get_symbols(db, today, start_date, end_date):
    #3ヶ月、1,3,15年のバックテストで利益の出ている銘柄のみ探す
    start_date_3month = (today - relativedelta(months=3)).strftime("%Y-%m-%d")
    start_date_1year = (today - relativedelta(years=1)).strftime("%Y-%m-%d")
    start_date_3year = (today - relativedelta(years=3)).strftime("%Y-%m-%d")
    start_date_15year = (today - relativedelta(years=15)).strftime("%Y-%m-%d")

    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql = """
    select
     r.symbol
    ,r.strategy
    ,order_table.order_type
    ,order_table.order_price
    ,r.end_date
    ,m3.profit_rate_sum as 期待利益率3か月
    ,y1.profit_rate_sum as 期待利益率1年
    ,y3.profit_rate_sum as 期待利益率3年
    ,y15.profit_rate_sum as 期待利益率15年
    ,r.average_period_per_trade as 平均取引期間
    ,r.win_rate as 勝率
    ,r.long_expected_rate as 期待利益率long
    ,r.long_win_count+r.long_loss_count as 取引数long
    ,r.short_expected_rate as 期待利益率short
    ,r.short_win_count+r.short_loss_count as 取引数short
    ,r.win_count+r.loss_count as 取引数
   from backtest_result r
   left outer join (
   select
     symbol
    ,strategy_id
    ,sum(profit_rate) as profit_rate_sum
    ,count(business_date) as count
   from backtest_history
   where business_date between '%s' and '%s'
   group by symbol, strategy_id
   HAVING count(business_date) > 45
   ) m3
   on r.symbol = m3.symbol and r.strategy_id = m3.strategy_id
   left outer join (
   select
     symbol
    ,strategy_id
    ,sum(profit_rate) as profit_rate_sum
   from backtest_history
   where business_date between '%s' and '%s'
   group by symbol, strategy_id
   HAVING count(business_date) > 183
   ) y1
   on r.symbol = y1.symbol and r.strategy_id = y1.strategy_id
   left outer join (
   select
     symbol
    ,strategy_id
    ,sum(profit_rate) as profit_rate_sum
   from backtest_history
   where business_date between '%s' and '%s'
   group by symbol, strategy_id
   HAVING count(business_date) > 548
   ) y3
   on r.symbol = y3.symbol and r.strategy_id = y3.strategy_id
   left outer join (
   select
     symbol
    ,strategy_id
    ,sum(profit_rate) as profit_rate_sum
   from backtest_history
   where business_date between '%s' and '%s'
   group by symbol, strategy_id
   HAVING count(business_date) > 2738
   ) y15
   on r.symbol = y15.symbol and r.strategy_id = y15.strategy_id
   inner join (
        select
         symbol
        ,order_create_date
        ,order_type
        ,order_vol
        ,order_price
        from backtest_history
        where business_date = (select max(business_date) from backtest_history)
        and order_type in (1, 2)
        and order_price > 0
        and order_vol > 0
   ) as order_table
   on r.symbol = order_table.symbol
   where r.start_date = '%s'
   and r.end_date = '%s'
   and r.rate_of_return > 0
   and (m3.profit_rate_sum > 3 and y1.profit_rate_sum > 15 and y3.profit_rate_sum > 45 and y15.profit_rate_sum > 225)
   order by m3.profit_rate_sum desc
       """ % (
             start_date_3month, end_date
           , start_date_1year, end_date
           , start_date_3year, end_date
           , start_date_15year, end_date
           , start_date, end_date
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
    max_businessdate = get_max_businessdate(dbfile)
    today = (datetime.strptime(max_businessdate, "%Y-%m-%d") + timedelta(days=1)) 
    start_date = conf['backtest_startdate']
    end_date = max_businessdate
    symbols = _get_symbols(dbfile, today, start_date, end_date)
    for s in symbols:
        order_type = OrderType(s[2])
        msg = "[{symbol}][{strategy}] [注文方法:{ordertype}][価格:{order_price}]".format(symbol=s[0], strategy=s[1], ordertype=order_type.name, order_price = s[3])
        logger.info(msg)

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
    max_businessdate = get_max_businessdate(dbfile)
    today = (datetime.strptime(max_businessdate, "%Y-%m-%d") + timedelta(days=1)) 
    start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    t = tick.get_tick(symbol)
    #ポジションあり
    #ボリンジャー3日_1.00倍
    strategy_id = 1
    q = quotes.Quotes(dbfile, symbol, start_date, end_date, 3, 1.0, 3)
    butler = bollingerband.Butler(t, 1, 0.0001, True)
    strategy = get_strategy_name(dbfile, strategy_id)
    _check_close_order(butler, q, position, position_price, symbol, strategy)

