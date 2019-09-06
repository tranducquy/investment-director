#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from quotes import Quotes
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import sqlite3
import numpy as np
import threading
import numpy
from argparse import ArgumentParser
import common
import my_logger 
from position import Position
from positiontype import PositionType
from order import Order
from ordertype import OrderType
import my_lock
from butler import bollingerband
from butler import new_value_and_moving_average
from butler import bandwalk 
from www import tick
import investment_director
from www import symbol

s = my_logger.Logger()
logger = s.myLogger()

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--symbol', type=str, help='Absolute/relative path to input file')
    argparser.add_argument('--start_date', type=str, help='Date of backtest start')
    argparser.add_argument('--end_date', type=str, help='Date of backtest end')
    args = argparser.parse_args()
    return args

def set_order_info(info, order):
    info['create_date'] = order.create_date
    info['order_date'] = order.order_date
    info['close_order_date'] = order.close_order_date
    info['order_type'] = order.order_type
    info['order_status'] = order.order_status
    info['vol'] = order.vol
    info['price'] = order.price

def check_float(num):
    if (
        num is None 
            or numpy.isnan(num)
    ):
        return 0.00
    else:
        return float(num)

def make_history(
              symbol
            , strategy_id
            , strategy_option
            , business_date
            , quotes
            , idx
            , order_info
            , call_order_info
            , execution_order_info
            , position
            , cash
            , pos_vol
            , pos_price
            , total_value
            , trade_perfomance):
    if 'volume' in quotes.quotes:
        vol = float(quotes.quotes['volume'][idx])
    else:
        vol = 0.00
    t = (
          symbol
        , strategy_id
        , strategy_option
        , business_date
        , check_float(quotes.quotes['open'][idx])
        , check_float(quotes.quotes['high'][idx])
        , check_float(quotes.quotes['low'][idx])
        , check_float(quotes.quotes['close'][idx])
        , vol
        , check_float(quotes.sma[idx])
        , check_float(quotes.upper_ev_sigma[idx])
        , check_float(quotes.lower_ev_sigma[idx])
        , check_float(quotes.upper_ev2_sigma[idx])
        , check_float(quotes.lower_ev2_sigma[idx])
        , check_float(quotes.vol_ma[idx])
        , check_float(quotes.vol_upper_ev_sigma[idx])
        , check_float(quotes.vol_lower_ev_sigma[idx])
        , order_info['create_date']
        , order_info['order_type']
        , check_float(order_info['vol'])
        , check_float(order_info['price'])
        , call_order_info['order_date']
        , call_order_info['order_type']
        , check_float(call_order_info['vol'])
        , check_float(call_order_info['price'])
        , execution_order_info['close_order_date']
        , execution_order_info['order_type']
        , execution_order_info['order_status']
        , check_float(execution_order_info['vol'])
        , check_float(execution_order_info['price'])
        , position
        , check_float(cash)
        , check_float(pos_vol)
        , check_float(pos_price)
        , check_float(total_value)
        , check_float(trade_perfomance['profit_value'])
        , check_float(trade_perfomance['profit_rate'])
    )
    return t

def save_history(backtest_history):
    try:
        my_lock.lock.acquire()
        conn = sqlite3.connect(dbfile, isolation_level='EXCLUSIVE')
        c = conn.cursor()
        c.executemany("""
                    insert or replace into backtest_history
                    (
                        symbol,
                        strategy_id,
                        strategy_option,
                        business_date,
                        open,
                        high,
                        low,
                        close,
                        volume,
                        sma,
                        upper_sigma1,
                        lower_sigma1,
                        upper_sigma2,
                        lower_sigma2,
                        vol_sma,
                        vol_upper_sigma1,
                        vol_lower_sigma1,
                        order_create_date,
                        order_type,
                        order_vol, 
                        order_price,
                        call_order_date,
                        call_order_type,
                        call_order_vol,
                        call_order_price,
                        execution_order_date,
                        execution_order_type,
                        execution_order_status,
                        execution_order_vol,
                        execution_order_price,
                        position,
                        cash,
                        pos_vol,
                        pos_price,
                        total_value,
                        profit_value,
                        profit_rate
                    )
                    values
                    ( 
                         ?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                    )
                """,
                backtest_history
        )
    except Exception as err:
        if conn: 
            conn.rollback()
            logger.error(err)
    finally:
        if conn: 
            conn.commit()
            conn.close
        my_lock.lock.release()

def make_summary_msg(symbol, strategy_id, strategy_option, title, summary, quotes):
    if quotes.quotes.index.size == 0:
        return "\n"
    if summary['WinCount'] == 0 and summary['LoseCount'] == 0:
        win_rate = 0
    else:
        win_rate = round(summary['WinCount'] / (summary['WinCount'] + summary['LoseCount']) * 100, 2)
    if summary['LongWinCount'] == 0 and summary['LongLoseCount'] == 0:
        long_win_rate = 0
    else:
        long_win_rate = round(summary['LongWinCount'] / (summary['LongWinCount'] + summary['LongLoseCount']) * 100, 2)
    if summary['ShortWinCount'] == 0 and summary['ShortLoseCount'] == 0:
        short_win_rate = 0
    else:
        short_win_rate = round(summary['ShortWinCount'] / (summary['ShortWinCount'] + summary['ShortLoseCount']) * 100, 2)
    if summary['WinCount'] == 0 or summary['LoseCount'] == 0:
        payoffratio = 0
    else:
        payoffratio = round((summary['WinValue'] / summary['WinCount']) / (summary['LoseValue'] / summary['LoseCount']), 2)
    if summary['LongWinCount'] == 0 or summary['LongLoseCount'] == 0:
        long_payoffratio = 0
    else:
        long_payoffratio = round((summary['LongWinValue'] / summary['LongWinCount']) / (summary['LongLoseValue'] / summary['LongLoseCount']), 2)
    if summary['ShortWinCount'] == 0 or summary['ShortLoseCount'] == 0:
        short_payoffratio = 0
    else:
        short_payoffratio = round((summary['ShortWinValue'] / summary['ShortWinCount']) / (summary['ShortLoseValue'] / summary['ShortLoseCount']), 2)
    if summary['InitValue'] == 0:
        rate_of_return = 0
    else:
        rate_of_return = round((summary['LastValue'] - summary['InitValue']) / summary['InitValue'] * 100, 2) 
    if summary['WinCount'] == 0 and summary['LoseCount'] == 0:
        expected_rate = 0
    else:
        expected_rate = round(summary['ProfitRateSummary'] / (summary['WinCount'] + summary['LoseCount']), 2)
    if summary['LongWinCount'] == 0 and summary['LongLoseCount'] == 0:
        long_expected_rate = 0
    else:
        long_expected_rate = round(summary['LongProfitRateSummary'] / (summary['LongWinCount'] + summary['LongLoseCount']), 2)
    if summary['ShortWinCount'] == 0 and summary['ShortLoseCount'] == 0:
        short_expected_rate = 0
    else:
        short_expected_rate = round(summary['ShortProfitRateSummary'] / (summary['ShortWinCount'] + summary['ShortLoseCount']), 2)
    if (summary['WinCount'] == 0 and summary['LoseCount'] == 0) or summary['PositionHavingDays'] == 0:
        expected_rate_per_1day = 0
    else:
        expected_rate_per_1day = round(expected_rate / (summary['PositionHavingDays'] / (summary['WinCount'] + summary['LoseCount'])), 2)
    if (summary['LongWinCount'] == 0 and summary['LongLoseCount'] == 0) or summary['LongPositionHavingDays'] == 0:
        long_expected_rate_per_1day = 0
    else:
        long_expected_rate_per_1day = round(long_expected_rate / (summary['LongPositionHavingDays'] / (summary['LongWinCount'] + summary['LongLoseCount'])), 2)
    if (summary['ShortWinCount'] == 0 and summary['ShortLoseCount'] == 0) or summary['ShortPositionHavingDays'] == 0:
        short_expected_rate_per_1day = 0
    else:
        short_expected_rate_per_1day = round(short_expected_rate / (summary['ShortPositionHavingDays'] / (summary['ShortWinCount'] + summary['ShortLoseCount'])), 2)
    if summary['PositionHavingDays'] == 0 and (summary['WinCount'] + summary['LoseCount']) == 0:
        position_having_days_per_trade = 0
    else:
        position_having_days_per_trade = round(summary['PositionHavingDays'] / (summary['WinCount'] + summary['LoseCount']), 2)
    start_date = quotes.start_date
    end_date =quotes.end_date
    market_start_date = quotes.get_headdate()
    market_end_date =quotes.get_taildate()
    regist_date = datetime.today().strftime("%Y-%m-%d")
    msg  = "%s" % symbol
    msg += ",%s" % title
    msg += ",バックテスト開始日:%s" % (start_date)
    msg += ",バックテスト終了日:%s" % (end_date)
    msg += ",取引開始日:%s" % (market_start_date)
    msg += ",取引終了日:%s" % (market_end_date)
    msg += ",日数：%d" % (datetime.strptime(market_end_date, "%Y-%m-%d") - datetime.strptime(market_start_date, "%Y-%m-%d")).days
    msg += ",トレード保有日数:%d" % (summary['PositionHavingDays'])
    msg += ",1トレードあたりの平均日数:%d" % position_having_days_per_trade
    msg += ",初期資産:%f" % (summary['InitValue'])
    msg += ",最終資産:%f" % (summary['LastValue'])
    msg += ",全体騰落率(%%):%f" % rate_of_return
    msg += ",勝ちトレード数:%d" % (summary['WinCount'])
    msg += ",負けトレード数:%d" % (summary['LoseCount'])
    msg += ",勝率(%%):%f" % win_rate
    msg += ",ペイオフレシオ:%f" % payoffratio
    msg += ",1トレードあたりの期待利益率(%%):%f" % expected_rate
    msg += ",1トレードあたりの期待利益率long(%%):%f" % long_expected_rate
    msg += ",1トレードあたりの期待利益率short(%%):%f" % short_expected_rate
    #DBに保存
    save_simulate_result(
         symbol
        ,strategy_id
        ,strategy_option
        ,start_date
        ,end_date
        ,market_start_date
        ,market_end_date
        ,(datetime.strptime(market_end_date, "%Y-%m-%d") - datetime.strptime(market_start_date, "%Y-%m-%d")).days
        ,summary['PositionHavingDays']
        ,round(position_having_days_per_trade, 2)
        ,summary['InitValue']
        ,summary['LastValue']
        ,rate_of_return
        ,summary['WinCount']
        ,summary['LoseCount']
        ,summary['WinValue']
        ,summary['LoseValue']
        ,win_rate
        ,payoffratio
        ,expected_rate
        ,expected_rate_per_1day
        ,summary['LongWinCount']
        ,summary['LongLoseCount']
        ,summary['LongWinValue']
        ,summary['LongLoseValue']
        ,long_win_rate
        ,long_payoffratio
        ,long_expected_rate
        ,long_expected_rate_per_1day
        ,summary['ShortWinCount']
        ,summary['ShortLoseCount']
        ,summary['ShortWinValue']
        ,summary['ShortLoseValue']
        ,short_win_rate
        ,short_payoffratio
        ,short_expected_rate
        ,short_expected_rate_per_1day
        ,regist_date
    )
    return msg

def save_simulate_result(
                     symbol
                    ,strategy_id
                    ,strategy_option
                    ,start_date
                    ,end_date
                    ,market_start_date
                    ,market_end_date
                    ,backtest_period
                    ,trading_period
                    ,average_period_per_trade
                    ,initial_assets
                    ,last_assets
                    ,rate_of_return
                    ,win_count
                    ,loss_count
                    ,win_value
                    ,loss_value
                    ,win_rate
                    ,payoffratio
                    ,expected_rate
                    ,expected_rate_per_1day
                    ,long_win_count
                    ,long_loss_count
                    ,long_win_value
                    ,long_loss_value
                    ,long_win_rate
                    ,long_payoffratio
                    ,long_expected_rate
                    ,long_expected_rate_per_1day
                    ,short_win_count
                    ,short_loss_count
                    ,short_win_value
                    ,short_loss_value
                    ,short_win_rate
                    ,short_payoffratio
                    ,short_expected_rate
                    ,short_expected_rate_per_1day
                    ,regist_date
    ):
    try:
        my_lock.lock.acquire()
        conn = sqlite3.connect(dbfile, isolation_level='EXCLUSIVE')
        c = conn.cursor()
        c.execute("""
                    insert or replace into backtest_result 
                    (
                     symbol
                    ,strategy_id
                    ,strategy_option
                    ,start_date
                    ,end_date
                    ,market_start_date
                    ,market_end_date
                    ,backtest_period
                    ,trading_period
                    ,average_period_per_trade
                    ,initial_assets
                    ,last_assets
                    ,rate_of_return
                    ,win_count
                    ,loss_count
                    ,win_value
                    ,loss_value
                    ,win_rate
                    ,payoffratio
                    ,expected_rate
                    ,expected_rate_per_1day
                    ,long_win_count
                    ,long_loss_count
                    ,long_win_value
                    ,long_loss_value
                    ,long_win_rate
                    ,long_payoffratio
                    ,long_expected_rate
                    ,long_expected_rate_per_1day
                    ,short_win_count
                    ,short_loss_count
                    ,short_win_value
                    ,short_loss_value
                    ,short_win_rate
                    ,short_payoffratio
                    ,short_expected_rate
                    ,short_expected_rate_per_1day
                    ,regist_date
                )
                values
                ( 
                         ?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                        ,?
                    )
                """,
        (
         symbol
        ,strategy_id
        ,strategy_option
        ,start_date
        ,end_date
        ,market_start_date
        ,market_end_date
        ,backtest_period
        ,trading_period
        ,average_period_per_trade
        ,initial_assets
        ,last_assets
        ,rate_of_return
        ,win_count
        ,loss_count
        ,win_value
        ,loss_value
        ,win_rate
        ,payoffratio
        ,expected_rate
        ,expected_rate_per_1day
        ,long_win_count
        ,long_loss_count
        ,long_win_value
        ,long_loss_value
        ,long_win_rate
        ,long_payoffratio
        ,long_expected_rate
        ,long_expected_rate_per_1day
        ,short_win_count
        ,short_loss_count
        ,short_win_value
        ,short_loss_value
        ,short_win_rate
        ,short_payoffratio
        ,short_expected_rate
        ,short_expected_rate_per_1day
        ,regist_date
        ))
    except Exception as err:
        if conn: 
            conn.rollback()
            logger.error(err)
    finally:
        if conn: 
            conn.commit()
            conn.close
        my_lock.lock.release()

def simulator_run(title, strategy_id, strategy_option, quotes, butler, symbol, initial_cash, trade_fee, tick):
    p = Position(initial_cash, trade_fee, tick)
    backtest_history = list()
    for idx, high in enumerate(quotes.quotes['high']):
        if idx < quotes.ma_duration:
            continue
        current_position = p.get_position()
        low = quotes.quotes['low'][idx]
        open_price = quotes.quotes['open'][idx]
        business_date = quotes.quotes['business_date'][idx]
        order_info = { 'create_date':'' ,'order_date':'' ,'order_type':0 ,'order_status':0 ,'vol':0.00 ,'price':0.00 }
        call_order_info = { 'create_date':'' ,'order_date':'' ,'order_type':0 ,'order_status':0 ,'vol':0.00 ,'price':0.00 }
        execution_order_info = { 'close_order_date':'' ,'order_type':0 ,'order_status':0 ,'vol':0.00 ,'price':0.00 }
        trade_perfomance = { 'profit_value': 0.00, 'profit_rate': 0.00 }
        try:
            if (open_price is None
                or low is None
                or high is None
                or numpy.isnan(open_price) 
                or numpy.isnan(low) 
                or numpy.isnan(high)
                ):
                logger.warning('[%s][%d] ohlc is None or nan' % (symbol, idx))
                continue
        except Exception as err:
            logger.error('[%s][%d] ohlc is exception value:[%s]' % (symbol, idx, err))
            continue

        # 開場 
        # 注文を呼び出す
        if p.order != None:
            p.call_order(business_date)
            set_order_info(call_order_info, p.order)
        # 注文がある場合、約定判定
        if current_position == PositionType.NOTHING and p.order != None:
            if p.order.order_type == OrderType.STOP_MARKET_LONG:
                #約定判定
                if p.order.price == -1:
                    logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                    p.order.fail_order()
                elif high >= p.order.price and open_price >= p.order.price: #寄り付きが高値の場合
                    #最大volまで購入
                    p.open_long(business_date, open_price)
                elif high >= p.order.price:
                    p.open_long(business_date, p.order.price)
                else:
                    p.order.fail_order()
                set_order_info(execution_order_info, p.order)
            elif p.order.order_type == OrderType.STOP_MARKET_SHORT:
                #約定判定
                if p.order.price == -1:
                    logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                    p.order.fail_order()
                elif low <= p.order.price and open_price <= p.order.price: #寄り付きが安値の場合
                    #最大volまで購入
                    p.open_short(business_date, open_price)
                elif low <= p.order.price:
                    p.open_short(business_date, p.order.price)
                else:
                    p.order.fail_order()
                set_order_info(execution_order_info, p.order)
            elif p.order.order_type == OrderType.MARKET_LONG:
                #約定判定
                if p.order.price == -1:
                    logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                    p.order.fail_order()
                else:
                    #最大volまで購入
                    p.open_long(business_date, open_price)
                set_order_info(execution_order_info, p.order)
            elif p.order.order_type == OrderType.MARKET_SHORT:
                #約定判定
                if p.order.price == -1:
                    logger.error("symbol:[%s] idx:[%d] order_price:[%f]" % (symbol, idx, p.order.price))
                    p.order.fail_order()
                else:
                    #最大volまで購入
                    p.open_short(business_date, open_price)
                set_order_info(execution_order_info, p.order)
        elif current_position == PositionType.LONG and p.order != None:
            #約定判定
            if p.order.order_type == OrderType.CLOSE_STOP_MARKET_LONG: #逆指値成行買い返済
                if low <= p.order.price and open_price <= p.order.price:
                    p.close_long(business_date, open_price)
                    trade_perfomance = p.save_trade_perfomance(PositionType.LONG)
                elif low <= p.order.price:
                    p.close_long(business_date, p.order.price)
                    trade_perfomance = p.save_trade_perfomance(PositionType.LONG)
                else:
                    p.order.fail_order()
            elif p.order.order_type == OrderType.CLOSE_MARKET_LONG: #成行買い返済
                p.close_long(business_date, open_price)
                trade_perfomance = p.save_trade_perfomance(PositionType.LONG)
            set_order_info(execution_order_info, p.order)
        elif current_position == PositionType.SHORT and p.order != None:
            #約定判定
            if p.order.order_type == OrderType.CLOSE_STOP_MARKET_SHORT: #逆指値成行売り返済
                if high >= p.order.price and open_price >= p.order.price:
                    p.close_short(business_date, open_price)
                    trade_perfomance = p.save_trade_perfomance(PositionType.SHORT)
                elif high >= p.order.price:
                    p.close_short(business_date, p.order.price)
                    trade_perfomance = p.save_trade_perfomance(PositionType.SHORT)
                else:
                    p.order.fail_order()
            elif p.order.order_type == OrderType.CLOSE_MARKET_SHORT: #成行売り返済
                p.close_short(business_date, open_price)
                trade_perfomance = p.save_trade_perfomance(PositionType.SHORT)
            set_order_info(execution_order_info, p.order)
        #注文は1日だけ有効
        p.clear_order()

        # 引け後、翌日の注文作成
        current_position = p.get_position()
        if current_position == PositionType.NOTHING:
            long_order_type = butler.check_open_long(quotes, idx)
            short_order_type = butler.check_open_short(quotes, idx)
            if long_order_type == OrderType.STOP_MARKET_LONG:
                #create stop market long
                t = butler.create_order_stop_market_long_for_all_cash(p.cash, quotes, idx)
                p.create_order_stop_market_long(business_date, t[0], t[1])
                set_order_info(order_info, p.order)
            elif short_order_type == OrderType.STOP_MARKET_SHORT:
                #create stop market short
                t = butler.create_order_stop_market_short_for_all_cash(p.cash, quotes, idx)
                p.create_order_stop_market_short(business_date, t[0], t[1])
                set_order_info(order_info, p.order)
            elif long_order_type == OrderType.MARKET_LONG:
                t = butler.create_order_market_long_for_all_cash(p.cash, quotes, idx)
                p.create_order_market_long(business_date, t[0], t[1])
                set_order_info(order_info, p.order)
            elif short_order_type == OrderType.MARKET_SHORT:
                t = butler.create_order_market_short_for_all_cash(p.cash, quotes, idx)
                p.create_order_market_short(business_date, t[0], t[1])
                set_order_info(order_info, p.order)
        elif current_position == PositionType.LONG:
            close_order_type = butler.check_close_long(p.pos_price, quotes, idx)
            if close_order_type == OrderType.CLOSE_STOP_MARKET_LONG:
                #逆指値成行買い返済注文
                price = butler.create_order_close_stop_market_long(quotes, idx)
                p.create_order_close_stop_market_long(business_date, price, p.pos_vol)
                set_order_info(order_info, p.order)
            elif close_order_type == OrderType.CLOSE_MARKET_LONG:
                #成行買い返済注文
                price = butler.create_order_close_market_long(quotes, idx)
                p.create_order_close_market_long(business_date, price, p.pos_vol)
                set_order_info(order_info, p.order)
            else:
                pass #注文無し
        elif current_position == PositionType.SHORT:
            close_order_type = butler.check_close_short(p.pos_price, quotes, idx)
            if close_order_type == OrderType.CLOSE_STOP_MARKET_SHORT:
                #逆指値成行売り返済注文
                price = butler.create_order_close_stop_market_short(quotes, idx)
                p.create_order_close_stop_market_short(business_date, price, p.pos_vol)
                set_order_info(order_info, p.order)
            if close_order_type == OrderType.CLOSE_MARKET_SHORT:
                #成行売り返済注文
                price = butler.create_order_close_market_short(quotes, idx)
                p.create_order_close_market_short(business_date, price, p.pos_vol)
                set_order_info(order_info, p.order)
            else:
                pass #注文無し
        #1日の結果を出力
        close = 0
        if quotes.quotes['close'][idx] is None:
            close = 0
        else:
            close = quotes.quotes['close'][idx]
        history = make_history(
              symbol
            , strategy_id
            , strategy_option
            , business_date
            , quotes
            , idx
            , order_info
            , call_order_info
            , execution_order_info
            , p.position
            , p.cash
            , p.pos_vol
            , p.pos_price
            , round(p.cash + p.pos_vol * close, 2)
            , trade_perfomance
            )
        backtest_history.append(history)
    #シミュレーション結果を出力
    summary_msg_log = make_summary_msg(symbol, strategy_id, strategy_option, title, p.summary, quotes)
    save_history(backtest_history)
    logger.info(summary_msg_log)

def backtest_bollingerband(symbol, start_date, end_date, strategy_id, strategy_option, ma, diff, ev_sigma, ev2_sigma, vol_ma, vol_ev_sigma):
    q = Quotes(dbfile, symbol, start_date, end_date, ma, ev_sigma, ev2_sigma, vol_ma, vol_ev_sigma)
    t = tick.get_tick(symbol)
    bollinger_butler = bollingerband.Butler(t, ma, diff, True)
    title = "ボリンジャーバンド新値SMA%dSD%s" % (ma, '{:.1f}'.format(ev_sigma))
    simulator_run(title, strategy_id, strategy_option, q, bollinger_butler, symbol, initial_cash, trade_fee, t) 

def get_bollingerband_newvalue_settings(db, symbol):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""
    select
     symbol
    ,sma
    ,sigma1
    from bollingerband_newvalue
    where symbol = '{symbol}'
    """.format(symbol=symbol))
    rs = c.fetchall()
    conn.close()
    return rs

def backtest(db, symbols, start_date, end_date):
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
            #ストラテジ取得
            rs = get_bollingerband_newvalue_settings(db, symbol)
            #ボリンジャーバンド+新値 
            #デフォルト設定
            strategy_id = 1
            bollinger_ma = 3 #移動平均の日数
            diff_price = 0.0000 #決済する差額
            sigma1_ratio = 1.0 #トレンドを判定するsigmaの倍率
            sigma2_ratio = 3.0 #トレンドを判定するsigma2の倍率
            vol_ma = 14
            vol_sigma_ratio = 1.0
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
                                                                                            , diff_price
                                                                                            , sigma1_ratio
                                                                                            , sigma2_ratio
                                                                                            , vol_ma
                                                                                            , vol_sigma_ratio)))
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
                                                                                            , diff_price
                                                                                            , sigma1_ratio
                                                                                            , sigma2_ratio
                                                                                            , vol_ma
                                                                                            , vol_sigma_ratio)))
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
    s = my_logger.Logger()
    dbfile = conf['dbfile']
    initial_cash = int(conf['initial_cash'])
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
        end_date = investment_director.get_max_businessdate_from_ohlc(dbfile, ss)
    else:
        end_date = args.end_date
    backtest(dbfile, ss, start_date, end_date)

