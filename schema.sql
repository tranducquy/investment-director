
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
    profit_rate_3month decimal(10,5),
    profit_rate_1year decimal(10,5),
    profit_rate_3year decimal(10,5),
    profit_rate_15year decimal(10,5),
    long_profit_rate_3month decimal(10,5),
    long_profit_rate_1year decimal(10,5),
    long_profit_rate_3year decimal(10,5),
    long_profit_rate_15year decimal(10,5),
    short_profit_rate_3month decimal(10,5),
    short_profit_rate_1year decimal(10,5),
    short_profit_rate_3year decimal(10,5),
    short_profit_rate_15year decimal(10,5),
    expected_rate_3month decimal(10,5),
    expected_rate_1year decimal(10,5),
    expected_rate_3year decimal(10,5),
    expected_rate_15year decimal(10,5),
    long_expected_rate_3month decimal(10,5),
    long_expected_rate_1year decimal(10,5),
    long_expected_rate_3year decimal(10,5),
    long_expected_rate_15year decimal(10,5),
    short_expected_rate_3month decimal(10,5),
    short_expected_rate_1year decimal(10,5),
    short_expected_rate_3year decimal(10,5),
    short_expected_rate_15year decimal(10,5),
    drawdown decimal(10,5),
    drawdown_3month decimal(10,5),
    drawdown_1year decimal(10,5),
    drawdown_3year decimal(10,5),
    drawdown_15year decimal(10,5),
    primary key(symbol, strategy_id, strategy_option)
)
;

create table m_strategy
(
    strategy_id integer,
    strategy_name text,
    strategy_option text,
    primary key(strategy_id)
)
;
insert into m_strategy (strategy_id, strategy_name, strategy_option) values (1, 'Bollingerband/DailyTrail', 'SMA{sma}SD{sd}');
insert into m_strategy (strategy_id, strategy_name, strategy_option) values (2, 'Bollingerband/CloseOnDaily', 'SMA{sma}SD{sd}');

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

create table m_orderstatus
(
    orderstatus_id integer,
    orderstatus_name text,
    primary key(orderstatus_id)
)
;
insert into m_orderstatus (orderstatus_id, orderstatus_name) values (0, '注文なし');
insert into m_orderstatus (orderstatus_id, orderstatus_name) values (1, '注文中');
insert into m_orderstatus (orderstatus_id, orderstatus_name) values (2, '失効');
insert into m_orderstatus (orderstatus_id, orderstatus_name) values (3, '約定');

create table m_positiontype
(
    positiontype_id integer,
    positiontype_name text,
    primary key(positiontype_id)
)
;
insert into m_positiontype (positiontype_id, positiontype_name) values (0, 'NOTHING');
insert into m_positiontype (positiontype_id, positiontype_name) values (1, 'LONG');
insert into m_positiontype (positiontype_id, positiontype_name) values (2, 'SHORT');

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
);
alter table backtest_history add column leverage decimal(10,5);

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
delete from backtest_result where symbol = 'XBTUSD';
delete from backtest_history where symbol = 'XBTUSD';
delete from backtest_result where symbol = 'ETHUSD';
delete from backtest_history where symbol = 'ETHUSD';
delete from backtest_result where symbol = 'GBPJPY';
delete from backtest_history where symbol = 'GBPJPY';
delete from backtest_result where symbol = 'USDJPY';
delete from backtest_history where symbol = 'USDJPY';
delete from backtest_result where symbol = 'EURJPY';
delete from backtest_history where symbol = 'EURJPY';
delete from backtest_result where symbol = 'AUDJPY';
delete from backtest_history where symbol = 'AUDJPY';
delete from backtest_result where symbol = 'SGDJPY';
delete from backtest_history where symbol = 'SGDJPY';
delete from backtest_result where symbol = '3103.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '3103.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5202.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5202.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6141.T' and strategy_id = 1;
delete from backtest_history where symbol = '6141.T' and strategy_id = 1;
delete from backtest_result where symbol = '6728.T' and strategy_id = 1;
delete from backtest_history where symbol = '6728.T' and strategy_id = 1;
delete from backtest_result where symbol = '6753.T' and strategy_id = 1;
delete from backtest_history where symbol = '6753.T' and strategy_id = 1;
delete from backtest_result where symbol = '7012.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7012.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8303.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8303.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9101.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9101.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9107.T' and strategy_id = 1;
delete from backtest_history where symbol = '9107.T' and strategy_id = 1;
delete from backtest_result where symbol = '7003.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7003.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8377.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8377.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8473.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8473.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7732.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7732.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5019.T' and strategy_id = 1;
delete from backtest_history where symbol = '5019.T' and strategy_id = 1;
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
delete from backtest_result where symbol = '1954.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1954.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2109.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2109.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2120.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2120.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2168.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2168.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2378.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2378.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2462.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2462.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2695.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2695.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2752.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2752.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2767.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2767.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2792.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2792.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7616.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7616.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8136.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8136.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8904.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8904.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6440.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6440.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5801.T' and strategy_id = 1;
delete from backtest_history where symbol = '5801.T' and strategy_id = 1;
delete from backtest_result where symbol = '6205.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6205.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8613.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8613.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5406.T' and strategy_id = 1;
delete from backtest_history where symbol = '5406.T' and strategy_id = 1;
delete from backtest_result where symbol = '1518.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1518.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1766.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1766.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1808.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1808.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1820.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1820.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1821.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1821.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5981.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5981.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7599.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7599.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7513.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7513.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6815.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6815.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5711.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5711.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4028.T' and strategy_id = 1;
delete from backtest_history where symbol = '4028.T' and strategy_id = 1;
delete from backtest_result where symbol = '5707.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5707.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4368.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4368.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5711.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5711.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8698.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8698.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6866.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6866.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5741.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5741.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7004.T' and strategy_id = 1;
delete from backtest_history where symbol = '7004.T' and strategy_id = 1;
delete from backtest_result where symbol = '3101.T' and strategy_id = 1;
delete from backtest_history where symbol = '3101.T' and strategy_id = 1;
delete from backtest_result where symbol = '2501.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2501.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2729.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2729.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '3004.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '3004.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '3526.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '3526.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4022.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4022.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4298.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4298.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4641.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4641.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4971.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4971.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5391.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5391.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5410.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5410.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5464.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5464.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7236.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7236.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5491.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5491.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5541.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5541.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5715.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5715.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5807.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5807.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5998.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5998.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6104.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6104.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6236.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6236.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6298.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6298.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6315.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6315.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1570.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1570.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1605.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1605.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1809.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '1809.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2428.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2428.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '2768.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '2768.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '3068.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '3068.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '3116.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '3116.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '3401.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '3401.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4004.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4004.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4043.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4043.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4062.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4062.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1356.T' and strategy_id = 1;
delete from backtest_history where symbol = '1356.T' and strategy_id = 1;
delete from backtest_result where symbol = '1568.T' and strategy_id = 1;
delete from backtest_history where symbol = '1568.T' and strategy_id = 1;
delete from backtest_result where symbol = '4183.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4183.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4502.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4502.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4661.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4661.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '4716.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '4716.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5105.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5105.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5201.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5201.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5232.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5232.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5233.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5233.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5310.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5310.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5333.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5333.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5401.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5401.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5411.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5411.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5480.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5480.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5563.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5563.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5631.T' and strategy_id = 1;
delete from backtest_history where symbol = '5631.T' and strategy_id = 1;
delete from backtest_result where symbol = '5706.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5706.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5726.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5726.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5727.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5727.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '5803.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '5803.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6103.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6103.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6269.T' and strategy_id = 1;
delete from backtest_history where symbol = '6269.T' and strategy_id = 1;
delete from backtest_result where symbol = '6302.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6302.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6305.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6305.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6310.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6310.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6361.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6361.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6366.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6366.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6460.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6460.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6474.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6474.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6501.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6501.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6674.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6674.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6701.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6701.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6724.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6724.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6758.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6758.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6803.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6803.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7011.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7011.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7013.T' and strategy_id = 1;
delete from backtest_history where symbol = '7013.T' and strategy_id = 1;
delete from backtest_result where symbol = '7189.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7189.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7203.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7203.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7211.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7211.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '6135.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '6135.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7241.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7241.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7242.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7242.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7261.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7261.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7550.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7550.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7581.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7581.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7860.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7860.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '7974.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '7974.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8031.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8031.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8053.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8053.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8078.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8078.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8233.T' and strategy_id = 1;
delete from backtest_history where symbol = '8233.T' and strategy_id = 1;
delete from backtest_result where symbol = '8267.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8267.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8316.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8316.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8338.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8338.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8511.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8511.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8570.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8570.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8591.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8591.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8595.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8595.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8604.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8604.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8086.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8086.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8616.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8616.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8628.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8628.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8703.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8703.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '8830.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '8830.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9001.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9001.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9005.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9005.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9008.T' and strategy_id = 1 and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9008.T' and strategy_id = 1 and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9041.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9041.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9062.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9062.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9104.T' and strategy_id = 1;
delete from backtest_history where symbol = '9104.T' and strategy_id = 1;
delete from backtest_result where symbol = '9202.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9202.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9474.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9474.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9501.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9501.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '9983.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_history where symbol = '9983.T' and strategy_option = 'SMA3SD1.0';
delete from backtest_result where symbol = '1321.T' and strategy_id = 1;
delete from backtest_history where symbol = '1321.T' and strategy_id = 1;
delete from backtest_result where symbol = '1571.T' and strategy_id = 1;
delete from backtest_history where symbol = '1571.T' and strategy_id = 1;

delete from bollingerband_dailytrail;
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1514.T', 3, 0.8);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1515.T', 4, 0.8);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1518.T', 23, 0.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1766.T', 9, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1805.T', 5, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1808.T', 16, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1813.T', 8, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1820.T', 5, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1821.T', 12, 1.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1861.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1866.T', 5, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1885.T', 9, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1914.T', 4, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1954.T', 3, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1963.T', 12, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2109.T', 5, 1.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2120.T', 18, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2168.T', 9, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2286.T', 10, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2378.T', 15, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2462.T', 24, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2695.T', 13, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2752.T', 7, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2767.T', 3, 1.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2792.T', 3, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4368.T', 3, 1.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4527.T', 3, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5202.T', 24, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5406.T', 12, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5471.T', 3, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5707.T', 23, 1.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5711.T', 8, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5741.T', 2, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5801.T', 9, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5981.T', 6, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6205.T', 8, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6440.T', 7, 0.8);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6815.T', 7, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6866.T', 4, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7003.T', 10, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7012.T', 8, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7201.T', 7, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7513.T', 4, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7599.T', 17, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7732.T', 4, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8136.T', 19, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8303.T', 21, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8377.T', 4, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8473.T', 8, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8601.T', 4, 0.8);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8613.T', 4, 1.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8698.T', 8, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8801.T', 4, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8904.T', 8, 0.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9101.T', 23, 0.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('ETHUSD', 4, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('GBPJPY', 3, 1.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('USDJPY', 2, 1.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('XBTUSD', 13, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2501.T', 14, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2729.T', 4, 1.8);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('3004.T', 2, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('3526.T', 23, 0.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4022.T', 7, 1.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4298.T', 13, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4641.T', 21, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4971.T', 3, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5391.T', 23, 0.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5410.T', 8, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5464.T', 3, 1.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7236.T', 3, 0.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5491.T', 6, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5541.T', 17, 0.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5715.T', 17, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5807.T', 5, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5998.T', 13, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6104.T', 4, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6236.T', 2, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6298.T', 3, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6315.T', 6, 1.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1605.T', 5, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1809.T', 5, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2428.T', 4, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('2768.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('3068.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('3116.T', 8, 0.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('3401.T', 8, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4004.T', 6, 1.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4043.T', 13, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4062.T', 24, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1570.T', 4, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1357.T', 8, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1356.T', 4, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4183.T', 5, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4502.T', 24, 0.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4661.T', 24, 1.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4716.T', 23, 0.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5105.T', 10, 0.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5201.T', 24, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5232.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5233.T', 3, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5310.T', 1, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5333.T', 13, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5401.T', 5, 1.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5411.T', 19, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5480.T', 18, 1.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5563.T', 22, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5706.T', 5, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5726.T', 2, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5727.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5803.T', 17, 0.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6103.T', 6, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6269.T', 9, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6302.T', 8, 0.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6305.T', 17, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6310.T', 6, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6366.T', 18, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6460.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6474.T', 3, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6501.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6674.T', 15, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6701.T', 8, 2.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6724.T', 15, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6758.T', 3, 2.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6803.T', 3, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7011.T', 10, 0.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7189.T', 5, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7203.T', 9, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7211.T', 11, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6135.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7241.T', 5, 0.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7242.T', 6, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7261.T', 11, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7550.T', 23, 0.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7581.T', 4, 0.8);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7860.T', 5, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7974.T', 2, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8031.T', 3, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8053.T', 8, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8078.T', 3, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8267.T', 15, 0.8);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8316.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8338.T', 3, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8511.T', 3, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8570.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8591.T', 4, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8595.T', 7, 0.8);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8604.T', 20, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8086.T', 2, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8616.T', 3, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8628.T', 9, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8703.T', 24, 0.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8830.T', 24, 0.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9001.T', 17, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9005.T', 4, 1.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9008.T', 3, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9041.T', 4, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9062.T', 3, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9202.T', 14, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9474.T', 4, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9501.T', 24, 0.3);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9983.T', 19, 0.2);
--2019.10.16
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9104.T', 18, 1.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('9107.T', 13, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6141.T', 4, 1.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5019.T', 3, 1.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1568.T', 3, 1.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6753.T', 14, 0.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('3101.T', 4, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('3103.T', 10, 0.9);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('4028.T', 16, 0.5);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6361.T', 4, 2.2);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('6728.T', 8, 2.0);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7004.T', 7, 1.4);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7013.T', 3, 1.1);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('7616.T', 3, 0.7);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('8233.T', 3, 0.9);
--2019.10.24
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('5631.T', 6, 1.6);
--2019.11.25
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1321.T', 4, 0.6);
insert into bollingerband_dailytrail (symbol, sma, sigma1) values ('1571.T', 7, 0.4);


create table bollingerband_closeondaily
(
    symbol text,
    sma integer,
    sigma1 decimal(10,5),
    primary key(symbol, sma, sigma1)
);
delete from bollingerband_closeondaily;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('6674.T', 18, 0.4);
delete from backtest_result where symbol = '6674.T' and strategy_id = 2;
delete from backtest_history where symbol = '6674.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('5333.T', 15, 0.3);
delete from backtest_result where symbol = '5333.T' and strategy_id = 2;
delete from backtest_history where symbol = '5333.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('9041.T', 22, 0.4);
delete from backtest_result where symbol = '9041.T' and strategy_id = 2;
delete from backtest_history where symbol = '9041.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('9001.T', 17, 0.5);
delete from backtest_result where symbol = '9001.T' and strategy_id = 2;
delete from backtest_history where symbol = '9001.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('7550.T', 23, 0.2);
delete from backtest_result where symbol = '7550.T' and strategy_id = 2;
delete from backtest_history where symbol = '7550.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('9005.T', 3, 0.8);
delete from backtest_result where symbol = '9005.T' and strategy_id = 2;
delete from backtest_history where symbol = '9005.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('1766.T', 12, 1.8);
delete from backtest_result where symbol = '1766.T' and strategy_id = 2;
delete from backtest_history where symbol = '1766.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('1801.T', 2, 2.3);
delete from backtest_result where symbol = '1801.T' and strategy_id = 2;
delete from backtest_history where symbol = '1801.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('1820.T', 16, 0.7);
delete from backtest_result where symbol = '1820.T' and strategy_id = 2;
delete from backtest_history where symbol = '1820.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('1885.T', 11, 0.4);
delete from backtest_result where symbol = '1885.T' and strategy_id = 2;
delete from backtest_history where symbol = '1885.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('2168.T', 9, 2.1);
delete from backtest_result where symbol = '2168.T' and strategy_id = 2;
delete from backtest_history where symbol = '2168.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('2792.T', 24, 1.3);
delete from backtest_result where symbol = '2792.T' and strategy_id = 2;
delete from backtest_history where symbol = '2792.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('4028.T', 3, 0.3);
delete from backtest_result where symbol = '4028.T' and strategy_id = 2;
delete from backtest_history where symbol = '4028.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('4502.T', 6, 0.7);
delete from backtest_result where symbol = '4502.T' and strategy_id = 2;
delete from backtest_history where symbol = '4502.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('5202.T', 18, 0.1);
delete from backtest_result where symbol = '5202.T' and strategy_id = 2;
delete from backtest_history where symbol = '5202.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('5406.T', 13, 1.7);
delete from backtest_result where symbol = '5406.T' and strategy_id = 2;
delete from backtest_history where symbol = '5406.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('5410.T', 6, 1.8);
delete from backtest_result where symbol = '5410.T' and strategy_id = 2;
delete from backtest_history where symbol = '5410.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('5491.T', 17, 0.3);
delete from backtest_result where symbol = '5491.T' and strategy_id = 2;
delete from backtest_history where symbol = '5491.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('5631.T', 4, 2.2);
delete from backtest_result where symbol = '5631.T' and strategy_id = 2;
delete from backtest_history where symbol = '5631.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('5706.T', 10, 1.7);
delete from backtest_result where symbol = '5706.T' and strategy_id = 2;
delete from backtest_history where symbol = '5706.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('5711.T', 8, 1.8);
delete from backtest_result where symbol = '5711.T' and strategy_id = 2;
delete from backtest_history where symbol = '5711.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('5715.T', 6, 2.1);
delete from backtest_result where symbol = '5715.T' and strategy_id = 2;
delete from backtest_history where symbol = '5715.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('5801.T', 10, 1.2);
delete from backtest_result where symbol = '5801.T' and strategy_id = 2;
delete from backtest_history where symbol = '5801.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('6141.T', 4, 0.8);
delete from backtest_result where symbol = '6141.T' and strategy_id = 2;
delete from backtest_history where symbol = '6141.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('6269.T', 9, 1.3);
delete from backtest_result where symbol = '6269.T' and strategy_id = 2;
delete from backtest_history where symbol = '6269.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('6474.T', 2, 2.1);
delete from backtest_result where symbol = '6474.T' and strategy_id = 2;
delete from backtest_history where symbol = '6474.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('6728.T', 12, 2.2);
delete from backtest_result where symbol = '6728.T' and strategy_id = 2;
delete from backtest_history where symbol = '6728.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('6753.T', 15, 0.6);
delete from backtest_result where symbol = '6753.T' and strategy_id = 2;
delete from backtest_history where symbol = '6753.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('6803.T', 16, 0.9);
delete from backtest_result where symbol = '6803.T' and strategy_id = 2;
delete from backtest_history where symbol = '6803.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('6815.T', 19, 0.8);
delete from backtest_result where symbol = '6815.T' and strategy_id = 2;
delete from backtest_history where symbol = '6815.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('7003.T', 9, 1.8);
delete from backtest_result where symbol = '7003.T' and strategy_id = 2;
delete from backtest_history where symbol = '7003.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('7211.T', 8, 0.4);
delete from backtest_result where symbol = '7211.T' and strategy_id = 2;
delete from backtest_history where symbol = '7211.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('7242.T', 9, 1.5);
delete from backtest_result where symbol = '7242.T' and strategy_id = 2;
delete from backtest_history where symbol = '7242.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('7550.T', 23, 0.2);
delete from backtest_result where symbol = '7550.T' and strategy_id = 2;
delete from backtest_history where symbol = '7550.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('7581.T', 22, 1.7);
delete from backtest_result where symbol = '7581.T' and strategy_id = 2;
delete from backtest_history where symbol = '7581.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('7616.T', 12, 0.5);
delete from backtest_result where symbol = '7616.T' and strategy_id = 2;
delete from backtest_history where symbol = '7616.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('8031.T', 13, 0.3);
delete from backtest_result where symbol = '8031.T' and strategy_id = 2;
delete from backtest_history where symbol = '8031.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('8053.T', 8, 0.1);
delete from backtest_result where symbol = '8053.T' and strategy_id = 2;
delete from backtest_history where symbol = '8053.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('8086.T', 12, 0.8);
delete from backtest_result where symbol = '8086.T' and strategy_id = 2;
delete from backtest_history where symbol = '8086.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('8136.T', 20, 0.5);
delete from backtest_result where symbol = '8136.T' and strategy_id = 2;
delete from backtest_history where symbol = '8136.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('8233.T', 9, 0.5);
delete from backtest_result where symbol = '8233.T' and strategy_id = 2;
delete from backtest_history where symbol = '8233.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('8267.T', 16, 1.3);
delete from backtest_result where symbol = '8267.T' and strategy_id = 2;
delete from backtest_history where symbol = '8267.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('8604.T', 3, 1.2);
delete from backtest_result where symbol = '8604.T' and strategy_id = 2;
delete from backtest_history where symbol = '8604.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('8613.T', 10, 0.3);
delete from backtest_result where symbol = '8613.T' and strategy_id = 2;
delete from backtest_history where symbol = '8613.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('8628.T', 11, 1.7);
delete from backtest_result where symbol = '8628.T' and strategy_id = 2;
delete from backtest_history where symbol = '8628.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('9001.T', 20, 1.1);
delete from backtest_result where symbol = '9001.T' and strategy_id = 2;
delete from backtest_history where symbol = '9001.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('9008.T', 22, 0.3);
delete from backtest_result where symbol = '9008.T' and strategy_id = 2;
delete from backtest_history where symbol = '9008.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('9041.T', 22, 0.4);
delete from backtest_result where symbol = '9041.T' and strategy_id = 2;
delete from backtest_history where symbol = '9041.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('9062.T', 15, 0.8);
delete from backtest_result where symbol = '9062.T' and strategy_id = 2;
delete from backtest_history where symbol = '9062.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('9202.T', 14, 0.7);
delete from backtest_result where symbol = '9202.T' and strategy_id = 2;
delete from backtest_history where symbol = '9202.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('1570.T', 2, 2.4);
delete from backtest_result where symbol = '1570.T' and strategy_id = 2;
delete from backtest_history where symbol = '1570.T' and strategy_id = 2;
insert into bollingerband_closeondaily(symbol, sma, sigma1) values ('1356.T', 8, 1.6);
delete from backtest_result where symbol = '1356.T' and strategy_id = 2;
delete from backtest_history where symbol = '1356.T' and strategy_id = 2;

create table updown_ratio
(
    symbol text,
    business_date date,
    up_count decimal(10,5),
    down_count decimal(10,5),
    sma5 decimal(10,5),
    sma6 decimal(10,5),
    sma10 decimal(10,5),
    sma15 decimal(10,5),
    sma25 decimal(10,5),
    primary key(symbol, business_date)
)
;

create table trading_volume
(
    symbol text,
    business_date date,
    volume decimal(10,5),
    primary key(symbol, business_date)
)
;
