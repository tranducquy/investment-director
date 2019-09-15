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
import my_logger 
from butler import bollingerband
from butler import new_value_and_moving_average
from butler import bandwalk 
from www import tick
import investment_director
from www import symbol
from market import Market
from my_db import MyDB
from assets import Assets

s = my_logger.Logger()
logger = s.myLogger()

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--symbol', type=str, help='Absolute/relative path to input file')
    argparser.add_argument('--start_date', type=str, help='Date of backtest start')
    argparser.add_argument('--end_date', type=str, help='Date of backtest end')
    argparser.add_argument('--period', type=str, help='for bitmex_cc/minkabu_fx')
    argparser.add_argument('--brute_force', type=str, help='breaking the code!')
    args = argparser.parse_args()
    return args

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

def backtest(symbols, start_date, end_date, initial_cash, brute_force=None):
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
            if not brute_force is None:
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

def get_dates():
    end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date_3month = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(months=3)).strftime("%Y-%m-%d")
    start_date_1year = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(years=1)).strftime("%Y-%m-%d")
    start_date_3year = (datetime.strptime(end_date, "%Y-%m-%d")- relativedelta(years=3)).strftime("%Y-%m-%d")
    start_date_15year = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(years=15)).strftime("%Y-%m-%d")
    return (
              end_date 
            , start_date_3month
            , start_date_1year
            , start_date_3year
            , start_date_15year
            )

def update_expected_rate():
    logger.info("update_expected_rate()")
    (end_date , start_date_3month , start_date_1year , start_date_3year , start_date_15year) = get_dates()
    #backtest_result table取得
    conn = MyDB().get_db()
    c = conn.cursor()
    c.execute("""
    select
     symbol
    ,strategy_id
    ,strategy_option
    from backtest_result
    """)
    rs = c.fetchall()
    conn.close()
    for r in rs:
        logger.info("{symbol},{strategy_id},{strategy_option}".format(symbol=r[0], strategy_id=r[1], strategy_option=r[2]))
        conn = MyDB().get_db()
        c = conn.cursor()
        c.execute("""
                update backtest_result
                set
                 expected_rate_3month = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_3month}' and '{end_date}'
                    group by symbol, strategy_id, strategy_option
                )
                ,expected_rate_1year = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_1year}' and '{end_date}'
                    group by symbol, strategy_id, strategy_option
                )
                ,expected_rate_3year = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_3year}' and '{end_date}'
                    group by symbol, strategy_id, strategy_option
                )
                ,expected_rate_15year = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_15year}' and '{end_date}'
                    group by symbol, strategy_id, strategy_option
                )
                ,long_expected_rate_3month = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_3month}' and '{end_date}'
                    and execution_order_type = 5
                    group by symbol, strategy_id, strategy_option, execution_order_type
                )
                ,long_expected_rate_1year = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_1year}' and '{end_date}'
                    and execution_order_type = 5
                    group by symbol, strategy_id, strategy_option, execution_order_type
                )
                ,long_expected_rate_3year = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_3year}' and '{end_date}'
                    and execution_order_type = 5
                    group by symbol, strategy_id, strategy_option, execution_order_type
                )
                ,long_expected_rate_15year = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_15year}' and '{end_date}'
                    and execution_order_type = 5
                    group by symbol, strategy_id, strategy_option, execution_order_type
                )
                ,short_expected_rate_3month = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_3month}' and '{end_date}'
                    and execution_order_type = 6
                    group by symbol, strategy_id, strategy_option, execution_order_type
                )
                ,short_expected_rate_1year = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_1year}' and '{end_date}'
                    and execution_order_type = 6
                    group by symbol, strategy_id, strategy_option, execution_order_type
                )
                ,short_expected_rate_3year = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_3year}' and '{end_date}'
                    and execution_order_type = 6
                    group by symbol, strategy_id, strategy_option, execution_order_type
                )
                ,short_expected_rate_15year = 
                (
                    select 
                     sum(profit_rate) 
                    from backtest_history 
                    where symbol='{symbol}' 
                    and strategy_id = {strategy_id} 
                    and strategy_option = '{strategy_option}' 
                    and business_date between '{start_date_15year}' and '{end_date}'
                    and execution_order_type = 6
                    group by symbol, strategy_id, strategy_option, execution_order_type
                )
                where symbol = '{symbol}' and strategy_id = {strategy_id} and strategy_option = '{strategy_option}'
                """.format(
                              symbol=r[0]
                            , strategy_id=r[1]
                            , strategy_option=r[2]
                            , end_date=end_date
                            , start_date_3month=start_date_3month
                            , start_date_1year=start_date_1year
                            , start_date_3year=start_date_3year
                            , start_date_15year=start_date_15year
                )
        )
        conn.commit()
        conn.close()

if __name__ == '__main__':
    trade_fee = 0.1
    conf = common.read_conf()
    s = my_logger.Logger()
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
        end_date = investment_director.get_max_businessdate_from_ohlc(ss)
    else:
        end_date = args.end_date
    if args.brute_force is None:
        brute_force = None
    else:
        brute_force = args.brute_force
    backtest(ss, start_date, end_date, inicash, brute_force)
    update_expected_rate()

