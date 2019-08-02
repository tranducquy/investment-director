
import sys
import datetime
import sqlite3
import yfinance as yf
import common
import my_logger

s = my_logger.Logger()
logger = s.myLogger()

def insert_history(business_date, symbol, open_price, high_price, low_price, close_price, volume):
    dbfile = conf['dbfile']
    try:
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()
        param = ( business_date, symbol, open_price, high_price, low_price, close_price, volume )
        c.execute('INSERT OR REPLACE INTO ohlc(symbol, business_date, open, high, low, close, volume) VALUES(?,?,?,?,?,?,?)', param)
        conn.commit()
        conn.close
    except Exception as err:
        logger.error('error dayo. {0}'.format(err))

if __name__ == '__main__':
    args = sys.argv
    conf = common.read_conf()
    s = my_logger.Logger()
    logger = s.myLogger(conf['logger'])
    logger.info('crawler.')
    start_date = conf['start_date']
    end_date = conf['end_date']
    #実行時引数が3つの場合は開始日、終了日を上書き
    if len(args) == 3:
        start_date = args[1]
        end_date = args[2]
    #実行時引数が2つで特定の文字であれば、30日前から昨日まで
    elif len(args) == 2 and args[1] == "-30days":
        start_date = (datetime.datetime.now() + datetime.timedelta(days=-30)).strftime('%Y-%m-%d') #30日前
        end_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d') #昨日
    symbols = open("symbol/symbol.txt", "r")
    for symbol in symbols:
        symbol = symbol.strip()
        data = yf.download(symbol, start=start_date, end=end_date)
        idx = data.index.size-1
        for i in range(idx):
            insert_history(data.index[i].strftime("%Y-%m-%d"), symbol, data['Open'][i], data['High'][i], data['Low'][i], data['Close'][i], data['Volume'][i])
        logger.info("downloaded:[%s][%s-%s]" % (symbol, start_date, end_date))

