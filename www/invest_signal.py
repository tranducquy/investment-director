# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import symbol

def _get_open_signal_nikkei225_topix500(db, start_date, end_date, symbols):
    #3ヶ月、1,3,15年のバックテストで利益の出ている銘柄のみ探す
    start_date_3month = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(months=3)).strftime("%Y-%m-%d")
    start_date_1year = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(years=1)).strftime("%Y-%m-%d")
    start_date_3year = (datetime.strptime(end_date, "%Y-%m-%d")- relativedelta(years=3)).strftime("%Y-%m-%d")
    start_date_15year = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(years=15)).strftime("%Y-%m-%d")

    c = db.cursor()
    sql = """
    select
     r.symbol
    ,r.strategy
    ,order_table.order_name
    ,order_table.order_price
    ,r.end_date
    ,m3.profit_rate_sum as 期待利益率3か月
    ,y1.profit_rate_sum as 期待利益率1年
    ,y3.profit_rate_sum as 期待利益率3年
    ,y15.profit_rate_sum as 期待利益率15年
    ,r.expected_rate as 全期間期待利益率
    ,r.long_expected_rate as 全期間期待利益率long
    ,r.short_expected_rate as 全期間期待利益率short
    ,r.win_rate as 勝率
    ,r.average_period_per_trade as 平均取引期間
    ,r.win_count+r.loss_count as 取引数
    ,r.long_win_count+r.long_loss_count as 取引数long
    ,r.short_win_count+r.short_loss_count as 取引数short
    ,r.payoffratio as ペイオフレシオ
   from backtest_result r
   left outer join (
   select
     symbol
    ,strategy_id
    ,sum(profit_rate) as profit_rate_sum
    ,count(business_date) as count
   from backtest_history
   where business_date between '%s' and '%s'
   group by symbol, strategy_id
   HAVING count(business_date) > 45
   ) m3
   on r.symbol = m3.symbol and r.strategy_id = m3.strategy_id
   left outer join (
   select
     symbol
    ,strategy_id
    ,sum(profit_rate) as profit_rate_sum
   from backtest_history
   where business_date between '%s' and '%s'
   group by symbol, strategy_id
   HAVING count(business_date) > 183
   ) y1
   on r.symbol = y1.symbol and r.strategy_id = y1.strategy_id
   left outer join (
   select
     symbol
    ,strategy_id
    ,sum(profit_rate) as profit_rate_sum
   from backtest_history
   where business_date between '%s' and '%s'
   group by symbol, strategy_id
   HAVING count(business_date) > 548
   ) y3
   on r.symbol = y3.symbol and r.strategy_id = y3.strategy_id
   left outer join (
   select
     symbol
    ,strategy_id
    ,sum(profit_rate) as profit_rate_sum
   from backtest_history
   where business_date between '%s' and '%s'
   group by symbol, strategy_id
   HAVING count(business_date) > 2738
   ) y15
   on r.symbol = y15.symbol and r.strategy_id = y15.strategy_id
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
        where bh.business_date = (select max(business_date) from backtest_history)
        and bh.order_type in (1, 2)
        and bh.order_price > 0
        and bh.order_vol > 0
   ) as order_table
   on r.symbol = order_table.symbol
   where r.start_date = '%s'
   and r.end_date = '%s'
   and r.rate_of_return > 0
   and (m3.profit_rate_sum > 3 and y1.profit_rate_sum > 15 and y3.profit_rate_sum > 45 and y15.profit_rate_sum > 225)
   and r.symbol in ({0})
   order by m3.profit_rate_sum desc
       """ % (
             start_date_3month, end_date
           , start_date_1year, end_date
           , start_date_3year, end_date
           , start_date_15year, end_date
           , start_date, end_date
           )
    sql = sql.format(', '.join('?' for _ in symbols))
    c.execute(sql, symbols)
    symbols = c.fetchall()
    c.close()
    return symbols

def direct_open_order(db, symbol_txt, start_date, end_date):
    symbols = symbol.get_symbols(symbol_txt)
    start_date = start_date
    end_date = end_date
    result = _get_open_signal_nikkei225_topix500(db, start_date, end_date, symbols)
    return result

def _check_close_order(butler, q, position, position_price, symbol, strategy):
    pass

def direct_close_order(dbfile, symbol, position, position_price):
    pass

