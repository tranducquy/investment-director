
create table ohlc
(
    symbol text,
    business_date date,
    open decimal(10,5),
    high decimal(10,5),
    low decimal(10,5),
    close decimal(10,5),
    volume decimal(10,5),
    primary key(symbol, business_date)
)
;

create table backtest_result 
(
    symbol text,
    strategy_id integer,
    strategy_option text,
    start_date text,
    end_date text,
    market_start_date text,
    market_end_date text,
    backtest_period integer,
    trading_period integer,
    average_period_per_trade integer,
    initial_assets decimal(10,5),
    last_assets decimal(10,5),
    rate_of_return decimal(10,5),
    win_count integer,
    loss_count integer,
    win_value decimal(10,5),
    loss_value decimal(10,5),
    win_rate decimal(10,5),
    payoffratio decimal(10,5),
    expected_rate decimal(10,5),
    expected_rate_per_1day decimal(10,5),
    long_win_count integer,
    long_loss_count integer,
    long_win_value decimal(10,5),
    long_loss_value decimal(10,5),
    long_win_rate decimal(10,5),
    long_payoffratio decimal(10,5),
    long_expected_rate decimal(10,5),
    long_expected_rate_per_1day decimal(10,5),
    short_win_count integer,
    short_loss_count integer,
    short_win_value decimal(10,5),
    short_loss_value decimal(10,5),
    short_win_rate decimal(10,5),
    short_payoffratio decimal(10,5),
    short_expected_rate decimal(10,5),
    short_expected_rate_per_1day decimal(10,5),
    regist_date text,
    primary key(symbol, strategy_id, strategy_option)
)
;
alter table backtest_result add column profit_rate_3month decimal(10,5);
alter table backtest_result add column profit_rate_1year decimal(10,5);
alter table backtest_result add column profit_rate_3year decimal(10,5);
alter table backtest_result add column profit_rate_15year decimal(10,5);
alter table backtest_result add column long_profit_rate_3month decimal(10,5);
alter table backtest_result add column long_profit_rate_1year decimal(10,5);
alter table backtest_result add column long_profit_rate_3year decimal(10,5);
alter table backtest_result add column long_profit_rate_15year decimal(10,5);
alter table backtest_result add column short_profit_rate_3month decimal(10,5);
alter table backtest_result add column short_profit_rate_1year decimal(10,5);
alter table backtest_result add column short_profit_rate_3year decimal(10,5);
alter table backtest_result add column short_profit_rate_15year decimal(10,5);
alter table backtest_result add column expected_rate_3month decimal(10,5);
alter table backtest_result add column expected_rate_1year decimal(10,5);
alter table backtest_result add column expected_rate_3year decimal(10,5);
alter table backtest_result add column expected_rate_15year decimal(10,5);
alter table backtest_result add column long_expected_rate_3month decimal(10,5);
alter table backtest_result add column long_expected_rate_1year decimal(10,5);
alter table backtest_result add column long_expected_rate_3year decimal(10,5);
alter table backtest_result add column long_expected_rate_15year decimal(10,5);
alter table backtest_result add column short_expected_rate_3month decimal(10,5);
alter table backtest_result add column short_expected_rate_1year decimal(10,5);
alter table backtest_result add column short_expected_rate_3year decimal(10,5);
alter table backtest_result add column short_expected_rate_15year decimal(10,5);

create table m_strategy
(
    strategy_id integer,
    strategy_name text,
    strategy_option text,
    primary key(strategy_id)
)
;
insert into m_strategy (strategy_id, strategy_name, strategy_option) values (1, 'Bollingerband/DailyTrail', 'SMA{sma}SD{sd}');

create table m_ordertype
(
    ordertype_id integer,
    ordertype_name text,
    primary key(ordertype_id)
)
;
insert into m_ordertype (ordertype_id, ordertype_name) values (0, '注文なし');
insert into m_ordertype (ordertype_id, ordertype_name) values (1, '逆指値成行買');
insert into m_ordertype (ordertype_id, ordertype_name) values (2, '逆指値成行売');
insert into m_ordertype (ordertype_id, ordertype_name) values (3, '指値買');
insert into m_ordertype (ordertype_id, ordertype_name) values (4, '指値売');
insert into m_ordertype (ordertype_id, ordertype_name) values (5, '逆指値成行返売');
insert into m_ordertype (ordertype_id, ordertype_name) values (6, '逆指値成行返買');
insert into m_ordertype (ordertype_id, ordertype_name) values (7, '成行返売');
insert into m_ordertype (ordertype_id, ordertype_name) values (8, '成行返買');
insert into m_ordertype (ordertype_id, ordertype_name) values (9, '成行買');
insert into m_ordertype (ordertype_id, ordertype_name) values (10, '成行売');
insert into m_ordertype (ordertype_id, ordertype_name) values (11, '指値返売');
insert into m_ordertype (ordertype_id, ordertype_name) values (12, '指値返買');

create table backtest_history
(
    symbol text,
    strategy_id integer,
    strategy_option text,
    business_date text,
    open decimal(10,5),
    high decimal(10,5),
    low decimal(10,5),
    close decimal(10,5),
    volume decimal(10, 5),
    sma decimal(10, 5),
    upper_sigma1 decimal(10, 5),
    lower_sigma1 decimal(10, 5),
    upper_sigma2 decimal(10, 5),
    lower_sigma2 decimal(10, 5),
    vol_sma decimal(10, 5),
    vol_upper_sigma1 decimal(10, 5),
    vol_lower_sigma1 decimal(10, 5),
    order_create_date text,
    order_type integer,
    order_vol decimal(10, 5),
    order_price decimal(10, 5),
    call_order_date text,
    call_order_type integer,
    call_order_vol decimal(10, 5),
    call_order_price decimal(10, 5),
    execution_order_date text,
    execution_order_type integer,
    execution_order_status text,
    execution_order_vol decimal(10, 5),
    execution_order_price decimal(10, 5),
    position integer,
    cash decimal(10, 5),
    pos_vol decimal(10, 5),
    pos_price decimal(10, 5),
    total_value decimal(10, 5),
    profit_value decimal(10, 5),
    profit_rate decimal(10, 5),
    primary key(symbol, strategy_id, strategy_option, business_date)
)
;

create table position
(
    position_id integer,
    symbol text,
    position_type integer,
    open_order_type integer,
    open_order_status integer,
    close_order_type integer,
    close_order_status integer,
    open_date text,
    close_date text,
    open_price decimal(10,5),
    open_volume desimal(10,5),
    position_volume desimal(10,5),
    close_price decimal(10,5),
    close_volume desimal(10,5),
    update_ts timestamp,
    regit_ts timestamp,
    primary key(position_id)
)
;

delete from ohlc where symbol = '4666.T' and business_date = '2007-01-01';
delete from backtest_history where symbol = '4666.T' and business_date = '2007-01-01';
delete from backtest_result where symbol = '4666.T';
delete from ohlc where symbol = '4751.T' and business_date = '2007-01-01';
delete from backtest_history where symbol = '4751.T' and business_date = '2007-01-01';
delete from backtest_result where symbol = '4751.T';
delete from ohlc where symbol = '4755.T' and business_date < '2013-07-16';
delete from backtest_history where symbol = '4755.T' and business_date < '2013-07-16';
delete from backtest_result where symbol = '4755.T';
delete from ohlc where symbol = '5214.T' and business_date < '2007-01-01';
delete from backtest_history where symbol = '5214.T' and business_date < '2007-01-01';
delete from backtest_result where symbol = '5214.T';
delete from ohlc where symbol = '7267.T' and business_date < '2007-01-01';
delete from backtest_history where symbol = '7267.T' and business_date < '2007-01-01';
delete from backtest_result where symbol = '7267.T';
delete from ohlc where symbol = '8309.T' and business_date < '2007-01-01';
delete from backtest_history where symbol = '8309.T' and business_date < '2007-01-01';
delete from backtest_result where symbol = '8309.T';
delete from ohlc where symbol = '8411.T' and business_date < '2006-08-01';
delete from backtest_history where symbol = '8411.T' and business_date < '2006-08-01';
delete from backtest_result where symbol = '8411.T';
delete from ohlc where symbol = '9201.T' and business_date < '2002-10-01';
delete from backtest_history where symbol = '9201.T' and business_date < '2002-10-01';
delete from backtest_result where symbol = '9201.T';
delete from ohlc where symbol = '9613.T' and business_date < '2009-02-24';
delete from backtest_history where symbol = '9613.T' and business_date < '2009-02-24';
delete from backtest_result where symbol = '9613.T';
delete from ohlc where symbol = '9984.T' and business_date < '2006-01-10';
delete from backtest_history where symbol = '9984.T' and business_date < '2006-01-10';
delete from backtest_result where symbol = '9984.T';

create table bollingerband_dailytrail
(
    symbol text,
    sma integer,
    sigma1 decimal(10,5),
    primary key(symbol, sma, sigma1)
);
delete from bollingerband_dailytrail where symbol = 'XBTUSD';
delete from bollingerband_dailytrail where symbol = 'ETHUSD';
delete from bollingerband_dailytrail where symbol = 'GBPJPY';
delete from backtest_result where symbol = 'XBTUSD' and strategy_option = 'SMA8SD1.2';
delete from backtest_history where symbol = 'XBTUSD' and strategy_option = 'SMA8SD1.2';
delete from backtest_result where symbol = 'ETHUSD' and strategy_option = 'SMA2SD1.6';
delete from backtest_history where symbol = 'ETHUSD' and strategy_option = 'SMA2SD1.6';
delete from backtest_result where symbol = 'GBPJPY' and strategy_option = 'SMA8SD1.2';
delete from backtest_history where symbol = 'GBPJPY' and strategy_option = 'SMA8SD1.2';
delete from backtest_result where symbol = '3103.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '3103.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5202.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5202.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6141.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6141.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6728.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6728.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6753.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6753.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7012.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7012.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8303.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8303.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9101.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9101.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9107.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9107.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7003.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7003.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8377.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8377.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8473.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8473.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7732.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7732.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5019.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5019.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8601.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8601.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8801.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8801.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1963.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1963.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7201.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7201.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5471.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5471.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4527.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4527.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1514.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1514.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1515.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1515.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1805.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1805.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1813.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1813.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1861.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1861.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1866.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1866.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1885.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1885.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1914.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1914.T' and strategy_option = 'SMA3SD1.0';
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('XBTUSD', 13, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('ETHUSD', 8, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('GBPJPY', 20, 0.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('3103.T', 18, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5202.T', 24, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6141.T', 3, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6728.T', 16, 0.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6753.T', 4, 1.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7012.T', 8, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8303.T', 21, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9101.T', 23, 0.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9107.T', 19, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7003.T', 10, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8377.T', 4, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8473.T', 8, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7732.T', 4, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5019.T', 15, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8601.T', 4, 0.8);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8801.T', 4, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1963.T', 12, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7201.T', 7, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5471.T', 3, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4527.T', 3, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1514.T', 3, 0.8);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1515.T', 4, 0.8);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1805.T', 5, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1813.T', 8, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1861.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1866.T', 5, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1885.T', 9, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1914T', 4, 1.4);





