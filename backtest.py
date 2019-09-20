#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from quotes import Quotes
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import threading
import numpy
from argparse import ArgumentParser
import common
import mylogger 
from butler import bollingerband
from www import tick
from www import symbol
from market import Market
from mydb import MyDB
from assets import Assets
from backtest_dumper import BacktestDumper

s = mylogger.Logger()
logger = s.myLogger()

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--symbol', type=str, help='Absolute/relative path to input file')
    argparser.add_argument('--start_date', type=str, help='Date of backtest start')
    argparser.add_argument('--end_date', type=str, help='Date of backtest end')
    argparser.add_argument('--period', type=str, help='for bitmex/minkabu_fx')
    argparser.add_argument('--brute_force', action='store_true', help='breaking the code!')
    args = argparser.parse_args()
    return args

def get_max_businessdate_from_ohlc(symbols):
    conn = MyDB().get_db()
    c = conn.cursor()
    #ohlcの最終登録日を取得
    c.execute("""
    select
    max(business_date)
    from ohlc 
    where symbol in ({0})""".format(', '.join('?' for _ in symbols)), symbols)
    max_date = c.fetchone()
    conn.close()
    return max_date[0]


def backtest_bollingerband(symbol, start_date, end_date, strategy_id, strategy_option, ma, sigma1, sigma2, initial_cash):
    q = Quotes(symbol, start_date, end_date, ma, sigma1, sigma2)
    t = tick.get_tick(symbol)
    bollinger_butler = bollingerband.Butler(t, ma)
    title = "BollingerBand/DailyTrail SMA%dSD%s" % (ma, '{:.1f}'.format(sigma1))
    a = Assets(initial_cash)
    Market().simulator_run(title, strategy_id, strategy_option, q, bollinger_butler, symbol, a, trade_fee) 

def bruteforce_bollingerband_dailytrail(symbol, start_date, end_date, initial_cash):
    #デフォルト設定
    strategy_id = 1
    sigma2_ratio = 3.0 #トレンドを判定するsigma2の倍率
    #単純移動平均2-25
    min_sma_duration = 2
    max_sma_duration = 25
    #標準偏差0.1-2.5
    min_sigma1_duration = 0.1
    max_sigma1_duration = 2.5
    sigma1_band= 0.1
    for bollinger_ma in range(min_sma_duration, max_sma_duration):
        thread_pool = list()
        for sigma1_ratio in numpy.arange(min_sigma1_duration, max_sigma1_duration, sigma1_band):
            strategy_option = "SMA{sma}SD{sd:.1f}".format(sma=bollinger_ma, sd=sigma1_ratio)
            #スレッド作成
            thread_pool.append(threading.Thread(target=backtest_bollingerband, args=(symbol
                                                                                        , start_date
                                                                                        , end_date
                                                                                        , strategy_id
                                                                                        , strategy_option
                                                                                        , bollinger_ma
                                                                                        , sigma1_ratio
                                                                                        , sigma2_ratio
                                                                                        , initial_cash
                                                                                        )))
        thread_join_cnt = 0
        thread_pool_cnt = len(thread_pool)
        #symbol単位のスレッド実行
        for t in thread_pool:
            t.start()
        #スレッド終了まで待機
        for t in thread_pool:
            t.join()
            thread_join_cnt += 1
            logger.info("*** thread join[%d]/[%d] ***" % (thread_join_cnt, thread_pool_cnt))
        thread_pool.clear()
    logger.info("bruteforce_bollingerband_dailytrail done symbol[%s]" % (symbol))

def get_bollingerband_dailytrail_settings(symbol):
    conn = MyDB().get_db()
    c = conn.cursor()
    c.execute("""
    select
     symbol
    ,sma
    ,sigma1
    from bollingerband_dailytrail
    where symbol = '{symbol}'
    """.format(symbol=symbol))
    rs = c.fetchall()
    conn.close()
    return rs

def backtest(symbols, start_date, end_date, initial_cash, brute_force=False):
    work_size = 16 #16symbolずつ実行
    thread_pool = list()
    fin_cnt = 0
    max_cnt = len(symbols)
    while True:
        #symbol読み込み
        symbols_work = list()
        symbols_len = len(symbols)
        if symbols_len > work_size:
            symbols_work = symbols[:work_size]
            symbols = symbols[work_size:]
        elif symbols_len > 0:
            symbols_work = symbols[:symbols_len]
            symbols.clear()
        else:
            break
        #symbol単位でスレッド作成
        for symbol in symbols_work:
            """ボリンジャーバンド""" #TODO:他のテクニカル指標対応
            if brute_force:
                bruteforce_bollingerband_dailytrail(symbol, start_date, end_date, initial_cash)
                continue
            #ストラテジ取得
            rs = get_bollingerband_dailytrail_settings(symbol)
            #ボリンジャーバンド+DailyTrail
            #デフォルト設定
            strategy_id = 1
            bollinger_ma = 3 #移動平均の日数
            sigma1_ratio = 1.0 #トレンドを判定するsigmaの倍率
            sigma2_ratio = 3.0 #トレンドを判定するsigma2の倍率
            strategy_option = "SMA{sma}SD{sd:.1f}".format(sma=bollinger_ma, sd=sigma1_ratio)
            #結果が0件のときはデフォルト設定で実行する
            if not rs:
                #スレッド作成
                thread_pool.append(threading.Thread(target=backtest_bollingerband, args=(symbol
                                                                                            , start_date
                                                                                            , end_date
                                                                                            , strategy_id
                                                                                            , strategy_option
                                                                                            , bollinger_ma
                                                                                            , sigma1_ratio
                                                                                            , sigma2_ratio
                                                                                            , initial_cash
                                                                                            )))
                continue
            for r in rs:
                bollinger_ma = r[1]
                sigma1_ratio = r[2]
                strategy_option = "SMA{sma}SD{sd:.1f}".format(sma=bollinger_ma, sd=sigma1_ratio)
                #スレッド作成
                thread_pool.append(threading.Thread(target=backtest_bollingerband, args=(symbol
                                                                                            , start_date
                                                                                            , end_date
                                                                                            , strategy_id
                                                                                            , strategy_option
                                                                                            , bollinger_ma
                                                                                            , sigma1_ratio
                                                                                            , sigma2_ratio
                                                                                            , initial_cash
                                                                                            )))
        thread_join_cnt = 0
        thread_pool_cnt = len(thread_pool)
        #symbol単位のスレッド実行
        for t in thread_pool:
            t.start()
        #スレッド終了まで待機
        for t in thread_pool:
            t.join()
            thread_join_cnt += 1
            logger.info("*** thread join[%d]/[%d] ***" % (thread_join_cnt, thread_pool_cnt))
        thread_pool.clear()
        fin_cnt += len(symbols_work)
        logger.info("backtest(%d/%d)" % (fin_cnt, max_cnt))

if __name__ == '__main__':
    trade_fee = 0.1
    conf = common.read_conf()
    s = mylogger.Logger()
    inicash = int(conf['initial_cash'])
    args = get_option()
    if args.symbol is None:
        symbol_txt = conf['symbol']
    else:
        symbol_txt = args.symbol
    ss = symbol.get_symbols(symbol_txt)
    if args.start_date is None:
        start_date = conf['backtest_startdate']
    else:
        start_date = args.start_date
    if args.end_date is None:
        end_date = get_max_businessdate_from_ohlc(ss)
    else:
        end_date = args.end_date
    if args.brute_force:
        brute_force = True
    else:
        brute_force = False
    backtest(ss, start_date, end_date, inicash, brute_force)
    ss = symbol.get_symbols(symbol_txt)
    BacktestDumper().update_expected_rate(ss)
    BacktestDumper().update_maxdrawdown(ss)

