
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
    primary key(symbol, strategy, start_date, end_date)
)
;
