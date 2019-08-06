
import sys
import sqlite3
import pandas as pd
import common
import my_logger

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
    conn = sqlite3.connect(dbfile)
    symbols = open(symbol_txt, "r")
    for symbol in symbols:
        symbol = symbol.strip()
        df = pd.read_sql_query("select business_date, open, high, low, close, volume from ohlc where symbol = '%s'" % (symbol), conn)
        s = pd.Series(df['close'])
        duration = 2
        deviation = 2
        sma = s.rolling(window=duration).mean()
        sigma = s.rolling(window=duration).std(ddof=0)
        upper2_sigma = sma + sigma*deviation
        lower2_sigma = sma - sigma*deviation
        idx = df.index.size-1
        long_flg = df['high'][idx] > upper2_sigma[idx]
        short_flg = lower2_sigma[idx] > df['low'][idx]
        if (long_flg and short_flg) or (long_flg == False and short_flg == False):
            continue
        if long_flg:
            logger.debug("%s %f > %f long ute" % (symbol, df['high'][idx]+1.0, upper2_sigma[idx]))
        elif short_flg:
            logger.debug("%s %f > %f short ute" % (symbol, lower2_sigma[idx], df['low'][idx]-1.0))
    conn.close()
    
