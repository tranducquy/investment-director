select
r.symbol
,ms.strategy_name
,r.strategy_option
,r.end_date
,r.rate_of_return as 全期間騰落率_複利
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
,r.payoffratio * r.win_rate * (r.win_count+r.loss_count) as ペイオフレシオ×勝率
from backtest_result as r
inner join m_strategy as ms 
on r.strategy_id = ms.strategy_id
where 0 = 0 
and r.regist_date = '2019-09-15'
and r.expected_rate_3month > 5
and r.expected_rate_1year > 15*1
and r.expected_rate_3year > 15*3
and r.expected_rate_15year > 15*15
and r.rate_of_return > 500
order by r.rate_of_return desc
