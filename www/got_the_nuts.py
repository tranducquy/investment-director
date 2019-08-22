
from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

DATABASE = '/usr/local/investment-director/market-history.db'

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

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/bitmex_xbtusd')
def bitmex_xbtusd():
    db = get_db()
    rv = query_db("select * from backtest_history where symbol = 'XBTUSD'")
    return render_template('tables.html')

@app.route('/bitmex_ethusd')
def bitmex_ethusd():
    return 'bitmex_ethusd'

@app.route('/minkabu_fx_gbpjpy')
def minkabu_fx_gbpjpy():
    return 'minkabu_fx_gbpjpy'

@app.route('/nikkei_topix')
def nikkei_topix():
    return 'nikkei_topix'



