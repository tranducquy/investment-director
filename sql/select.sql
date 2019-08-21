-- SQLite

-- strategy summary
SELECT
 count(symbol) as 件数
,strategy
,start_date
,end_date
,avg(rate_of_return) as 平均騰落率
,max(rate_of_return) as 最高騰落率
,min(rate_of_return) as 最低騰落率
,avg(win_rate) as 平均勝率
,avg(trading_period) as 平均取引日数
,avg(expected_rate) as 平均期待損益率
,avg(expected_rate_per_1day) as 一日当たりの期待損益率平均
,avg(long_expected_rate) as 平均期待損益率long
,avg(long_expected_rate_per_1day) as 一日当たりの期待損益率平均long
,avg(short_expected_rate) as 平均期待損益率short
,avg(short_expected_rate_per_1day) as 一日当たりの期待損益率平均short
,avg(average_period_per_trade) as 取引当たりの平均日数
,avg(win_count+loss_count) as 平均取引数
from backtest_result
where 0 = 0
and end_date = '2019-08-20'
and regist_date = '2019-08-21'
and rate_of_return > -110
group by strategy, start_date, end_date
order by 平均騰落率 desc
;

--delete from backtest_result;
--delete from backtest_history;
--delete from backtest_ohlc;

--銘柄抽出
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
   where start_date = '2018-08-16'
   and end_date = '2019-08-15'
   and backtest_period > 300*1
   and rate_of_return > 0
   ) y1
   on m3.symbol = y1.symbol and m3.strategy = y1.strategy
   left outer join (
   select
    *
   from backtest_result
   where start_date = '2016-08-16'
   and end_date = '2019-08-15'
   and backtest_period > 300*3
   and rate_of_return > 0
   ) y3
   on m3.symbol = y3.symbol and m3.strategy = y3.strategy
   left outer join (
   select
    *
   from backtest_result
   where start_date = '2004-08-16'
   and end_date = '2019-08-15'
   and backtest_period > 300*15
   and rate_of_return > 0
   ) y15
   on m3.symbol = y15.symbol and m3.strategy = y15.strategy
   where m3.start_date = '2019-05-16'
   and m3.end_date = '2019-08-15'
   and m3.rate_of_return > 0
   and
   (
       --(m3.rate_of_return < y1.rate_of_return and y1.rate_of_return < y3.rate_of_return and y3.rate_of_return < y15.rate_of_return)
       --or
       (y1.rate_of_return > 15 and y3.rate_of_return > 45 and y15.rate_of_return > 225)
   )
   order by m3.rate_of_return desc
   ;

-- 投資シグナル
SELECT
 symbol
,order_create_date
,order_type
,order_vol
,order_price
,position
,total_value
from backtest_history
where 0 = 0
and business_date = 
(select max(business_date) from backtest_history)
and order_type in (1, 2)
and order_price > 0
and order_vol > 0
order by total_value desc
;

--銘柄抽出2
    select
     r.symbol
    ,r.strategy
    ,r.end_date
    ,m3.profit_rate_sum as 期待利益率3か月
    ,y1.profit_rate_sum as 期待利益率1年
    ,y3.profit_rate_sum as 期待利益率3年
    ,y15.profit_rate_sum as 期待利益率15年
    ,r.average_period_per_trade as 平均取引期間
    ,r.win_rate as 勝率
    ,r.long_expected_rate as 期待利益率long
    ,r.long_win_count+r.long_loss_count as 取引数long
    ,r.short_expected_rate as 期待利益率short
    ,r.short_win_count+r.short_loss_count as 取引数short
    ,r.win_count+r.loss_count as 取引数
   from backtest_result r
   left outer join (
   select
     symbol
    ,strategy_id
    ,sum(profit_rate) as profit_rate_sum
    ,count(business_date) as count
   from backtest_history
   where business_date between '2019-05-20' and '2019-08-19'
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
   where business_date between '2018-08-20' and '2019-08-19'
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
   where business_date between '2013-08-20' and '2019-08-19'
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
   where business_date between '2004-08-20' and '2019-08-19'
   group by symbol, strategy_id
   HAVING count(business_date) > 2738
   ) y15
   on r.symbol = y15.symbol and r.strategy_id = y15.strategy_id
   where r.start_date = '2001-01-01'
   and r.end_date = '2019-08-19'
   and r.rate_of_return > 0
   and (m3.profit_rate_sum > 3 and y1.profit_rate_sum > 15 and y3.profit_rate_sum > 45 and y15.profit_rate_sum > 225)
   order by m3.profit_rate_sum desc
   ;


    select
     r.symbol
    ,r.strategy
    ,order_table.order_type
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
   from backtest_result r
   left outer join (
   select
     symbol
    ,strategy_id
    ,sum(profit_rate) as profit_rate_sum
    ,count(business_date) as count
   from backtest_history
   where business_date between '2019-05-21' and '2019-08-20'
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
   where business_date between '2018-08-21' and '2019-08-20'
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
   where business_date between '2016-08-21' and '2019-08-20'
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
   where business_date between '2004-08-21' and '2019-08-20'
   group by symbol, strategy_id
   HAVING count(business_date) > 2738
   ) y15
   on r.symbol = y15.symbol and r.strategy_id = y15.strategy_id
   inner join (
        select
         symbol
        ,order_create_date
        ,order_type
        ,order_vol
        ,order_price
        from backtest_history
        where business_date = (select max(business_date) from backtest_history)
        and order_type in (1, 2)
        and order_price > 0
        and order_vol > 0
   ) as order_table
   on r.symbol = order_table.symbol
   where r.start_date = '2001-01-01'
   and r.end_date = '2019-08-20'
   and r.rate_of_return > 0
   and (m3.profit_rate_sum > 3 and y1.profit_rate_sum > 15 and y3.profit_rate_sum > 45 and y15.profit_rate_sum > 225)
   order by m3.profit_rate_sum desc
;
