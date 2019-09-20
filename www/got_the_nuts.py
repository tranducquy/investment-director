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
,bh.leverage
,mot1.ordertype_name
,mot2.ordertype_name
,mot3.ordertype_name
,mos.orderstatus_name
,mpt.positiontype_name
from backtest_history as bh
left outer join m_strategy as ms
on bh.strategy_id = ms.strategy_id
left outer join m_ordertype as mot1
on bh.order_type = mot1.ordertype_id
left outer join m_ordertype as mot2
on bh.call_order_type = mot2.ordertype_id
left outer join m_ordertype as mot3
on bh.execution_order_type = mot3.ordertype_id
left outer join m_orderstatus as mos
on bh.execution_order_status = mos.orderstatus_id
left outer join m_positiontype as mpt
on bh.position = mpt.positiontype_id
where 
bh.symbol = '{symbol}'
and bh.strategy_id = {strategy_id}
and bh.strategy_option = '{strategy_option}'
and bh.business_date between '{start_date}' and '{end_date}'
order by bh.business_date
"""

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
,r.drawdown as 最大ドローダウン
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
from backtest_result as r
inner join m_strategy as ms 
on r.strategy_id = ms.strategy_id
where 0 = 0 
and r.regist_date = '{regist_date}'
order by r.rate_of_return desc
"""

PROFIT_RATE_PER_YEAR = """
select
 symbol
,strategy_id
,strategy_option
,substr(business_date, 1, 4) as YYYY
,sum(profit_rate) as 利益率合計
from backtest_history
where symbol = ''
and execution_order_type in (5, 6)
group by symbol, strategy_id, strategy_option, substr(business_date, 1, 4)
"""

PROFIT_RATE_PER_YEAR_LONG_SHORT = """
select
 symbol
,strategy_id
,strategy_option
,substr(business_date, 1, 4) as YYYY
,case
  when execution_order_type = 5 then 'long'
  when execution_order_type = 6 then 'short'
 end as 注文タイプ
,sum(profit_rate) as 利益率合計
from backtest_history
where symbol = ''
and execution_order_type in (5, 6)
group by symbol, strategy_id, strategy_option, substr(business_date, 1, 4), execution_order_type
"""

PROFIT_RATE_PER_MONTH = """
select
 symbol
,strategy_id
,strategy_option
,substr(business_date, 1, 7) as YYYY-MM
,sum(profit_rate) as 利益率合計
from backtest_history
where symbol = ''
and business_date between '{start_date_3year}' and '{end_date}'
and execution_order_type in (5, 6)
group by symbol, strategy_id, strategy_option, substr(business_date, 1, 7)
"""

PROFIT_RATE_PER_MONTH_LONG_SHORT = """
select
 symbol
,strategy_id
,strategy_option
,substr(business_date, 1, 7) as YYYY-MM
,case
  when execution_order_type = 5 then 'long'
  when execution_order_type = 6 then 'short'
 end as 注文タイプ
,sum(profit_rate) as 利益率合計
from backtest_history
where symbol = ''
and business_date between '{start_date_3year}' and '{end_date}'
and execution_order_type in (5, 6)
group by symbol, strategy_id, strategy_option, substr(business_date, 1, 7), execution_order_type
"""

BOLLINGERBAND_DAILYTRAIL_LIST = """
select
 symbol
,sma
,sigma1
from bollingerband_dailytrail
"""

OPEN_SIGNAL = """
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
where 0 = 0
and r.rate_of_return > 0
and (
    (order_table.order_type = 1 and (r.long_profit_rate_3month > 15 or r.long_profit_rate_1year > 15)) 
    or 
    (order_table.order_type = 2 and (r.short_profit_rate_3month > 15 or r.short_profit_rate_1year > 15))
)
and (r.profit_rate_3month > 5 and r.profit_rate_1year > 15 and r.profit_rate_3year > 45 and r.profit_rate_15year > 225)
and r.symbol in ({symbols})
order by r.profit_rate_1year desc
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
                 "5202.T"
                ,"6141.T"
                ,"6728.T"
                ,"6753.T"
                ,"9107.T"
                ]
    symbols_mindrawdown = [
                 "7616.T"
                ,"8136.T"
                ,"8904.T"
                ]
    return render_template('index.html'
                            , symbols=symbols
                            , symbols_mindrawdown=symbols_mindrawdown
                            , index=index
                            )

@app.route("/index")
#@auth.login_required
def index2():
    index="active"
    symbols = [
                 "5202.T"
                ,"6141.T"
                ,"6728.T"
                ,"6753.T"
                ,"9107.T"
                ]
    symbols_mindrawdown = [
                 "7616.T"
                ,"8136.T"
                ,"8904.T"
                ]
    return render_template('index.html'
                            , symbols=symbols
                            , symbols_mindrawdown=symbols_mindrawdown
                            , index=index
                            )

@app.route('/open_signal', methods=['GET'])
#@auth.login_required
def open_signal():
    signal="active"
    symbol1 = request.args.get("symbol", "Nikkei225_TOPIX_20190918.txt")
    symbol2 = request.args.get("symbol", "bitmex.txt")
    symbol3 = request.args.get("symbol", "minkabu_fx.txt")
    symbol1_txt = os.path.join(SYMBOL_DIR, symbol1)
    symbol2_txt = os.path.join(SYMBOL_DIR, symbol2)
    symbol3_txt = os.path.join(SYMBOL_DIR, symbol3)
    start_date = request.args.get("start_date", "2001-01-01")
    today = datetime.now()
    end_date = request.args.get("end_date", (today - timedelta(days=1)).strftime('%Y-%m-%d'))
    db = get_db()
    (open_signals1, query1) = invest_signal.direct_open_order(db, symbol1_txt, start_date, end_date)
    (open_signals2, query2) = invest_signal.direct_open_order(db, symbol2_txt, start_date, end_date)
    (open_signals3, query3) = invest_signal.direct_open_order(db, symbol3_txt, start_date, end_date)
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
                        , open_signals1=open_signals1
                        , open_signals2=open_signals2
                        , open_signals3=open_signals3
                        , query1=query1
                        , query2=query2
                        , query3=query3
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
    from bollingerband_dailytrail
    where symbol = '{symbol}'
    """.format(symbol=symbol)
    rv = query_db(query)
    if rv:
        strategy_option = "SMA{sma}SD{sd:.1f}".format(sma=rv[0][1], sd=rv[0][2])
    else:
        strategy_option = "SMA3SD1.0"
    return strategy_option

@app.route('/backtest_history', methods=['GET', 'POST'])
#@auth.login_required
def backtest_history():
    backtest_history="active"
    default_end_date = datetime.today().strftime('%Y-%m-%d')
    default_start_date = (datetime.today() - relativedelta(months=3)).strftime('%Y-%m-%d') #今日の3ヶ月前
    default_strategy_id = 1
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

def get_dates():
    regist_date = datetime.today().strftime('%Y-%m-%d') #今日
    end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = '2001-01-01'
    start_date_3month = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(months=3)).strftime("%Y-%m-%d")
    start_date_1year = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(years=1)).strftime("%Y-%m-%d")
    start_date_3year = (datetime.strptime(end_date, "%Y-%m-%d")- relativedelta(years=3)).strftime("%Y-%m-%d")
    start_date_15year = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(years=15)).strftime("%Y-%m-%d")
    return (
              regist_date
            , end_date 
            , start_date
            , start_date_3month
            , start_date_1year
            , start_date_3year
            , start_date_15year
            )

@app.route('/backtest_summary', methods=['GET', 'POST'])
#@auth.login_required
def backtest_summary():
    backtest_summary='backtest_summary'
    header_title = u"Backtest Summary"
    content_title = u"Backtest Summary"
    (regist_date , end_date , start_date , start_date_3month , start_date_1year , start_date_3year , start_date_15year) = get_dates()
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
    symbol1 = request.args.get("symbol1", "Nikkei225_TOPIX_20190918.txt")
    symbol2 = request.args.get("symbol2", "bitmex.txt")
    symbol3 = request.args.get("symbol3", "minkabu_fx.txt")
    symbol1_txt = os.path.join(SYMBOL_DIR, symbol1)
    symbol2_txt = os.path.join(SYMBOL_DIR, symbol2)
    symbol3_txt = os.path.join(SYMBOL_DIR, symbol3)
    symbol1_list = sy.get_symbols(symbol1_txt)
    symbol2_list = sy.get_symbols(symbol2_txt)
    symbol3_list = sy.get_symbols(symbol3_txt)
    header_title = u"Symbol List"
    content_title = u"Symbol List"
    return render_template('symbols.html'
                        , symbols=symbols
                        , header_title=header_title
                        , content_title=content_title
                        , symbol1=symbol1
                        , symbol2=symbol2
                        , symbol3=symbol3
                        , symbol1_list=symbol1_list
                        , symbol2_list=symbol2_list
                        , symbol3_list=symbol3_list
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
        q = request.args.get("q", "")
        query = ""
        if q == "backtest_result":
            (regist_date , end_date , start_date , start_date_3month , start_date_1year , start_date_3year , start_date_15year) = get_dates()
            query = BACKTEST_SUMMARY_QUERY.format(start_date=start_date
                                                , start_date_3month=start_date_3month
                                                , start_date_1year=start_date_1year
                                                , start_date_3year=start_date_3year
                                                , start_date_15year=start_date_15year
                                                , regist_date=regist_date
                                                , end_date=end_date
                                                , backtest_summary=backtest_summary)
        elif q == "profit_rate_per_year":
            query = PROFIT_RATE_PER_YEAR
        elif q == "profit_rate_per_year_long_short":
            query = PROFIT_RATE_PER_YEAR_LONG_SHORT
        elif q == "profit_rate_per_month":
            (regist_date , end_date , start_date , start_date_3month , start_date_1year , start_date_3year , start_date_15year) = get_dates()
            query = PROFIT_RATE_PER_MONTH.format(start_date_3year=start_date_3year, end_date=end_date)
        elif q == "profit_rate_per_month_long_short":
            (regist_date , end_date , start_date , start_date_3month , start_date_1year , start_date_3year , start_date_15year) = get_dates()
            query = PROFIT_RATE_PER_MONTH_LONG_SHORT.format(start_date_3year=start_date_3year, end_date=end_date)
        elif q == "strategy_list":
            query = BOLLINGERBAND_DAILYTRAIL_LIST
        elif q == "open_signal":
            query = OPEN_SIGNAL
        elif q == "":
            pass
        return render_template('db_access.html'
                            ,db_access=db_access
                            ,header_title=header_title
                            ,query=query
                            )

@app.route('/tradingview1')
#@auth.login_required
def tradingview1():
    tradingview = "active"
    return render_template('tradingview1.html' ,tradingview=tradingview)

@app.route('/tradingview2')
#@auth.login_required
def tradingview2():
    tradingview = "active"
    return render_template('tradingview2.html' ,tradingview=tradingview)

if __name__ == "__main__":
     app.run()
