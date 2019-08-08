#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from quotes import Quotes
import csv
import datetime
import sqlite3
import common
import my_logger 
from position import Position
from positiontype import PositionType
from order import Order
from ordertype import OrderType
from butler import bollingerband
from butler import new_value_and_moving_average

s = my_logger.Logger()
logger = s.myLogger()

def set_order_info(info, order):
    info['create_date'] = order.create_date
    info['order_date'] = order.order_date
    info['close_order_date'] = order.close_order_date
    info['order_type'] = order.order_type
    info['order_status'] = order.order_status
    info['vol'] = order.vol
    info['price'] = order.price

def make_history(
              business_date
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
        vol = quotes.quotes['volume'][idx]
    else:
        vol = 0.00
    t = (
          business_date
        , quotes.quotes['close'][idx]
        , quotes.quotes['open'][idx]
        , quotes.quotes['high'][idx]
        , quotes.quotes['low'][idx]
        , vol
        , quotes.sma[idx]
        , quotes.upper2_sigma[idx]
        , quotes.lower2_sigma[idx]
        , order_info['create_date']
        , order_info['order_type']
        , order_info['vol']
        , order_info['price']
        , call_order_info['order_date']
        , call_order_info['order_type']
        , call_order_info['vol']
        , call_order_info['price']
        , execution_order_info['close_order_date']
        , execution_order_info['order_type']
        , execution_order_info['order_status']
        , execution_order_info['vol']
        , execution_order_info['price']
        , position
        , cash
        , pos_vol
        , pos_price
        , total_value
        , trade_perfomance['profit_value']
        , trade_perfomance['profit_rate']
    )
    return t

def get_summary_msgheader():
    msg  = "シンボル"
    msg += ",ストラテジ"
    msg += ",開始日"
    msg += ",終了日"
    msg += ",バックテスト日数"
    msg += ",トレード保有日数"
    msg += ",1トレードあたりの平均日数"
    msg += ",初期資産"
    msg += ",最終資産"
    msg += ",全体騰落率(%%)"
    msg += ",勝ちトレード数"
    msg += ",負けトレード数"
    msg += ",勝ち額"
    msg += ",負け額"
    msg += ",勝率(%%)"
    msg += ",ペイオフレシオ"
    msg += ",1トレードあたりの期待損益率(%%)¥n"
    return msg

def make_summary_msg(csvfilename, title, summary, quotes, for_csv):
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
    start_date = quotes.get_headdate()
    end_date =quotes.get_taildate()
    msg = ""
    if for_csv:
        msg  = "%s" % symbol
        msg += ",%s" % title
        msg += ",%s" % (start_date)
        msg += ",%s" % (end_date)
        msg += ",%d" % (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(start_date, "%Y-%m-%d")).days
        msg += ",%d" % (summary['PositionHavingDays'])
        msg += ",%d" % position_having_days_per_trade
        msg += ",%f" % (summary['InitValue'])
        msg += ",%f" % (summary['LastValue'])
        msg += ",%f" % rate_of_return
        msg += ",%d" % (summary['WinCount'])
        msg += ",%d" % (summary['LoseCount'])
        msg += ",%f" % (summary['WinValue'])
        msg += ",%f" % (summary['LoseValue'])
        msg += ",%f" % win_rate
        msg += ",%f" % payoffratio
        msg += ",%f" % expected_rate
        msg += ",%f" % expected_rate_per_1day
        msg += ",%f" % (summary['LongWinValue'])
        msg += ",%f" % (summary['LongLoseValue'])
        msg += ",%f" % long_win_rate
        msg += ",%f" % long_payoffratio
        msg += ",%f" % long_expected_rate
        msg += ",%f" % long_expected_rate_per_1day
        msg += ",%f" % (summary['ShortWinValue'])
        msg += ",%f" % (summary['ShortLoseValue'])
        msg += ",%f" % short_win_rate
        msg += ",%f" % short_payoffratio
        msg += ",%f" % short_expected_rate
        msg += ",%f\n" % short_expected_rate_per_1day
    else:
        msg  = "%s" % symbol
        msg += ",%s" % title
        msg += ",開始日:%s" % (start_date)
        msg += ",終了日:%s" % (end_date)
        msg += ",日数：%d" % (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(start_date, "%Y-%m-%d")).days
        msg += ",トレード保有日数:%d" % (summary['PositionHavingDays'])
        msg += ",1トレードあたりの平均日数:%d" % position_having_days_per_trade
        msg += ",初期資産:%f" % (summary['InitValue'])
        msg += ",最終資産:%f" % (summary['LastValue'])
        msg += ",全体騰落率(%%):%f" % rate_of_return
        msg += ",勝ちトレード数:%d" % (summary['WinCount'])
        msg += ",負けトレード数:%d" % (summary['LoseCount'])
        msg += ",勝ち額:%f" % (summary['WinValue'])
        msg += ",負け額:%f" % (summary['LoseValue'])
        msg += ",勝率(%%):%f" % win_rate
        msg += ",ペイオフレシオ:%f" % payoffratio
        msg += ",1トレードあたりの期待損益率(%%):%f" % expected_rate
        msg += ",トレード1日あたりの期待損益率(%%):%f\n" % expected_rate_per_1day
        msg += ",勝ち額(long):%f" % (summary['LongWinValue'])
        msg += ",負け額(long):%f" % (summary['LongLoseValue'])
        msg += ",勝率(%%)(long):%f" % long_win_rate
        msg += ",ペイオフレシオ(long):%f" % long_payoffratio
        msg += ",1トレードあたりの期待損益率(%%)(long):%f" % long_expected_rate
        msg += ",トレード1日あたりの期待損益率(%%)(long):%f\n" % long_expected_rate_per_1day
        msg += ",勝ち額(short):%f" % (summary['ShortWinValue'])
        msg += ",負け額(short):%f" % (summary['ShortLoseValue'])
        msg += ",勝率(%%)(short):%f" % short_win_rate
        msg += ",ペイオフレシオ(short):%f" % short_payoffratio
        msg += ",1トレードあたりの期待損益率(%%)(short):%f" % short_expected_rate
        msg += ",トレード1日あたりの期待損益率(%%)(short):%f\n" % short_expected_rate_per_1day
        #DBに結果を保存してしまう
        save_simulate_result(
             symbol
            ,title
            ,start_date
            ,end_date
            ,(datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(start_date, "%Y-%m-%d")).days
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
        )
    return msg

def save_simulate_result(
                     symbol
                    ,strategy
                    ,start_date
                    ,end_date
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
):
    conn = sqlite3.connect(dbfile)
    conn.execute("""
                insert or replace into backtest_result 
                (
                     symbol
                    ,strategy
                    ,start_date
                    ,end_date
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
                )
    """,
    (
        symbol
        ,strategy
        ,start_date
        ,end_date
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
    ))
    conn.commit()
    conn.close()
    pass

def simulator_run(title, quotes, butler, symbol, output_summary_filename, output_history_filename, initial_cash, trade_fee, tick):
    p = Position(initial_cash, trade_fee, tick)
    output_history = open(output_history_filename, 'w', encoding='utf-8', newline='\n')
    output_summary = open(output_summary_filename, 'a', encoding='utf-8', newline='\n')
    output_history_writer = csv.writer(output_history)
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

        # 開場 
        # 注文を呼び出す
        if p.order != None:
            p.call_order(business_date)
            set_order_info(call_order_info, p.order)
        # 注文がある場合、約定判定
        if current_position == PositionType.NOTHING and p.order != None:
            if p.order.order_type == OrderType.STOP_MARKET_LONG:
                #約定判定
                if high >= p.order.price and open_price >= p.order.price: #寄り付きが高値の場合
                    if open_price * p.order.vol < p.cash: #現金以上に購入しない
                        p.open_long(business_date, open_price)
                    else:
                        p.order.fail_order()
                elif high >= p.order.price:
                    p.open_long(business_date, p.order.price)
                else:
                    p.order.fail_order()
                set_order_info(execution_order_info, p.order)
            elif p.order.order_type == OrderType.STOP_MARKET_SHORT:
                #約定判定
                if low <= p.order.price and open_price <= p.order.price: #寄り付きが安値の場合
                    if open_price * p.order.vol < p.cash: #現金以上に空売りしない
                        p.open_short(business_date, open_price)
                    else:
                        p.order.fail_order()
                elif low <= p.order.price:
                    p.open_short(business_date, p.order.price)
                else:
                    p.order.fail_order()
                set_order_info(execution_order_info, p.order)
        elif current_position == PositionType.LONG and p.order != None:
            #約定判定
            if low <= p.order.price and open_price <= p.order.price:
                p.close_long(business_date, open_price)
                trade_perfomance = p.save_trade_perfomance(OrderType.STOP_MARKET_LONG)
            elif low <= p.order.price:
                p.close_long(business_date, p.order.price)
                trade_perfomance = p.save_trade_perfomance(OrderType.STOP_MARKET_LONG)
            else:
                p.order.fail_order()
            set_order_info(execution_order_info, p.order)
        elif current_position == PositionType.SHORT and p.order != None:
            #約定判定
            if high >= p.order.price and open_price >= p.order.price:
                p.close_short(business_date, open_price)
                trade_perfomance = p.save_trade_perfomance(OrderType.STOP_MARKET_LONG)
            elif high >= p.order.price:
                p.close_short(business_date, p.order.price)
                trade_perfomance = p.save_trade_perfomance(OrderType.STOP_MARKET_SHORT)
            else:
                p.order.fail_order()
            set_order_info(execution_order_info, p.order)
        #注文は1日だけ有効
        p.clear_order()

        # 引け後、翌日の注文作成
        current_position = p.get_position()
        if current_position == PositionType.NOTHING:
            if butler.check_open_long(quotes, idx):
                #create long order
                t = butler.create_order_stop_market_long_for_all_cash(p.cash, high, tick)
                p.create_order_stop_market_long(business_date, t[0], t[1])
                set_order_info(order_info, p.order)
            elif butler.check_open_short(quotes, idx):
                #create short order
                t = butler.create_order_stop_market_short_for_all_cash(p.cash, low, tick)
                p.create_order_stop_market_short(business_date, t[0], t[1])
                set_order_info(order_info, p.order)
        elif current_position == PositionType.LONG:
            if butler.check_close_long(p.pos_price, quotes, idx):
                price = butler.create_order_stop_market_close_long(quotes, idx, tick)
                p.create_order_stop_market_close_long(business_date, price, p.pos_vol)
                set_order_info(order_info, p.order)
        elif current_position == PositionType.SHORT:
            if butler.check_close_short(p.pos_price, quotes, idx):
                price = butler.create_order_stop_market_close_short(quotes, idx, tick)
                p.create_order_stop_market_close_short(business_date, price, p.pos_vol)
                set_order_info(order_info, p.order)
        #1日の結果を出力
        close = 0
        if quotes.quotes['close'][idx] is None:
            close = 0
        else:
            close = quotes.quotes['close'][idx]
        history = make_history(
              business_date
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
        output_history_writer.writerow(history)
    #シミュレーション結果を出力
    summary_msg_log = make_summary_msg(symbol, title, p.summary, quotes, False)
    summary_msg_csv = make_summary_msg(symbol, title, p.summary, quotes, True)
    logger.info(summary_msg_log)
    output_summary.write(summary_msg_csv)
    output_history.close()
    output_summary.close()

if __name__ == '__main__':
    initial_cash = 1000000
    trade_fee = 0.1
    tick = 0.5

    conf = common.read_conf()
    s = my_logger.Logger()
    dbfile = conf['dbfile']
    backtest_result_path = conf['backtest_result']
    backtest_summary_filename = backtest_result_path + '/summary.csv'
    start_date = "2015-01-01"
    end_date = "2018-12-31"
    symbol_txt = conf['symbol']
    symbols = open(symbol_txt, "r")
    #超短期ボリンジャーバンド
    for symbol in symbols:
        symbol = symbol.strip()
        ma_duration = 2 #移動平均の日数
        diff_price = 0.1 #決済する差額
        ev_sigma_ratio = 2.0 #トレンドを判定するsigmaの倍率
        q = Quotes(dbfile, symbol, start_date, end_date, ma_duration, ev_sigma_ratio)
        bollinger_butler = bollingerband.Butler(ma_duration, diff_price, ev_sigma_ratio)
        title = "超短期ボリンジャーバンド%d日_シグマ%s倍_決済差額%s" % (ma_duration, '{:.2f}'.format(ev_sigma_ratio), '{:.2f}'.format(diff_price))
        backtest_history_filename = backtest_result_path + symbol + '_%s-%s_b%d_s%s_diff%s.csv' % (start_date, end_date, ma_duration, '{:.2f}'.format(ev_sigma_ratio), '{:.2f}'.format(diff_price))
        simulator_run(title, q, bollinger_butler, symbol, backtest_summary_filename, backtest_history_filename, initial_cash, trade_fee, tick) 

    symbols = open(symbol_txt, "r")
    #新値＋移動平均
    for symbol in symbols:
        symbol = symbol.strip()
        ma_duration = 2 #移動平均の日数
        new_value_duration = 1 #新値の日数
        q = Quotes(dbfile, symbol, start_date, end_date, ma_duration)
        nv_ma_butler = new_value_and_moving_average.Butler(new_value_duration)
        title = "新値%d日_移動平均%d日" % (ma_duration, new_value_duration)
        backtest_history_filename = backtest_result_path + symbol + '_%s-%s_nv%d_ma%d.csv' % (start_date, end_date, ma_duration, new_value_duration)
        simulator_run(title, q, nv_ma_butler, symbol, backtest_summary_filename, backtest_history_filename, initial_cash, trade_fee, tick) 

