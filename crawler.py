# -*- coding: utf-8 -*-

import sys
import datetime
import sqlite3
import calendar, requests
import pandas as pd
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

def minkabu_fx_download(symbol, leg='daily', count=30):
    uri = "https://fx.minkabu.jp/api/v2/bar/%s/%s.json?count=%d" % (symbol, leg, count)
    logger.info(uri)
    res = requests.get(uri).json()
    data = dict()
    data['BusinessDate'] = list()
    data['Open'] = list()
    data['High'] = list()
    data['Low'] = list()
    data['Close'] = list()
    for r in res:
        business_date = datetime.datetime.fromtimestamp(r[0]/1000).strftime('%Y-%m-%d')
        data['BusinessDate'].append(business_date)
        data['Open'].append(r[1])
        data['High'].append(r[2])
        data['Low'].append(r[3])
        data['Close'].append(r[4])
        data['Volume'].append(0)
    return data

def bitmex_download(symbol, seconds):
    now = datetime.datetime.utcnow()
    unixtime = calendar.timegm(now.utctimetuple())
    since = unixtime - seconds
    param = {"symbol": symbol, "period": 1440, "from": since, "to": unixtime}
    url = "https://www.bitmex.com/api/udf/history?symbol={symbol}&resolution={period}&from={from}&to={to}".format(**param)
    res = requests.get(url)
    data = res.json()
    business_dates = list()
    for t in data["t"]:
        business_dates.append(datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d'))
    #DataFrame生成
    df = pd.DataFrame({
            "BusinessDate": business_dates,
            "Open":      data["o"],
            "High":      data["h"],
            "Low":       data["l"],
            "Close":     data["c"],
            "Volume":    data["v"],
        }, columns = ["BusinessDate","Open","High","Low","Close","Volume"])
    return df

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
    if args.period is None:
        unix_period = int(conf['default_unix_period'])
    else:
        unix_period = int(args.period)

    if 'bitmex' in symbol_txt:
        bitmex = True
    else:
        bitmex = False
    if 'minkabu' in symbol_txt:
        minkabu = True
    else:
        minkabu = False

    symbols = sym.get_symbols(symbol_txt)
    for symbol in symbols:
        if minkabu:
            data = minkabu_fx_download(symbol, count=unix_period)
            idx = len(data['BusinessDate'])
        elif bitmex:
            data = bitmex_download(symbol, 60 * 60 * 24 * abs(unix_period))
            idx = len(data['BusinessDate'])
        else:
            data = yf.download(symbol, start=start_date, end=end_date)
            idx = data.index.size
        max_date = ''
        min_date = ''
        quotes = list()
        for i in range(idx):
            if minkabu or bitmex:
                business_date = data['BusinessDate'][i]
            else:
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
        if minkabu or bitmex:
            logger.info("downloaded:[%s][%s-%s]" % (symbol, min_date, max_date))
        else:
            logger.info("downloaded:[%s][%s-%s] [%s-%s]" % (symbol, start_date, end_date, min_date, max_date))

