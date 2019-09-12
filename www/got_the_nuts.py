# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from datetime import timedelta 
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, g, request
from flask_httpauth import HTTPDigestAuth
import random
import sqlite3
import subprocess
import invest_signal
import symbol as sy

app = Flask(__name__)
seed = datetime.now()
app.config['SECRET_KEY'] = seed.strftime('%M%s%d%Y%m%H')
auth = HTTPDigestAuth()
users = {
    "takeyukitanaka": "password1",
    "vip": "vipuser1"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

DATABASE = '/usr/local/investment-director/market-history.db'
SYMBOL_DIR = '/usr/local/investment-director/symbol/'
BACKTEST_HISTORY_QUERY = u"""
                    select 
                     bh.symbol
                    ,ms.strategy_name
                    ,bh.strategy_option
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
                    where 
                    bh.symbol = '{symbol}'
                    and bh.strategy_id = {strategy_id}
                    and bh.strategy_option = '{strategy_option}'
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
                    ,r.strategy_option
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
                        ,strategy_option
                        ,sum(profit_rate) as profit_rate_sum
                        ,count(business_date) as count
                        from backtest_history
                        where business_date between '{start_date_3month}' and '{end_date}'
                        group by symbol, strategy_id, strategy_option
                    ) m3
                    on r.symbol = m3.symbol and r.strategy_id = m3.strategy_id and r.strategy_option = m3.strategy_option
                    left outer join (
                        select
                         symbol
                        ,strategy_id
                        ,strategy_option
                        ,sum(profit_rate) as profit_rate_sum
                        from backtest_history
                        where business_date between '{start_date_1year}' and '{end_date}'
                        group by symbol, strategy_id, strategy_option
                    ) y1
                    on r.symbol = y1.symbol and r.strategy_id = y1.strategy_id and r.strategy_option = y1.strategy_option
                    left outer join (
                        select
                        symbol
                        ,strategy_id
                        ,strategy_option
                        ,sum(profit_rate) as profit_rate_sum
                        from backtest_history
                        where business_date between '{start_date_3year}' and '{end_date}'
                        group by symbol, strategy_id, strategy_option
                    ) y3
                    on r.symbol = y3.symbol and r.strategy_id = y3.strategy_id and r.strategy_option = y3.strategy_option
                    left outer join (
                        select
                        symbol
                        ,strategy_id
                        ,strategy_option
                        ,sum(profit_rate) as profit_rate_sum
                        from backtest_history
                        where business_date between '{start_date_15year}' and '{end_date}'
                        group by symbol, strategy_id, strategy_option
                    ) y15
                    on r.symbol = y15.symbol and r.strategy_id = y15.strategy_id and r.strategy_option = y15.strategy_option
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
#@auth.login_required
def index():
    index="active"
    symbols = [
                 "9107.T"
                ,"6728.T"
                ,"5202.T"
                ,"6141.T"
                ,"6753.T"
                ]
    return render_template('index.html'
                            , symbols=symbols
                            , index=index
                            )

@app.route("/index")
#@auth.login_required
def index2():
    index="active"
    symbols = [
                 "9107.T"
                ,"6728.T"
                ,"5202.T"
                ,"6141.T"
                ,"6753.T"
                ]
    return render_template('index.html'
                            , symbols=symbols
                            , index=index
                            )

@app.route('/open_signal', methods=['GET'])
#@auth.login_required
def open_signal():
    signal="active"
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
    header_title = "Open Signal"
    content_title = "Open Signal"
    return render_template('open_signal.html'
                        , signal=signal
                        , header_title=header_title
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
#@auth.login_required
def close_signal():
    signal="active"
    content_title = 'Close Signal'
    if request.method == "POST":
        symbol = request.form.get("symbol", "")
        position = request.form.get("position", "")
        open_price = request.form.get("open_price", "")
        bitmex_flg = request.form.get("checkbox_bitmex", "")
        firstday_flg = request.form.get("checkbox_firstday", "")
        close_order = invest_signal.direct_close_order(get_db(), symbol, position, open_price, bitmex_flg, firstday_flg)
        if close_order.get('ordertype') is not None:
            close_order_type = close_order['ordertype']
            close_order_price = close_order['orderprice']
        else:
            close_order_type = ""
            close_order_price = 0
        header_title = '{symbol} Close Signal'.format(symbol=symbol)
        return render_template('close_signal.html'
                        , signal=signal
                        , header_title=header_title
                        , content_title=content_title
                        , symbol=symbol
                        , position=position
                        , open_price=open_price
                        , bitmex_flg=bitmex_flg
                        , firstday_flg=firstday_flg
                        , close_order_type=close_order_type
                        , close_order_price=close_order_price)
    else:
        return render_template('close_signal.html'
                        , signal=signal
                        , content_title=content_title)

def get_bb_strategy_option(symbol):
    query = """
    select
    symbol
    ,sma
    ,sigma1
    from bollingerband_newvalue
    where symbol = '{symbol}'
    """.format(symbol=symbol)
    rv = query_db(query)
    if rv:
        strategy_option = "SMA{sma}SD{sd:.1f}".format(sma=rv[0][1], sd=rv[0][2])
    else:
        strategy_option = ""
    return strategy_option

@app.route('/backtest_history', methods=['GET', 'POST'])
#@auth.login_required
def backtest_history():
    backtest_history="active"
    default_end_date = datetime.today().strftime('%Y-%m-%d')
    default_start_date = (datetime.today() - relativedelta(months=3)).strftime('%Y-%m-%d') #今日の3ヶ月前
    default_strategy_id = 1
    default_strategy_option = 'SMA3SD1.0'
    if request.method == 'POST':
        symbol = request.form.get("symbol", "")
        start_date = request.form.get("start_date", default_start_date)
        end_date = request.form.get("end_date", default_end_date)
        strategy_id = request.form.get("strategy_id", default_strategy_id)
        strategy_option = request.form.get("strategy_option", "")
        if strategy_option == "":
            strategy_option = get_bb_strategy_option(symbol)
    else:
        symbol = request.args.get("symbol", "")
        start_date = request.args.get("start_date", default_start_date)
        end_date = request.args.get("end_date", default_end_date)
        strategy_id = request.args.get("strategy_id", default_strategy_id)
        strategy_option = request.args.get("strategy_option", get_bb_strategy_option(symbol))
    header_title = u"{symbol} {start_date} {end_date} Backtest Data".format(symbol=symbol, start_date=start_date, end_date=end_date)
    content_title = u"Backtest Data".format(symbol=symbol, start_date=start_date, end_date=end_date)
    query = BACKTEST_HISTORY_QUERY.format(symbol=symbol
                                            , start_date=start_date
                                            , end_date=end_date
                                            , strategy_id=strategy_id
                                            , strategy_option=strategy_option)
    rv = query_db(query)
    return render_template('backtest_history_table.html'
                        , backtest_history=backtest_history
                        , header_title=header_title
                        , content_title=content_title
                        , symbol=symbol
                        , strategy_id=strategy_id
                        , strategy_option=strategy_option
                        , start_date=start_date
                        , end_date=end_date
                        , rv=rv
                        , query=query)

@app.route('/ohlcv_daily', methods=['GET', 'POST'])
#@auth.login_required
def ohlcv_daily():
    ohlcv_daily="active"
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
    header_title = u"{symbol} {start_date} {end_date} OHLCV Daily".format(symbol=symbol, start_date=start_date, end_date=end_date)
    content_title = u"OHLCV Daily".format(symbol=symbol)
    query = OHLCV_DAILY_QUERY.format(symbol=symbol, start_date=start_date, end_date=end_date)
    rv = query_db(query)
    return render_template('ohlcv_table.html'
                        , ohlcv_daily=ohlcv_daily
                        , header_title=header_title
                        , content_title=content_title
                        , symbol=symbol
                        , start_date=start_date
                        , end_date=end_date
                        , rv=rv
                        , query=query)

@app.route('/backtest_summary', methods=['GET', 'POST'])
#@auth.login_required
def backtest_summary():
    backtest_summary='backtest_summary'
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
    header_title = u"Backtest Summary"
    content_title = u"Backtest Summary"
    query = BACKTEST_SUMMARY_QUERY.format(start_date=start_date
                                        , start_date_3month=start_date_3month
                                        , start_date_1year=start_date_1year
                                        , start_date_3year=start_date_3year
                                        , start_date_15year=start_date_15year
                                        , regist_date=regist_date
                                        , end_date=end_date
                                        , backtest_summary=backtest_summary)
    rv = query_db(query)
    return render_template('backtest_summary.html'
                        , header_title=header_title
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
                        , backtest_summary=backtest_summary
                        )

@app.route('/symbols', methods=['GET'])
#@auth.login_required
def symbols():
    symbols = "active"
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
    header_title = u"Symbol List"
    content_title = u"Symbol List"
    return render_template('symbols.html'
                        , symbols=symbols
                        , header_title=header_title
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

@app.route('/crontab')
#@auth.login_required
def crontab():
    crontab = "active"
    crontab_command = sy.get_symbols('/usr/local/investment-director/crontab/crontab')
    header_title = u"crontab"
    return render_template('crontab.html'
                        , header_title=header_title
                        , crontab=crontab
                        , crontab_command=crontab_command)

@app.route('/db_access', methods=['GET', 'POST'])
#@auth.login_required
def db_access():
    db_access = "active"
    header_title="DB ACCESS"
    if request.method == 'POST':
        try:
            query = request.form.get("query", "")
            cur = get_db().execute(query)
            ds = cur.fetchall()
            ds_header = [description[0] for description in cur.description]
            cur.close()
            return render_template('db_access.html'
                                ,db_access=db_access
                                ,header_title=header_title
                                ,query=query
                                ,ds=ds
                                ,ds_header=ds_header
                                )
        except Exception as err:
            return render_template('db_access.html'
                            ,db_access=db_access
                            ,header_title=header_title
                            ,query=query
                            ,errmsg=err
                            )
    else:
        return render_template('db_access.html'
                            ,db_access=db_access
                            ,header_title=header_title
                            )

@app.route('/tradingview')
#@auth.login_required
def tradingview():
    tradingview = "active"
    return render_template('tradingview.html'
                            ,tradingview=tradingview
                            )

if __name__ == "__main__":
     app.run()
