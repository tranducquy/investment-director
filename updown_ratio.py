# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy
from argparse import ArgumentParser
import common
import mylogger
import mylock
from mydb import MyDB

class UpdownRatio():
    def __init__(self, logger=None):
        if logger is None:
            self.logger = mylogger.Logger().myLogger()
        else:
            self.logger = logger

    def update(self ,symbols, start_date, end_date):
        try:
            #TODO:select
            #TODO:単純移動平均算出
            #TODO:DB更新
            mylock.lock.acquire()
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
            mylock.lock.release()
    
    def _check_float(self, num):
        if ( num is None or numpy.isnan(num)):
            return 0.00
        else:
            return float(num)
    
    def update_maxdrawdown(self, symbols, strategy_id):
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
        and strategy_id = {strategy_id}
        """.format(symbols=', '.join('?' for _ in symbols), strategy_id=strategy_id), symbols)
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
        business_date = ''
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
                    drawdown = self.round(diff / maxv)
                    if max_drawdown < drawdown:
                        max_drawdown = drawdown
                        business_date = r[0]
                count += 1
            self.logger.info("maxdrawdown:{symbol},{strategy_id},{strategy_option},{start_date},{end_date},{business_date},{max_drawdown}".format(
                            symbol=symbol
                            ,strategy_id=strategy_id
                            ,strategy_option=strategy_option
                            ,start_date=start_date
                            ,end_date=end_date
                            ,business_date=business_date
                            ,max_drawdown=max_drawdown
                            ))
        return max_drawdown

    def round(self, v):
        return round(v, 4)

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--start_date', type=str, help='Date of backtest start')
    argparser.add_argument('--end_date', type=str, help='Date of backtest end')
    args = argparser.parse_args()
    return args

if __name__ == '__main__':
    s = mylogger.Logger()
    conf = common.read_conf()
    args = get_option()
    symbols = ['Nikkei225.txt', 'TOPIX500.txt', 'DJI.txt', 'SP500.txt']
    if args.start_date is None:
        start_date = conf['backtest_startdate']
    else:
        start_date = args.start_date
    if args.end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')
    else:
        end_date = args.end_date
    UpdownRatio().update(symbols, start_date, end_date)

