
import sqlite3
import pandas as pd
import my_lock

class Quotes():
    def __init__(self, dbfile, symbol, start_date, end_date, ma_duration=15, ev_sigma_ratio=2, vol_ma_duration=15, vol_ev_sigma_ratio=1):
        self.dbfile = dbfile
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.ma_duration = ma_duration
        self.ev_sigma_ratio = ev_sigma_ratio 
        self.vol_ma_duration = vol_ma_duration
        self.vol_ev_sigma_ratio = vol_ev_sigma_ratio
        self.get_history()
        self.set_sigma()

    def is_str(self, v):
        return isinstance(v, str)

    def get_history(self):
        try:
            my_lock.lock.acquire()
            conn = sqlite3.connect(self.dbfile, isolation_level='EXCLUSIVE')
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
        except Exception as err:
            print(err)
        finally:
            if conn: 
                self.quotes = df
                conn.close
            else:
                self.quotes = None
            my_lock.lock.release()

    def set_sigma(self):
        #終値の配列から移動平均、標準偏差の配列を算出
        s = pd.Series(self.quotes['close'])
        self.sma = s.rolling(window=self.ma_duration).mean()
        self.sigma = s.rolling(window=self.ma_duration).std(ddof=0)
        #self.upper2_sigma = self.sma + self.sigma * 2
        #self.lower2_sigma = self.sma - self.sigma * 2
        #self.upper3_sigma = self.sma + self.sigma * 3
        #self.lower3_sigma = self.sma - self.sigma * 3
        self.upper_ev_sigma = self.sma + self.sigma * self.ev_sigma_ratio
        self.lower_ev_sigma = self.sma - self.sigma * self.ev_sigma_ratio
        #出来高の移動平均を算出
        v = pd.Series(self.quotes['volume'])
        self.vol_ma = v.rolling(window=self.vol_ma_duration).mean()
        self.vol_sigma = v.rolling(window=self.vol_ma_duration).std(ddof=0)
        self.vol_upper_ev_sigma = self.vol_ma + self.vol_sigma * self.vol_ev_sigma_ratio
        self.vol_lower_ev_sigma = self.vol_ma - self.vol_sigma * self.vol_ev_sigma_ratio

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
