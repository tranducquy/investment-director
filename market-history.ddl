
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
    primary key(symbol, strategy, start_date, end_date)
)
;

create table m_strategy
(
    id integer,
    name text
)
;
insert into m_strategy (id, name) values (1, 'ボリンジャーバンドSMA3SD1.0新値'); -- 株式(Nikkei225,TOPIX)

create table backtest
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
    execution_order_type text,
    execution_order_status text,
    execution_order_vol decimal(10, 5)
    execution_order_price decimal(10. 5),
    position integer,
    cash decimal(10, 5),
    pos_vol decimal(10, 5),
    pos_price decimal(10, 5),
    total_value decimal(10, 5),
    profit_value decimal(10, 5),
    profit_rate decimal(10, 5)
    primary key(symbol, strategy_id, business_date)
)
;