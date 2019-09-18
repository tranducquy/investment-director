# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy
import my_logger
import my_lock
from my_db import MyDB

class BacktestDumper():
    def __init__(self, logger=None):
        if logger is None:
            self.logger = my_logger.Logger().myLogger()
        else:
            self.logger = logger

    def save_simulate_result(
                         self
                        ,symbol
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
            conn = MyDB().get_db()
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
                self.logger.error(err)
        finally:
            if conn: 
                conn.commit()
                conn.close
            my_lock.lock.release()
    
    def _check_float(self, num):
        if ( num is None or numpy.isnan(num)):
            return 0.00
        else:
            return float(num)
    
    def make_history(
                  self
                , symbol
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
            , self._check_float(quotes.quotes['open'][idx])
            , self._check_float(quotes.quotes['high'][idx])
            , self._check_float(quotes.quotes['low'][idx])
            , self._check_float(quotes.quotes['close'][idx])
            , vol
            , self._check_float(quotes.sma[idx])
            , self._check_float(quotes.upper_ev_sigma[idx])
            , self._check_float(quotes.lower_ev_sigma[idx])
            , self._check_float(quotes.upper_ev2_sigma[idx])
            , self._check_float(quotes.lower_ev2_sigma[idx])
            , 0.00 # vol_sma
            , 0.00 # vol_upper_sigma1
            , 0.00 # vol_lower_sigma1
            , order_info['create_date']
            , order_info['order_type']
            , self._check_float(order_info['vol'])
            , self._check_float(order_info['price'])
            , call_order_info['order_date']
            , call_order_info['order_type']
            , self._check_float(call_order_info['vol'])
            , self._check_float(call_order_info['price'])
            , execution_order_info['close_order_date']
            , execution_order_info['order_type']
            , execution_order_info['order_status']
            , self._check_float(execution_order_info['vol'])
            , self._check_float(execution_order_info['price'])
            , position
            , self._check_float(cash)
            , self._check_float(pos_vol)
            , self._check_float(pos_price)
            , self._check_float(total_value)
            , self._check_float(trade_perfomance['profit_value'])
            , self._check_float(trade_perfomance['profit_rate'])
        )
        return t
    
    def save_history(self, backtest_history):
        try:
            my_lock.lock.acquire()
            conn = MyDB().get_db()
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
                self.logger.error(err)
        finally:
            if conn: 
                conn.commit()
                conn.close
            my_lock.lock.release()
    
    def make_summary_msg(self, symbol, strategy_id, strategy_option, title, summary, quotes):
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
        self.save_simulate_result(
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

    def get_dates(self):
        end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        start_date = '2001-01-01'
        start_date_3month = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(months=3)).strftime("%Y-%m-%d")
        start_date_1year = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(years=1)).strftime("%Y-%m-%d")
        start_date_3year = (datetime.strptime(end_date, "%Y-%m-%d")- relativedelta(years=3)).strftime("%Y-%m-%d")
        start_date_15year = (datetime.strptime(end_date, "%Y-%m-%d") - relativedelta(years=15)).strftime("%Y-%m-%d")
        return (
                 end_date 
                , start_date
                , start_date_3month
                , start_date_1year
                , start_date_3year
                , start_date_15year
                )

    def update_expected_rate(self, symbols):
        self.logger.info("update_expected_rate()")
        (end_date , start_date, start_date_3month , start_date_1year , start_date_3year , start_date_15year) = self.get_dates()
        #backtest_result table取得
        conn = MyDB().get_db()
        c = conn.cursor()
        c.execute("""
        select
         symbol
        ,strategy_id
        ,strategy_option
        from backtest_result
        where symbol in ({symbols})
        """.format(symbols=', '.join('?' for _ in symbols)))
        rs = c.fetchall()
        conn.close()
        for r in rs:
            self.logger.info("{symbol},{strategy_id},{strategy_option}".format(symbol=r[0], strategy_id=r[1], strategy_option=r[2]))
            conn = MyDB().get_db()
            c = conn.cursor()
            c.execute("""
                    update backtest_result
                    set
                     profit_rate_3month = 
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
                    ,profit_rate_1year = 
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
                    ,profit_rate_3year = 
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
                    ,profit_rate_15year = 
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
                    ,long_profit_rate_3month = 
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
                    ,long_profit_rate_1year = 
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
                    ,long_profit_rate_3year = 
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
                    ,long_profit_rate_15year = 
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
                    ,short_profit_rate_3month = 
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
                    ,short_profit_rate_1year = 
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
                    ,short_profit_rate_3year = 
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
                    ,short_profit_rate_15year = 
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
    
                    ,expected_rate_3month = 
                    (
                        select 
                         sum(profit_rate) / count(profit_rate)
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
                         sum(profit_rate) / count(profit_rate)
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
                         sum(profit_rate) / count(profit_rate)
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
                         sum(profit_rate) / count(profit_rate)
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
                         sum(profit_rate) / count(profit_rate)
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
                         sum(profit_rate) / count(profit_rate)
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
                         sum(profit_rate) / count(profit_rate)
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
                         sum(profit_rate) / count(profit_rate)
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
                         sum(profit_rate) / count(profit_rate)
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
                         sum(profit_rate) / count(profit_rate)
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
                         sum(profit_rate) / count(profit_rate)
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
                         sum(profit_rate) / count(profit_rate)
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

    def update_maxdrawdown(self, symbols):
        (end_date , start_date, start_date_3month , start_date_1year , start_date_3year , start_date_15year) = self.get_dates()
        #バックテスト結果を取得
        conn = MyDB().get_db()
        c = conn.cursor()
        c.execute("""
        select 
        symbol
        ,strategy_id
        ,strategy_option 
        from backtest_result
        where symbol in ({symbols})
        """.format(symbols=', '.join('?' for _ in symbols)))
        rs = c.fetchall()
        conn.close()
        #ドローダウン算出
        for r in rs:
            symbol = r[0]
            strategy_id = r[1]
            strategy_option = r[2]
            drawdown = self.get_maxdrawdown(symbol, strategy_id, strategy_option, start_date, end_date)
            drawdown_3month = self.get_maxdrawdown(symbol, strategy_id, strategy_option, start_date_3month, end_date)
            drawdown_1year = self.get_maxdrawdown(symbol, strategy_id, strategy_option, start_date_1year, end_date)
            drawdown_3year = self.get_maxdrawdown(symbol, strategy_id, strategy_option, start_date_3year, end_date)
            drawdown_15year = self.get_maxdrawdown(symbol, strategy_id, strategy_option, start_date_15year, end_date)
            #DB更新
            conn = MyDB().get_db()
            c = conn.cursor()
            c.execute("""
            update backtest_result set 
             drawdown = {drawdown} 
            ,drawdown_3month = {drawdown_3month} 
            ,drawdown_1year = {drawdown_1year} 
            ,drawdown_3year = {drawdown_3year} 
            ,drawdown_15year = {drawdown_15year} 
            where symbol = '{symbol}'
            and strategy_id = {strategy_id}
            and strategy_option = '{strategy_option}'
            """.format(
                         symbol=symbol
                        ,strategy_id=strategy_id
                        ,strategy_option=strategy_option
                        ,drawdown=drawdown
                        ,drawdown_3month=drawdown_3month
                        ,drawdown_1year=drawdown_1year
                        ,drawdown_3year=drawdown_3year
                        ,drawdown_15year=drawdown_15year
            ))
            self.logger.info("update_drawdown() {symbol},{strategy_id},{strategy_option}".format(
                                                                                             symbol=symbol
                                                                                            ,strategy_id=strategy_id
                                                                                            ,strategy_option=strategy_option
                                                                                            ))
            conn.commit()
            conn.close()

    def get_maxdrawdown(self, symbol, strategy_id, strategy_option, start_date, end_date):
        conn = MyDB().get_db()
        c = conn.cursor()
        #cash+建玉(取得価格) 
        c.execute("""
        select
        business_date
        ,cash
        ,pos_price
        ,pos_vol 
        from backtest_history 
        where symbol = '{symbol}'
        and strategy_id = {strategy_id}
        and strategy_option = '{strategy_option}'
        and business_date between '{start_date}' and '{end_date}'
        order by business_date
        """.format(
                     symbol=symbol
                    ,strategy_id=strategy_id
                    ,strategy_option=strategy_option
                    ,start_date=start_date
                    ,end_date=end_date
        ))
        rs = c.fetchall()
        conn.close()
        maxv = 0
        minv = 0
        max_drawdown = 0
        drawdown = 0
        count = 0
        if rs:
            for r in rs:
                v = r[1] + (r[2] * r[3])
                if count == 0:
                    maxv = v
                    minv = v
                elif maxv < v:
                    maxv = v
                    minv = v
                elif minv > v:
                    minv = v
                    diff = maxv - minv
                    drawdown = round(diff / maxv, 6)
                    if max_drawdown < drawdown:
                        max_drawdown = drawdown
                        self.logger.info("maxdrawdown:{symbol},{strategy_id},{strategy_option},{start_date},{end_date},{business_date},{max_drawdown}".format(
                            symbol=symbol
                            ,strategy_id=strategy_id
                            ,strategy_option=strategy_option
                            ,start_date=start_date
                            ,end_date=end_date
                            ,business_date=r[0]
                            ,max_drawdown=max_drawdown
                        ))
                count += 1
        return max_drawdown


