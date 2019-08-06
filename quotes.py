
import sqlite3
import pandas as pd

class Quotes():
    def __init__(self, dbfile, symbol, start_date, end_date, ma_duration=15):
        self.dbfile = dbfile
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.ma_duration = ma_duration
        self.get_history()
        self.set_sigma()

    def is_str(self, v):
        return isinstance(v, str)

    def get_history(self):
        conn = sqlite3.connect(self.dbfile)
        df = pd.read_sql_query("""select
                                      symbol
                                     , business_date
                                     , open
                                     , high
                                     , low
                                     , close
                                     , volume
                                     from ohlc 
                                     where symbol = '%s'
                                     and business_date between '%s' and '%s'
                                     order by business_date
                                     """ 
                                     % (
                                         self.symbol
                                         ,self.start_date
                                         ,self.end_date
                                        ), conn)
        conn.close()    
        self.quotes = df

    def set_sigma(self):
        #終値の配列から移動平均、標準偏差の配列を算出
        s = pd.Series(self.quotes['close'])
        self.sma = s.rolling(window=self.ma_duration).mean()
        self.sigma = s.rolling(window=self.ma_duration).std(ddof=0)
        self.upper2_sigma = self.sma + self.sigma * 2
        self.lower2_sigma = self.sma - self.sigma * 2
        self.upper3_sigma = self.sma + self.sigma * 3
        self.lower3_sigma = self.sma - self.sigma * 3

    def get_headdate(self):
        if self.quotes.index.size != 0:
            return self.quotes.iloc[0]['business_date']
        else:
            return ""

    def get_taildate(self):
        if self.quotes.index.size != 0:
            return self.quotes.iloc[-1]['business_date']
        else:
            return ""
