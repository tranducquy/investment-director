
import sys
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import common
import my_logger
import quotes
from butler import bollingerband
from butler import bollingerband_and_volume_bollingerband
from butler import bollingerband_and_volume_moving_average
from butler import new_value_and_moving_average_and_volume_moving_average
import tick

s = my_logger.Logger()
logger = s.myLogger()

def get_last_backtestdate(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    #バックテストの最終登録日を取得
    c.execute("""
    select
    max(regist_date)
    from backtest_result""")
    max_date = c.fetchone()
    conn.close()
    return max_date[0]

def get_symbols(db, regist_date, today, end_date):
    #3ヶ月、1,3,15年のバックテストで利益の出ている銘柄のみ探す
    start_date_3month = (today - relativedelta(months=3)).strftime("%Y-%m-%d")
    start_date_1year = (today - relativedelta(years=1)).strftime("%Y-%m-%d")
    start_date_3year = (today - relativedelta(years=3)).strftime("%Y-%m-%d")
    start_date_15year = (today - relativedelta(years=15)).strftime("%Y-%m-%d")

    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql = """
    select
     m3.symbol
    ,m3.strategy
    ,m3.regist_date
    ,m3.rate_of_return as 騰落率3か月
    ,y1.rate_of_return as 騰落率1年
    ,y3.rate_of_return as 騰落率3年
    ,y15.rate_of_return as 騰落率15年
    ,m3.expected_rate as トレード当たりの期待値3か月
    ,y1.expected_rate as トレード当たりの期待値1年
    ,y3.expected_rate as トレード当たりの期待値3年
    ,y15.expected_rate as トレード当たりの期待値15年
    ,m3.expected_rate_per_1day as トレード1日当たりの期待値3か月
    ,y1.expected_rate_per_1day as トレード1日当たりの期待値1年
    ,y3.expected_rate_per_1day as トレード1日当たりの期待値3年
    ,y15.expected_rate_per_1day as トレード1日当たりの期待値15年
    ,m3.average_period_per_trade as 平均取引期間3か月
    ,y1.average_period_per_trade as 平均取引期間1年
    ,y3.average_period_per_trade as 平均取引期間3年
    ,y15.average_period_per_trade as 平均取引期間15年
    ,m3.win_rate as 勝率3か月
    ,y1.win_rate as 勝率1年
    ,y3.win_rate as 勝率3年
    ,y15.win_rate as 勝率15年
    ,m3.long_expected_rate as 期待利益率long3か月
    ,y1.long_expected_rate as 期待利益率long1年
    ,y3.long_expected_rate as 期待利益率long3年
    ,y15.long_expected_rate as 期待利益率long15年
    ,m3.long_expected_rate_per_1day as 一日当たりの期待利益率long3か月
    ,y1.long_expected_rate_per_1day as 一日当たりの期待利益率long1年
    ,y3.long_expected_rate_per_1day as 一日当たりの期待利益率long3年
    ,y15.long_expected_rate_per_1day as 一日当たりの期待利益率long15年
    ,m3.long_win_count+m3.long_loss_count as 取引数long3か月
    ,y1.long_win_count+y1.long_loss_count as 取引数long1年
    ,y3.long_win_count+y3.long_loss_count as 取引数long3年
    ,y15.long_win_count+y15.long_loss_count as 取引数long15年
    ,m3.short_expected_rate as 期待利益率short3か月
    ,y1.short_expected_rate as 期待利益率short1年
    ,y3.short_expected_rate as 期待利益率short3年
    ,y15.short_expected_rate as 期待利益率short15年
    ,m3.short_expected_rate_per_1day as 一日当たりの期待利益率short3か月
    ,y1.short_expected_rate_per_1day as 一日当たりの期待利益率short1年
    ,y3.short_expected_rate_per_1day as 一日当たりの期待利益率short3年
    ,y15.short_expected_rate_per_1day as 一日当たりの期待利益率short15年
    ,m3.short_win_count+m3.short_loss_count as 取引数short3か月
    ,y1.short_win_count+y1.short_loss_count as 取引数short1年
    ,y3.short_win_count+y3.short_loss_count as 取引数short3年
    ,y15.short_win_count+y15.short_loss_count as 取引数short15年
    ,m3.win_count+m3.loss_count as 取引数3か月
    ,y1.win_count+y1.loss_count as 取引数1年
    ,y3.win_count+y3.loss_count as 取引数3年
    ,y15.win_count+y15.loss_count as 取引数15年
   from backtest_result m3
   left outer join (
   select
    *
   from backtest_result
   where start_date = '%s'
   and end_date = '%s'
   and backtest_period > 300*1
   and rate_of_return > 0
   ) y1
   on m3.symbol = y1.symbol and m3.strategy = y1.strategy and m3.rate_of_return < y1.rate_of_return
   left outer join (
   select
    *
   from backtest_result
   where start_date = '%s'
   and end_date = '%s'
   and backtest_period > 300*3
   and rate_of_return > 0
   ) y3
   on m3.symbol = y3.symbol and m3.strategy = y3.strategy and y1.rate_of_return < y3.rate_of_return
   left outer join (
   select
    *
   from backtest_result
   where start_date = '%s'
   and end_date = '%s'
   and backtest_period > 300*15
   and rate_of_return > 0
   ) y15
   on m3.symbol = y15.symbol and m3.strategy = y15.strategy and y3.rate_of_return < y15.rate_of_return
   where m3.start_date = '%s'
   and m3.end_date = '%s'
   and m3.rate_of_return > 0
   and m3.rate_of_return < y1.rate_of_return
   and y1.rate_of_return < y3.rate_of_return
   and y3.rate_of_return < y15.rate_of_return
   order by m3.rate_of_return desc
       """ % (
             start_date_1year, end_date
           , start_date_3year, end_date
           , start_date_15year, end_date
           , start_date_3month, end_date
           )
    logger.info(sql)
    c.execute(sql)
    symbols = c.fetchall()
    conn.close()
    return symbols

if __name__ == '__main__':
    args = sys.argv
    conf = common.read_conf()
    s = my_logger.Logger()
    logger = s.myLogger(conf['logger'])
    logger.info('investment-director.')
    #symbol_txt = conf['symbol']
    dbfile = conf['dbfile']

    max_regist_date = get_last_backtestdate(dbfile)
    today = datetime.strptime(max_regist_date, "%Y-%m-%d")
    start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    symbols = get_symbols(dbfile, max_regist_date, today, end_date)

    #ポジション無し
    for s in symbols:
        symbol = s[0]
        strategy = s[1]
        regist_date = s[2]
        t = tick.get_tick(symbol)
        if strategy == '新値1日_移動平均4日_出来高移動平均20日':
            q = quotes.Quotes(dbfile, symbol, start_date, end_date, 4, 1, 20, 1)
            butler = new_value_and_moving_average_and_volume_moving_average.Butler(t, 1)
        elif strategy == '超短期ボリンジャー5日_1.20倍_決済差額0.00':
            q = quotes.Quotes(dbfile, symbol, start_date, end_date, 5, 1.2)
            butler = bollingerband.Butler(t, 1, 0.0001)
        elif strategy == '超短期ボリンジャー3日_1.00倍_0.00_出来高ボリンジャー14日_2.00倍':
            q = quotes.Quotes(dbfile, symbol, start_date, end_date, 3, 1.0, 14, 2.0)
            butler = bollingerband_and_volume_bollingerband.Butler(t, 1, 0.0001)
        elif strategy == '超短期ボリンジャー3日_1.00倍_0.00':
            q = quotes.Quotes(dbfile, symbol, start_date, end_date, 3, 1.0)
            butler = bollingerband.Butler(t, 1, 0.0001)
        else:
            continue
        for idx, high in enumerate(q.quotes['high']):
            business_date = q.quotes['business_date'][idx]
            if business_date == max(q.quotes['business_date']):
                if butler.check_open_long(q, idx):
                    price = butler.create_order_stop_market_long(q, idx)
                    logger.info("[%s]に逆指値でlongうて(最終営業日%s) 逆指値:[%f] (%s)" % (symbol, business_date, price, strategy))
                elif butler.check_open_short(q, idx):
                    price = butler.create_order_stop_market_short(q, idx)
                    logger.info("[%s]に逆指値でshortうて(最終営業日%s) 逆指値:[%f] (%s)" % (symbol, business_date, price, strategy))
    
    #TODO:ポジション有り
