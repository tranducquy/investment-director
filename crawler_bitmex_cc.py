
import sys
import datetime
import calendar, requests
import sqlite3
#import yfinance as yf
import pandas as pd
import common
import my_logger

s = my_logger.Logger()
logger = s.myLogger()

def bitmex_download(symbol, seconds):
    # 現在時刻のUTC
    now = datetime.datetime.utcnow()
    unixtime = calendar.timegm(now.utctimetuple())
    # 取得開始のUnixTime
    since = unixtime - seconds
    # APIリクエスト(1時間前から現在までの1日足OHLCVデータを取得)
    param = {"symbol": symbol, "period": 1440, "from": since, "to": unixtime}
    url = "https://www.bitmex.com/api/udf/history?symbol={symbol}&resolution={period}&from={from}&to={to}".format(**param)
    res = requests.get(url)
    data = res.json()
    business_dates = list()
    for t in data["t"]:
        business_dates.append(datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d'))
    # レスポンスのjsonデータからOHLCVのDataFrameを作成
    df = pd.DataFrame({
            "BusinessDate": business_dates,
            "Open":      data["o"],
            "High":      data["h"],
            "Low":       data["l"],
            "Close":     data["c"],
            "Volume":    data["v"],
        }, columns = ["BusinessDate","Open","High","Low","Close","Volume"])
    return df

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
    logger.info('crawler.')
    #設定ファイルから対象期間を取得
    if len(args) == 1:
        default_period = int(conf['default_period'])
    else:
        sys.exit()
    symbol_txt = conf['symbol']
    symbols = open(symbol_txt, "r")
    for symbol in symbols:
        symbol = symbol.strip()
        #data = yf.download(symbol, start=start_date, end=end_date)
        data = bitmex_download(symbol, 60 * 60 * 24 * default_period)
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
        insert_history(quotes)
        logger.info("downloaded:[%s][%s-%s]" % (symbol, min_date, max_date))

