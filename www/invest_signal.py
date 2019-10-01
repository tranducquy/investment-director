# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import symbol as sy
import tick

def _get_open_signal_nikkei225_topix500(db, start_date, end_date, symbols, strategy_id):
    #3ヶ月、1,3,15年のバックテストで利益の出ている銘柄のみ探す
    c = db.cursor()
    sql = u"""
    select
     r.symbol
    ,ms.strategy_name
    ,r.strategy_option
    ,order_table.order_name
    ,order_table.order_price
    ,r.end_date
    ,r.rate_of_return as 全期間騰落率
    ,r.profit_rate_3month as 利益率3か月
    ,r.long_profit_rate_3month as 利益率3か月long
    ,r.short_profit_rate_3month as 利益率3か月short
    ,r.profit_rate_1year as 利益率1年
    ,r.long_profit_rate_1year as 利益率1年long
    ,r.short_profit_rate_1year as 利益率1年short
    ,r.profit_rate_3year as 利益率3年
    ,r.long_profit_rate_3year as 利益率3年long
    ,r.short_profit_rate_3year as 利益率3年short
    ,r.profit_rate_15year as 利益率15年
    ,r.long_profit_rate_15year as 利益率15年long
    ,r.short_profit_rate_15year as 利益率15年short
    ,r.drawdown as 最大ドローダウン全期間
    ,r.drawdown_3month as 最大ドローダウン3か月
    ,r.drawdown_1year as 最大ドローダウン1年
    ,r.drawdown_3year as 最大ドローダウン3年
    ,r.drawdown_15year as 最大ドローダウン15年
    ,r.expected_rate_3month as 期待利益率3か月
    ,r.long_expected_rate_3month as 期待利益率3か月long
    ,r.short_expected_rate_3month as 期待利益率3か月short
    ,r.expected_rate_1year as 期待利益率1年
    ,r.long_expected_rate_1year as 期待利益率1年long
    ,r.short_expected_rate_1year as 期待利益率1年short
    ,r.expected_rate_3year as 期待利益率3年
    ,r.long_expected_rate_3year as 期待利益率3年long
    ,r.short_expected_rate_3year as 期待利益率3年short
    ,r.expected_rate_15year as 期待利益率15年
    ,r.long_expected_rate_15year as 期待利益率15年long
    ,r.short_expected_rate_15year as 期待利益率15年short
    ,r.expected_rate as 全期間期待利益率
    ,r.long_expected_rate as 全期間期待利益率long
    ,r.short_expected_rate as 全期間期待利益率short
    ,r.win_rate as 勝率
    ,r.average_period_per_trade as 平均取引期間
    ,r.win_count+r.loss_count as 取引数
    ,r.long_win_count+r.long_loss_count as 取引数long
    ,r.short_win_count+r.short_loss_count as 取引数short
    ,r.payoffratio as ペイオフレシオ
    ,cast(order_table.order_max_vol * 0.01 / 100 as int) * 100
    from backtest_result r
    inner join (
        select
         bh.symbol
        ,bh.strategy_id
        ,bh.strategy_option
        ,bh.order_create_date
        ,bh.order_type
        ,mo.ordertype_name as order_name
        ,bh.order_vol
        ,bh.order_price
        ,bh.vol_sma as order_max_vol
        from backtest_history as bh
        inner join m_ordertype as mo
         on bh.order_type = mo.ordertype_id
        inner join (
            select
             symbol
             ,strategy_id
             ,strategy_option
             ,max(business_date) as max_business_date
            from backtest_history
            group by symbol, strategy_id, strategy_option
            ) as bhmd
         on bh.symbol = bhmd.symbol
         and bh.strategy_id = bhmd.strategy_id
         and bh.strategy_option = bhmd.strategy_option
         and bh.business_date = bhmd.max_business_date
        where 0 = 0
        and bh.order_type in (1, 2)
        and bh.order_price > 0
        and bh.order_vol != 0
    ) as order_table
    on r.symbol = order_table.symbol
    and r.strategy_id = order_table.strategy_id
    and r.strategy_option = order_table.strategy_option
    left outer join m_strategy as ms
    on r.strategy_id = ms.strategy_id
    where 0 = 0
    and r.rate_of_return > 0
    and r.symbol in ({symbols})
    and r.strategy_id = {strategy_id}
    order by r.profit_rate_1year desc
    """.format(symbols=', '.join('?' for _ in symbols), strategy_id=strategy_id)
    c.execute(sql, symbols)
    symbols = c.fetchall()
    c.close()
    return (symbols, sql)

def _get_open_signal(db, start_date, end_date, symbols, bitmex):
    #3ヶ月、1,3年のバックテストで利益の出ている銘柄のみ探す
    c = db.cursor()
    sql = u"""
    select
     r.symbol
    ,r.strategy_id
    ,r.strategy_option
    ,order_table.order_name
    ,order_table.order_price
    ,r.end_date
    ,r.rate_of_return as 全期間騰落率
    ,r.profit_rate_3month as 利益率3か月
    ,r.long_profit_rate_3month as 利益率3か月long
    ,r.short_profit_rate_3month as 利益率3か月short
    ,r.profit_rate_1year as 利益率1年
    ,r.long_profit_rate_1year as 利益率1年long
    ,r.short_profit_rate_1year as 利益率1年short
    ,r.profit_rate_3year as 利益率3年
    ,r.long_profit_rate_3year as 利益率3年long
    ,r.short_profit_rate_3year as 利益率3年short
    ,r.profit_rate_15year as 利益率15年
    ,r.long_profit_rate_15year as 利益率15年long
    ,r.long_profit_rate_15year as 利益率15年short
    ,r.drawdown as 最大ドローダウン全期間
    ,r.drawdown_3month as 最大ドローダウン3か月
    ,r.drawdown_1year as 最大ドローダウン1年
    ,r.drawdown_3year as 最大ドローダウン3年
    ,r.drawdown_15year as 最大ドローダウン15年
    ,r.expected_rate_3month as 期待利益率3か月
    ,r.long_expected_rate_3month as 期待利益率3か月long
    ,r.short_expected_rate_3month as 期待利益率3か月short
    ,r.expected_rate_1year as 期待利益率1年
    ,r.long_expected_rate_1year as 期待利益率1年long
    ,r.short_expected_rate_1year as 期待利益率1年short
    ,r.expected_rate_3year as 期待利益率3年
    ,r.long_expected_rate_3year as 期待利益率3年long
    ,r.short_expected_rate_3year as 期待利益率3年short
    ,r.expected_rate_15year as 期待利益率15年
    ,r.long_expected_rate_15year as 期待利益率15年long
    ,r.short_expected_rate_15year as 期待利益率15年short
    ,r.expected_rate as 期待利益率全期間
    ,r.long_expected_rate as 期待利益率long全期間
    ,r.short_expected_rate as 期待利益率short全期間
    ,r.win_rate as 勝率
    ,r.average_period_per_trade as 平均取引期間
    ,r.win_count+r.loss_count as 取引数
    ,r.long_win_count+r.long_loss_count as 取引数long
    ,r.short_win_count+r.short_loss_count as 取引数short
    ,r.payoffratio as ペイオフレシオ
    from backtest_result r
    inner join (
        select
         bh.symbol
        ,bh.order_create_date
        ,mo.ordertype_name as order_name
        ,bh.order_vol
        ,bh.order_price
        from backtest_history as bh
        inner join m_ordertype as mo
         on bh.order_type = mo.ordertype_id
        inner join (
            select
             symbol
        """
    if bitmex:
        sql += ",date(max(business_date), '-1 days') as max_business_date"
    else:
        sql += ",max(business_date) as max_business_date"
    sql += """
            from backtest_history
            group by symbol
            ) as bhmd
         on bh.symbol = bhmd.symbol
         and bh.business_date = bhmd.max_business_date
        where 0 = 0
        and bh.order_type in (1, 2)
        and bh.order_price > 0
        and bh.order_vol != 0
    ) as order_table
    on r.symbol = order_table.symbol
    where 0 = 0
    and r.rate_of_return > 0
    and r.symbol in ({0})
    order by r.profit_rate_1year desc
    """ 
    sql = sql.format(', '.join('?' for _ in symbols))
    c.execute(sql, symbols)
    symbols = c.fetchall()
    c.close()
    return (symbols, sql)

def direct_open_order(db, symbol_txt, start_date, end_date, strategy_id):
    symbols = sy.get_symbols(symbol_txt)
    start_date = start_date
    end_date = end_date
    if 'Nikkei225' in symbol_txt or 'recommend' in symbol_txt or 'close_on_daily' in symbol_txt:
        (result, query) = _get_open_signal_nikkei225_topix500(db, start_date, end_date, symbols, strategy_id)
    elif 'bitmex' in symbol_txt or 'minkabu' in symbol_txt:
        (result, query) = _get_open_signal(db, start_date, end_date, symbols, True)
    else:
        (result, query) = _get_open_signal(db, start_date, end_date, symbols, False)
    return (result, query)

def _get_max_businessdate(db, symbol):
    sql = """
    select
    max(business_date)
    from backtest_history
    where symbol = ?
    """
    c = db.cursor()
    c.execute(sql, [symbol])
    r = c.fetchall()
    c.close()
    business_date = ""
    if r:
        business_date = r[0][0]
    return business_date

def _get_quotes(db, symbol, business_date):
    sql = u"""
    select
     symbol
    ,business_date
    ,open
    ,high
    ,low
    ,close
    from ohlc
    where symbol = ?
    and business_date = ?
    """
    c = db.cursor()
    c.execute(sql, [symbol, business_date])
    r = c.fetchall()
    quotes = None
    if r:
        quotes = r[0]
    return quotes

def direct_close_order(db, symbol, position, open_price, bitmex_flg, firstday_flg):
    """現在は新値のみなので、すべての場合最終営業日の高値または安値を基準に1ティック差の価格を返す。ストラテジによって調整要"""
    close_order = dict()
    if symbol == "":
        return close_order
    #最終営業日取得
    business_date = _get_max_businessdate(db, symbol)
    losscut_ratio = 0.03
    #前日日付作成(BitMEXの場合、最終営業日の1日前)
    if bitmex_flg and business_date is not None:
        business_date = (datetime.strptime(business_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
        losscut_ratio = 0.05
    if symbol == 'GBPJPY' or symbol == 'USDJPY':
        losscut_ratio = 0.005
    #高値、安値取得
    q = _get_quotes(db, symbol, business_date)
    #前日日付の高値、安値より１ティック上または下を返す
    t = tick.get_tick(symbol)
    if q:
        if firstday_flg == '':
            if position == "long":
                close_order['ordertype'] = u"逆指値成行返売(close long)"
                close_order['orderprice']= q[4] - t
            elif position == "short":
                close_order['ordertype'] = u"逆指値成行返買(close short)"
                close_order['orderprice'] = q[3] + t
        else:
            if position == "long":
                close_order['ordertype'] = u"逆指値成行返売(当日損切りclose long)"
                close_order['orderprice']= q[3] - (q[3] * losscut_ratio)
            elif position == "short":
                close_order['ordertype'] = u"逆指値成行返買(当日損切りclose short)"
                close_order['orderprice'] = q[4] + (q[4] * losscut_ratio)
    return close_order
