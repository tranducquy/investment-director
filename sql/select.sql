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
and end_date = '2019-08-18'
and regist_date = '2019-08-19'
and rate_of_return > -110
group by strategy, start_date, end_date
order by 平均騰落率 desc
;

--delete from backtest_result;


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


SELECT 
symbol
,strategy
,start_date
,end_date
,backtest_period
,rate_of_return
 from backtest_result 
 where 0 = 0
 and symbol = '5406.T' 
 and regist_date = '2019-08-16'
 order by regist_date desc

