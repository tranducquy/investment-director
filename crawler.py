# -*- coding: utf-8 -*-

import sys
import datetime
import sqlite3
import yfinance as yf
import common
import my_logger
import backtest
from www import symbol as sym

s = my_logger.Logger()
logger = s.myLogger()

def insert_history(dbfile, quotes):
    try:
        conn = sqlite3.connect(dbfile, isolation_level='EXCLUSIVE')
        c = conn.cursor()
        c.executemany('INSERT OR REPLACE INTO ohlc(symbol, business_date, open, high, low, close, volume) VALUES(?,?,?,?,?,?,?)', quotes)
    except Exception as err:
        logger.error('error dayo. {0}'.format(err))
        if conn: conn.rollback()
    finally:
        if conn: 
            conn.commit()
            conn.close

if __name__ == '__main__':
    args = sys.argv
    conf = common.read_conf()
    s = my_logger.Logger()
    logger = s.myLogger(conf['logger'])
    logger.info('crawler.')
    dbfile = conf['dbfile']
    args = backtest.get_option()
    if args.start_date is None:
        default_period = abs(int(conf['default_period']))
        start_date = (datetime.datetime.now() + datetime.timedelta(days=-default_period)).strftime('%Y-%m-%d')
    else:
        start_date = args.start_date
    if args.end_date is None:
        end_date = (datetime.datetime.now()).strftime('%Y-%m-%d')
    else:
        end_date = args.end_date
    if args.symbol is None:
        symbol_txt = conf['symbol']
    else:
        symbol_txt = args.symbol
    symbols = sym.get_symbols(symbol_txt)
    for symbol in symbols:
        data = yf.download(symbol, start=start_date, end=end_date)
        idx = data.index.size
        max_date = ''
        min_date = ''
        quotes = list()
        for i in range(idx):
            business_date = (data.index[i]).strftime("%Y-%m-%d")
            open_price = data['Open'][i]
            high_price = data['High'][i]
            low_price = data['Low'][i]
            close_price = data['Close'][i]
            volume = int((data['Volume'][i]).astype('int64'))
            quotes.append( (symbol, business_date, open_price, high_price, low_price, close_price, volume) )
            if max_date == '':
                max_date = business_date
            elif business_date > max_date:
                max_date = business_date
            if min_date == '':
                min_date = business_date
            elif business_date < min_date:
                min_date = business_date
        insert_history(dbfile, quotes)
        logger.info("downloaded:[%s][%s-%s] [%s-%s]" % (symbol, start_date, end_date, min_date, max_date))

