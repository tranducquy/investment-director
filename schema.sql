
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
    strategy text,
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
    primary key(symbol, strategy_id)
)
;

create table m_strategy
(
    strategy_id integer,
    strategy_name text,
    primary key(strategy_id)
)
;
insert into m_strategy (strategy_id, strategy_name) values (1, 'ボリンジャーバンド新値SMA3SD1.0'); --株式(Nikkei225,TOPIX)
insert into m_strategy (strategy_id, strategy_name) values (2, 'ボリンジャーバンド新値SMA8SD1.2'); --暗号通貨(bitmex XBTUSD), FX(minkabu GBPJPY)
insert into m_strategy (strategy_id, strategy_name) values (3, 'ボリンジャーバンド新値SMA2SD1.6'); --暗号通貨(bitmex ETHUSD)

create table m_ordertype
(
    ordertype_id integer,
    ordertype_name text,
    primary key(ordertype_id)
)
;
insert into m_ordertype (ordertype_id, ordertype_name) values (0, '注文なし');
insert into m_ordertype (ordertype_id, ordertype_name) values (1, '逆指値成行買い');
insert into m_ordertype (ordertype_id, ordertype_name) values (2, '逆指値成行売り');
insert into m_ordertype (ordertype_id, ordertype_name) values (3, '指値買い');
insert into m_ordertype (ordertype_id, ordertype_name) values (4, '指値売り');
insert into m_ordertype (ordertype_id, ordertype_name) values (5, '逆指値成行買い返済');
insert into m_ordertype (ordertype_id, ordertype_name) values (6, '逆指値成行売り返済');
insert into m_ordertype (ordertype_id, ordertype_name) values (7, '成行買い返済');
insert into m_ordertype (ordertype_id, ordertype_name) values (8, '成行売り返済');
insert into m_ordertype (ordertype_id, ordertype_name) values (9, '成行買い');
insert into m_ordertype (ordertype_id, ordertype_name) values (10, '成行売り');
insert into m_ordertype (ordertype_id, ordertype_name) values (11, '指値買い返済');
insert into m_ordertype (ordertype_id, ordertype_name) values (12, '指値売り返済');

create table backtest_history
(
    symbol text,
    strategy_id integer,
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
    primary key(symbol, strategy_id, business_date)
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
    regit_ts timestamp
    primary key(position_id)
)
;


