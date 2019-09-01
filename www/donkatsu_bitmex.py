# -*- coding: utf-8 -*-

import sys
import datetime
import calendar, requests
import pandas as pd

def _get_history(symbol, seconds, period):
    now = datetime.datetime.utcnow()
    unixtime = calendar.timegm(now.utctimetuple())
    since = unixtime - seconds
    param = {"symbol": symbol, "period": 1, "from": since, "to": unixtime}
    url = "https://www.bitmex.com/api/udf/history?symbol={symbol}&resolution={period}&from={from}&to={to}".format(**param)
    res = requests.get(url)
    data = res.json()
    business_dates = list()
    for t in data["t"]:
        business_dates.append(datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%s'))
    #DataFrame生成
    df = pd.DataFrame({
            "BusinessDate": business_dates,
            "Open":      data["o"],
            "High":      data["h"],
            "Low":       data["l"],
            "Close":     data["c"],
            "Volume":    data["v"],
        }, columns = ["BusinessDate","Open","High","Low","Close","Volume"])
    return df

def set_sigma(quotes, ma_period, sigma1, sigma2, sigma3):
    s = pd.Series(quotes[5])
    sma = s.rolling(window=ma_period).mean()
    sigma = s.rolling(window=ma_period).std(ddof=0)
    upper_sigma1 = sma + sigma * sigma1
    lower_sigma1 = sma - sigma * sigma1
    upper_sigma2 = sma + sigma * sigma2
    lower_sigma2 = sma - sigma * sigma2
    upper_sigma3 = sma + sigma * sigma3
    lower_sigma3 = sma - sigma * sigma3
    return (upper_sigma1, lower_sigma1, upper_sigma2, lower_sigma2, upper_sigma3, lower_sigma3)

def download_bitmex_1punashi(symbol):
    seconds = 60 * 60 # 1時間
    period = 1 #1分足
    data = _get_history(symbol, seconds, period) 
    idx = len(data['BusinessDate'])
    quotes = list()
    for i in range(idx):
        business_date = data['BusinessDate'][i]
        volume = int((data['Volume'][i]).astype('int64'))
        open_price = data['Open'][i]
        high_price = data['High'][i]
        low_price = data['Low'][i]
        close_price = data['Close'][i]
        quotes.append( (symbol, business_date, open_price, high_price, low_price, close_price, volume) )
    return quotes
