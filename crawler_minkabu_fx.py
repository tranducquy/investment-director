
import sys
import sqlite3
import requests
import datetime
import common
import my_logger

s = my_logger.Logger()
logger = s.myLogger()

def minkabu_fx_download(symbol, leg='daily', count=30):
    uri = "https://fx.minkabu.jp/api/v2/bar/%s/%s.json?count=%d" % (symbol, leg, count)
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
    return data

def insert_history(quotes):
    dbfile = conf['dbfile']
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
    logger.info('minkabu crawler.')
    #設定ファイルから対象期間を取得
    if len(args) == 1:
        default_period = int(conf['default_period'])
    else:
        sys.exit()
    symbol_txt = conf['symbol']
    symbols = open(symbol_txt, "r")
    for symbol in symbols:
        symbol = symbol.strip()
        data = minkabu_fx_download(symbol, count=default_period)
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
            volume = 0
            quotes.append( (symbol, business_date, open_price, high_price, low_price, close_price, volume) )
            if max_date == '':
                max_date = business_date
            elif business_date > max_date:
                max_date = business_date
            if min_date == '':
                min_date = business_date
            elif business_date < min_date:
                min_date = business_date
        insert_history(quotes)
        logger.info("downloaded:[%s][%s-%s]" % (symbol, min_date, max_date))

