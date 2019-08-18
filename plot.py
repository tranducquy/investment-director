#! /usr/bin/env python
# -*- coding: utf-8 -*-

from quotes import Quotes
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance

def plot(output_filename, db, symbol, start_date, end_date, sma_duration=15, band_width1=2.0, band_width2=3.0):
    q = Quotes(db, symbol, start_date, end_date, sma_duration, band_width1, band_width2, 15, 2)
    df = q.quotes
    df.index = pd.to_datetime(df['business_date'])
    df = df.drop(columns=['symbol', 'business_date'])
    df.index = mdates.date2num(df.index)
    data = df.reset_index().values
    fig = plt.figure(figsize=(24, 8))
    ax = fig.add_subplot(1, 1, 1)
    
    mpl_finance.candlestick_ohlc(ax, data, width=1, alpha=0.5, colorup='r', colordown='b')
    s = pd.Series(df['close'])
    ax.plot(df['close'].rolling(sma_duration).mean()) #終値移動平均
    ax.plot(df['close'].rolling(sma_duration).mean() + s.rolling(window=sma_duration).std(ddof=0) * band_width1, alpha=0.5) #終値上1ボリンジャーバンド
    ax.plot(df['close'].rolling(sma_duration).mean() + s.rolling(window=sma_duration).std(ddof=0) * band_width2, alpha=0.5) #終値上2ボリンジャーバンド
    ax.plot(df['close'].rolling(sma_duration).mean() - s.rolling(window=sma_duration).std(ddof=0) * band_width1, alpha=0.5) #終値上1ボリンジャーバンド
    ax.plot(df['close'].rolling(sma_duration).mean() - s.rolling(window=sma_duration).std(ddof=0) * band_width2, alpha=0.5) #終値上2ボリンジャーバンド
    ax.grid()
    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.savefig(output_filename)

if __name__ == '__main__':
    #test
    plot('candle_stick.png', 'market-history.db', '8848.T', '2019-05-16', '2019-08-15', 3, 1.0, 3.0)

