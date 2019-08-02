
from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
yf.pdr_override()

symbols = open("symbol/symbol.txt", "r")
for symbol in symbols:
    df = pdr.get_data_yahoo(symbol, start="2017-01-01", end="2019-08-02")
    s = pd.Series(df['Close'])
    duration = 2
    deviation = 2
    sma = s.rolling(window=duration).mean()
    sigma = s.rolling(window=duration).std(ddof=0)
    upper2_sigma = sma + sigma*deviation
    lower2_sigma = sma - sigma*deviation
    idx = df.index.size-1
    long_flg = df['High'][idx] > upper2_sigma[idx]
    short_flg = lower2_sigma[idx] > df['Low'][idx]
    if (long_flg and short_flg) or (long_flg == False and short_flg == False):
        continue
    if long_flg:
        print(df.index[idx])
        print("%s %f > %f long ute" % (symbol, df['High'][idx]+1.0, upper2_sigma[idx]))
    elif short_flg:
        print(df.index[idx])
        print("%s %f > %f short ute" % (symbol, lower2_sigma[idx], df['Low'][idx]-1.0))

