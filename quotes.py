
import pandas as pd
import mylock
from mydb import MyDB

class Quotes():
    def __init__(self, symbol, start_date, end_date, ma_duration=15, ev_sigma_ratio=2, ev2_sigma_ratio=3):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.ma_duration = ma_duration
        self.ev_sigma_ratio = ev_sigma_ratio 
        self.ev2_sigma_ratio = ev2_sigma_ratio 
        self.get_history()
        self.set_sigma()

    def is_str(self, v):
        return isinstance(v, str)

    def get_history(self):
        try:
            mylock.lock.acquire()
            conn = MyDB().get_db()
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
            mylock.lock.release()

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
        self.upper_ev2_sigma = self.sma + self.sigma * self.ev2_sigma_ratio
        self.lower_ev2_sigma = self.sma - self.sigma * self.ev2_sigma_ratio

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
