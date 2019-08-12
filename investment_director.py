
import sys
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import common
import my_logger
import quotes
from butler import bollingerband
from butler import bollingerband_and_volume_bollingerband
from butler import bollingerband_and_volume_moving_average
from butler import new_value_and_moving_average_and_volume_moving_average
import tick

s = my_logger.Logger()
logger = s.myLogger()

if __name__ == '__main__':
    args = sys.argv
    conf = common.read_conf()
    s = my_logger.Logger()
    logger = s.myLogger(conf['logger'])
    logger.info('investment-director.')
    #symbol_txt = conf['symbol']
    dbfile = conf['dbfile']
    #symbols = open(symbol_txt, "r")
    #3ヶ月、1,3,15年のバックテストで利益の出ている銘柄のみ探す
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    today = datetime.today()
    start_date_3month = (today - relativedelta(months=3)).strftime("%Y-%m-%d")
    start_date_1year = (today - relativedelta(years=1)).strftime("%Y-%m-%d")
    start_date_3year = (today - relativedelta(years=3)).strftime("%Y-%m-%d")
    start_date_15year = (today - relativedelta(years=15)).strftime("%Y-%m-%d")
    start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    c.execute("""
    select
     symbol
    ,strategy
    ,regist_date
    ,rate_of_return
    ,expected_rate
    ,expected_rate_per_1day
    ,average_period_per_trade
    ,win_rate
    from backtest_result
    where 
    (symbol||strategy) in (
        select 
         symbol||strategy
        from backtest_result
        where (symbol||strategy) in (
            select
             symbol||strategy
            from backtest_result
            where (symbol||strategy) in (
                select
                 symbol||strategy
                from backtest_result
                where start_date = ?
                and end_date = ?
                and backtest_period > 20*3
                and rate_of_return > 0
            )
            and start_date = ?
            and end_date = ?
            and backtest_period > 300*1
            and rate_of_return > 0
        )
        and start_date = ?
        and end_date = ?
        and backtest_period > 300*3
        and rate_of_return > 0
    ) 
    and start_date = ?
    and end_date = ?
    and backtest_period > 300*15
    and rate_of_return > 0
    and regist_date = '2019-08-12'
    order by rate_of_return desc
    """, (start_date_3month, end_date
        , start_date_1year, end_date
        , start_date_3year, end_date
        , start_date_15year, end_date))
    symbols = c.fetchall()
    conn.close()

    #ポジション無し
    for s in symbols:
        symbol = s[0]
        strategy = s[1]
        regist_date = s[2]
        t = tick.get_tick(symbol)
        if strategy == '新値1日_移動平均4日_出来高移動平均20日':
            q = quotes.Quotes(dbfile, symbol, start_date, end_date, 4, 1, 20, 1)
            butler = new_value_and_moving_average_and_volume_moving_average.Butler(t, 1)
        elif strategy == '超短期ボリンジャー5日_1.20倍_決済差額0.00':
            q = quotes.Quotes(dbfile, symbol, start_date, end_date, 5, 1.2)
            butler = bollingerband.Butler(t, 1, 0.0001)
        elif strategy == '超短期ボリンジャー3日_1.00倍_0.00_出来高ボリンジャー14日_2.00倍':
            q = quotes.Quotes(dbfile, symbol, start_date, end_date, 3, 1.0, 14, 2.0)
            butler = bollingerband_and_volume_bollingerband.Butler(t, 1, 0.0001)
        else:
            continue
        for idx, high in enumerate(q.quotes['high']):
            business_date = q.quotes['business_date'][idx]
            if business_date == max(q.quotes['business_date']):
                if butler.check_open_long(q, idx):
                    price = butler.create_order_stop_market_long(q, idx)
                    logger.info("[%s]に逆指値でlongうて(最終営業日%s) 逆指値:[%f] (%s)" % (symbol, business_date, price, strategy))
                elif butler.check_open_short(q, idx):
                    price = butler.create_order_stop_market_short(q, idx)
                    logger.info("[%s]に逆指値でshortうて(最終営業日%s) 逆指値:[%f] (%s)" % (symbol, business_date, price, strategy))
    
    #TODO:ポジション有り
