
import sys
import sqlite3
import pandas as pd
from datetime import datetime
import common
import my_logger
import quotes
from butler import bollingerband_and_volume_bollingerband
from butler import bollingerband_and_volume_moving_average
from butler import new_value_and_moving_average_and_volume_moving_average

s = my_logger.Logger()
logger = s.myLogger()

if __name__ == '__main__':
    args = sys.argv
    conf = common.read_conf()
    s = my_logger.Logger()
    logger = s.myLogger(conf['logger'])
    logger.info('investment-director.')
    symbol_txt = conf['symbol']
    dbfile = conf['dbfile']
    tick = 1
    today = datetime.today()
    start_date = today - datetime.timedelta(days=30)
    end_date = datetime.strftime(today, '%Y-%m-%d')
    symbols = open(symbol_txt, "r")
    #TODO:3か月,1,3,15年のバックテストで利益の出ている銘柄のみ探す
    """
    select
    symbol
    from backtest_result
    where symbol in (
        select 
        symbol
        from backtest_result
        where symbol in (
            select
            symbol
            from backtest_result
            where start_date = '2018-08-10'
            and end_date = '2019-08-09'
            and trading_period > 300*1
            and rate_of_return > 0
        )
        and start_date = '2016-08-10'
        and end_date = '2019-08-09'
        and trading_period > 300*3
        and rate_of_return > 0
    )
    and start_date = '2004-08-10'
    and end_date = '2019-08-09'
    and trading_period > 300*15
    and rate_of_return > 0
    """

    #ポジション無し
    for symbol in symbols:
        symbol = symbol.strip()
        q = quotes.Quotes(dbfile, symbol, start_date, end_date, 4, 1, 20, 1)
        butler = new_value_and_moving_average_and_volume_moving_average.Butler(1)
        for idx, high in enumerate(q.quotes['high']):
            if q.quotes['business_date'][idx] == end_date:
                if butler.check_open_long(q, idx):
                    price = butler.get_price_stop_market_long(high, tick)
                    logger.info("long ute:[%s] price:[%f]" % (symbol, price))
                elif butler.check_open_short(q, idx):
                    price = butler.get_price_stop_market_short(high, tick)
                    logger.info("short ute:[%s] price:[%f]" % (symbol, price))
    
    #TODO:ポジション有り
