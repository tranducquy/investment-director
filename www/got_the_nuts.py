
from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

DATABASE = '/usr/local/investment-director/market-history.db'
BACKTEST_HISTORY_QUERY = """
                    select 
                     bh.symbol
                    ,ms.name
                    ,bh.business_date
                    ,bh.open
                    ,bh.high
                    ,bh.low
                    ,bh.close
                    ,bh.volume
                    ,bh.sma
                    ,bh.upper_sigma1
                    ,bh.lower_sigma1
                    ,bh.upper_sigma2
                    ,bh.lower_sigma2
                    ,bh.vol_sma
                    ,bh.vol_upper_sigma1
                    ,bh.vol_lower_sigma1
                    ,bh.order_create_date
                    ,bh.order_type
                    ,bh.order_vol
                    ,bh.order_price
                    ,bh.call_order_date
                    ,bh.call_order_type
                    ,bh.call_order_vol
                    ,bh.call_order_price
                    ,bh.execution_order_date
                    ,bh.execution_order_type
                    ,bh.execution_order_status
                    ,bh.execution_order_vol
                    ,bh.execution_order_price
                    ,bh.position
                    ,bh.cash
                    ,bh.pos_vol
                    ,bh.pos_price
                    ,bh.total_value
                    ,bh.profit_value
                    ,bh.profit_rate
                    from backtest_history as bh
                    left outer join m_strategy as ms
                     on bh.strategy_id = ms.id
                    where bh.symbol = '{symbol}'
                    order by business_date"""

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/index")
def index2():
    return render_template('index.html')

@app.route('/signal')
def signal():
    return 'Investment Signal'

@app.route('/bitmex_xbtusd')
def bitmex_xbtusd():
    rv = query_db(BACKTEST_HISTORY_QUERY.format(symbol='XBTUSD'))
    content_title = "BitMEX XBTUSD Backtest Data"
    return render_template('backtest_history_table.html', content_title=content_title, rv=rv)

@app.route('/bitmex_ethusd')
def bitmex_ethusd():
    rv = query_db(BACKTEST_HISTORY_QUERY.format(symbol='ETHUSD'))
    content_title = "BitMEX ETHUSD Backtest Data"
    return render_template('backtest_history_table.html', content_title=content_title, rv=rv)

@app.route('/minkabu_fx_gbpjpy')
def minkabu_fx_gbpjpy():
    rv = query_db(BACKTEST_HISTORY_QUERY.format(symbol='GBPJPY'))
    content_title = "みん株FX GBPJPY Backtest Data"
    return render_template('backtest_history_table.html', content_title=content_title, rv=rv)

@app.route('/nikkei_topix')
def nikkei_topix():
    return 'nikkei_topix'



