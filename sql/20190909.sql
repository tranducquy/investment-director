select 
symbol 
from backtest_history 
where business_date >= '2016-01-01'
and strategy_option = 'SMA3SD1.0' 
group by symbol,strategy_id,strategy_option 
having sum(profit_rate) > 60;

--
2264.T
3288.T
3349.T
4004.T
4043.T
4506.T
4523.T
4527.T
4587.T
5202.T
5706.T
5707.T
6141.T
6728.T
6753.T
6902.T
7003.T
7616.T
7732.T
7974.T
8028.T
8086.T
8267.T
8341.T
8377.T
8379.T
8473.T
8601.T
8848.T
9062.T
9107.T
9601.T
9984.T