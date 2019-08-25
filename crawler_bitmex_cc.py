# -*- coding: utf-8 -*-

import sys
import datetime
import calendar, requests
import sqlite3
#import yfinance as yf
import pandas as pd
import common
import my_logger
import backtest
import crawler
from www import symbol as sym

s = my_logger.Logger()
logger = s.myLogger()

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
    logger.info('bitmex crawler.')
    args = backtest.get_option()
    if args.period is None:
        default_period = int(conf['default_period'])
    else:
        default_period = int(args.period)
    if args.symbol is None:
        symbol_txt = conf['symbol']
    else:
        symbol_txt = args.symbol
    dbfile = conf['dbfile']
    symbols = sym.get_symbols(symbol_txt)
    for symbol in symbols:
        #data = yf.download(symbol, start=start_date, end=end_date)
        data = bitmex_download(symbol, 60 * 60 * 24 * abs(default_period))
        idx = len(data['BusinessDate'])
        max_date = ''
        min_date = ''
        quotes = list()
        for i in range(idx):
            business_date = data['BusinessDate'][i]
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
        crawler.insert_history(dbfile, quotes)
        logger.info("downloaded:[%s][%s-%s]" % (symbol, min_date, max_date))

