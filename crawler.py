
import sys
import datetime
import sqlite3
import yfinance as yf
import common
import my_logger

s = my_logger.Logger()
logger = s.myLogger()

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
    #実行時引数が3つの場合は開始日、終了日を上書き
    if len(args) == 3:
        start_date = args[1]
        end_date = args[2]
    #実行時引数が0であれば、設定ファイルから対象期間を取得
    elif len(args) == 1:
        default_period = int(conf['default_period'])
        start_date = (datetime.datetime.now() + datetime.timedelta(days=default_period)).strftime('%Y-%m-%d')
        end_date = (datetime.datetime.now()).strftime('%Y-%m-%d')
    else:
        sys.exit()
    symbol_txt = conf['symbol']
    symbols = open(symbol_txt, "r")
    for symbol in symbols:
        symbol = symbol.strip()
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
        insert_history(quotes)
        logger.info("downloaded:[%s][%s-%s] [%s-%s]" % (symbol, start_date, end_date, min_date, max_date))

