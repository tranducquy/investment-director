# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from datetime import timedelta 
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, g, request
import sqlite3
import invest_signal
import symbol as sy

app = Flask(__name__)

DATABASE = '/usr/local/investment-director/market-history.db'
SYMBOL_DIR = '/usr/local/investment-director/symbol/'
BACKTEST_HISTORY_QUERY = u"""
                    select 
                     bh.symbol
                    ,ms.strategy_name
                    ,bh.business_date
                    ,bh.open
                    ,bh.high
                    ,bh.low
                    ,bh.close
                    ,bh.volume
                    ,bh.sma
                    ,bh.upper_sigma1
                    ,bh.lower_sigma1
                    ,bh.upper_sigma2
                    ,bh.lower_sigma2
                    ,bh.vol_sma
                    ,bh.vol_upper_sigma1
                    ,bh.vol_lower_sigma1
                    ,bh.order_create_date
                    ,bh.order_type
                    ,bh.order_vol
                    ,bh.order_price
                    ,bh.call_order_date
                    ,bh.call_order_type
                    ,bh.call_order_vol
                    ,bh.call_order_price
                    ,bh.execution_order_date
                    ,bh.execution_order_type
                    ,bh.execution_order_status
                    ,bh.execution_order_vol
                    ,bh.execution_order_price
                    ,bh.position
                    ,bh.cash
                    ,bh.pos_vol
                    ,bh.pos_price
                    ,bh.total_value
                    ,bh.profit_value
                    ,bh.profit_rate
                    from backtest_history as bh
                    left outer join m_strategy as ms
                     on bh.strategy_id = ms.strategy_id
                    where bh.symbol = '{symbol}'
                    and bh.business_date between '{start_date}' and '{end_date}'
                    order by bh.business_date"""

OHLCV_DAILY_QUERY = u"""
                    select 
                     symbol
                    ,business_date
                    ,open
                    ,high
                    ,low
                    ,close
                    ,volume
                    from ohlc 
                    where symbol = '{symbol}'
                    and business_date between '{start_date}' and '{end_date}'
                    order by business_date
                    """

BACKTEST_SUMMARY_QUERY = u"""
                    select
                     r.symbol
                    ,ms.strategy_name
                    ,r.end_date
                    ,r.rate_of_return as 全期間騰落率_複利
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
                    from backtest_result as r
                    inner join m_strategy as ms 
                     on r.strategy_id = ms.strategy_id
                    left outer join (
                        select
                         symbol
                        ,strategy_id
                        ,sum(profit_rate) as profit_rate_sum
                        ,count(business_date) as count
                        from backtest_history
                        where business_date between '{start_date_3month}' and '{end_date}'
                        group by symbol, strategy_id
                    ) m3
                    on r.symbol = m3.symbol and r.strategy_id = m3.strategy_id
                    left outer join (
                        select
                         symbol
                        ,strategy_id
                        ,sum(profit_rate) as profit_rate_sum
                        from backtest_history
                        where business_date between '{start_date_1year}' and '{end_date}'
                        group by symbol, strategy_id
                    ) y1
                    on r.symbol = y1.symbol and r.strategy_id = y1.strategy_id
                    left outer join (
                        select
                        symbol
                        ,strategy_id
                        ,sum(profit_rate) as profit_rate_sum
                        from backtest_history
                        where business_date between '{start_date_3year}' and '{end_date}'
                        group by symbol, strategy_id
                    ) y3
                    on r.symbol = y3.symbol and r.strategy_id = y3.strategy_id
                    left outer join (
                        select
                        symbol
                        ,strategy_id
                        ,sum(profit_rate) as profit_rate_sum
                        from backtest_history
                        where business_date between '{start_date_15year}' and '{end_date}'
                        group by symbol, strategy_id
                    ) y15
                    on r.symbol = y15.symbol and r.strategy_id = y15.strategy_id
                    where 0 = 0 
                    and r.regist_date = '{regist_date}'
                    --and r.end_date = '{end_date}'
                    order by m3.profit_rate_sum desc
                    """

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/index")
def index2():
    return render_template('index.html')

@app.route('/open_signal', methods=['GET'])
def open_signal():
    symbol1 = request.args.get("symbol", "Nikkei225_TOPIX500.txt")
    symbol2 = request.args.get("symbol", "bitmex_xbtusd.txt")
    symbol3 = request.args.get("symbol", "bitmex_ethusd.txt")
    symbol4 = request.args.get("symbol", "minkabu_fx_gbpjpy.txt")
    symbol1_txt = os.path.join(SYMBOL_DIR, symbol1)
    symbol2_txt = os.path.join(SYMBOL_DIR, symbol2)
    symbol3_txt = os.path.join(SYMBOL_DIR, symbol3)
    symbol4_txt = os.path.join(SYMBOL_DIR, symbol4)
    start_date = request.args.get("start_date", "2001-01-01")
    today = datetime.now()
    end_date = request.args.get("end_date", (today - timedelta(days=1)).strftime('%Y-%m-%d'))
    db = get_db()
    (open_signals1, query1) = invest_signal.direct_open_order(db, symbol1_txt, start_date, end_date)
    (open_signals2, query2) = invest_signal.direct_open_order(db, symbol2_txt, start_date, end_date)
    (open_signals3, query3) = invest_signal.direct_open_order(db, symbol3_txt, start_date, end_date)
    (open_signals4, query4) = invest_signal.direct_open_order(db, symbol4_txt, start_date, end_date)
    content_title = "Open Signal"
    return render_template('open_signal.html'
                        , content_title=content_title
                        , start_date=start_date
                        , end_date=end_date
                        , symbol1=symbol1
                        , symbol2=symbol2
                        , symbol3=symbol3
                        , symbol4=symbol4
                        , open_signals1=open_signals1
                        , open_signals2=open_signals2
                        , open_signals3=open_signals3
                        , open_signals4=open_signals4
                        , query1=query1
                        , query2=query2
                        , query3=query3
                        , query4=query4
                        )

@app.route('/close_signal', methods=['GET', 'POST'])
def close_signal():
    content_title = 'Close Signal'
    if request.method == "POST":
        symbol = request.form.get("symbol", "")
        position = request.form.get("position", "")
        open_price = request.form.get("open_price", "")
        bitmex_flg = request.form.get("checkbox_bitmex", "")
        close_order = invest_signal.direct_close_order(get_db(), symbol, position, open_price, bitmex_flg)
        if close_order.get('ordertype') is not None:
            close_order_type = close_order['ordertype']
            close_order_price = close_order['orderprice']
        else:
            close_order_type = ""
            close_order_price = 0
        return render_template('close_signal.html'
                        , content_title=content_title
                        , symbol=symbol
                        , position=position
                        , open_price=open_price
                        , bitmex_flg=bitmex_flg
                        , close_order_type=close_order_type
                        , close_order_price=close_order_price)
    else:
        return render_template('close_signal.html'
                        , content_title=content_title)

@app.route('/backtest_history', methods=['GET', 'POST'])
def backtest_history():
    default_end_date = datetime.today().strftime('%Y-%m-%d')
    default_start_date = (datetime.today() - relativedelta(months=3)).strftime('%Y-%m-%d') #今日の3ヶ月前
    if request.method == 'POST':
        symbol = request.form.get("symbol", "")
        start_date = request.form.get("start_date", default_start_date)
        end_date = request.form.get("end_date", default_end_date)
    else:
        symbol = request.args.get("symbol", "")
        start_date = request.args.get("start_date", default_start_date)
        end_date = request.args.get("end_date", default_end_date)
    content_title = u"Backtest Data".format(symbol=symbol, start_date=start_date, end_date=end_date)
    query = BACKTEST_HISTORY_QUERY.format(symbol=symbol, start_date=start_date, end_date=end_date)
    rv = query_db(query)
    return render_template('backtest_history_table.html'
                        , content_title=content_title
                        , symbol=symbol
                        , start_date=start_date
                        , end_date=end_date
                        , rv=rv
                        , query=query)

@app.route('/ohlcv_daily', methods=['GET', 'POST'])
def ohlcv_daily():
    default_end_date = datetime.today().strftime('%Y-%m-%d')
    default_start_date = (datetime.today() - relativedelta(months=3)).strftime('%Y-%m-%d') #今日の3ヶ月前
    if request.method == 'POST':
        symbol = request.form.get("symbol", "")
        start_date = request.form.get("start_date", default_start_date)
        end_date = request.form.get("end_date", default_end_date)
    else:
        symbol = request.args.get("symbol", "")
        start_date = request.args.get("start_date", default_start_date)
        end_date = request.args.get("end_date", default_end_date)
    content_title = u"OHLCV Daily".format(symbol=symbol)
    query = OHLCV_DAILY_QUERY.format(symbol=symbol, start_date=start_date, end_date=end_date)
    rv = query_db(query)
    return render_template('ohlcv_table.html'
                        , content_title=content_title
                        , symbol=symbol
                        , start_date=start_date
                        , end_date=end_date
                        , rv=rv
                        , query=query)

@app.route('/backtest_summary', methods=['GET', 'POST'])
def backtest_summary():
    default_regist_date = datetime.today().strftime('%Y-%m-%d') #今日
    default_end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    if request.method == 'POST':
        regist_date = request.form.get("regist_date", default_regist_date)
        end_date = request.form.get("end_date", default_end_date)
    else:
        regist_date = request.args.get("regist_date", default_regist_date)
        end_date = request.args.get("end_date", default_end_date)
    start_date = '2001-01-01'
    start_date_3month = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(months=3)).strftime("%Y-%m-%d")
    start_date_1year = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(years=1)).strftime("%Y-%m-%d")
    start_date_3year = (datetime.strptime(end_date, "%Y-%m-%d")- relativedelta(years=3)).strftime("%Y-%m-%d")
    start_date_15year = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(years=15)).strftime("%Y-%m-%d")
    content_title = u"Backtest Summary"
    query = BACKTEST_SUMMARY_QUERY.format(start_date=start_date
                                        , start_date_3month=start_date_3month
                                        , start_date_1year=start_date_1year
                                        , start_date_3year=start_date_3year
                                        , start_date_15year=start_date_15year
                                        , regist_date=regist_date
                                        , end_date=end_date)
    rv = query_db(query)
    return render_template('backtest_summary.html'
                        , content_title=content_title
                        , start_date=start_date
                        , start_date_3month=start_date_3month
                        , start_date_1year=start_date_1year
                        , start_date_3year=start_date_3year
                        , start_date_15year=start_date_15year
                        , regist_date=regist_date
                        , end_date=end_date
                        , rv=rv
                        , query=query
                        )

@app.route('/symbols', methods=['GET'])
def symbols():
    symbol1 = request.args.get("symbol1", "Nikkei225_TOPIX500.txt")
    symbol2 = request.args.get("symbol2", "bitmex_xbtusd.txt")
    symbol3 = request.args.get("symbol3", "bitmex_ethusd.txt")
    symbol4 = request.args.get("symbol4", "minkabu_fx_gbpjpy.txt")
    symbol1_txt = os.path.join(SYMBOL_DIR, symbol1)
    symbol2_txt = os.path.join(SYMBOL_DIR, symbol2)
    symbol3_txt = os.path.join(SYMBOL_DIR, symbol3)
    symbol4_txt = os.path.join(SYMBOL_DIR, symbol4)
    symbol1_list = sy.get_symbols(symbol1_txt)
    symbol2_list = sy.get_symbols(symbol2_txt)
    symbol3_list = sy.get_symbols(symbol3_txt)
    symbol4_list = sy.get_symbols(symbol4_txt)
    content_title = u"Symbol List"
    return render_template('symbols.html'
                        , content_title=content_title
                        , symbol1=symbol1
                        , symbol2=symbol2
                        , symbol3=symbol3
                        , symbol4=symbol4
                        , symbol1_list=symbol1_list
                        , symbol2_list=symbol2_list
                        , symbol3_list=symbol3_list
                        , symbol4_list=symbol4_list
                        )

@app.route('/tables', methods=['GET'])
def table():
    return render_template('tables.html')

if __name__ == "__main__":
     app.run()
