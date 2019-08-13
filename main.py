
import sys
import common
import my_logger
import investment_director

s = my_logger.Logger()
logger = s.myLogger()

if __name__ == '__main__':
    args = sys.argv
    argc = len(args)
    conf = common.read_conf()
    dbfile = conf['dbfile']

    if argc == 1: #ポジション無し
        investment_director.direct_open_order(dbfile)
    elif argc == 3: #ポジション有り
        symbol = args[1]
        position_price = float(args[2])
        investment_director.direct_close_order(dbfile, symbol, position_price)
