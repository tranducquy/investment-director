
import sys
from argparse import ArgumentParser
import common
import my_logger
import investment_director

s = my_logger.Logger()
logger = s.myLogger()

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-o', '--symbol_file', type=str, help='Absolute/relative path to input file')
    argparser.add_argument('-c', '--symbol', type=str, help='Close symbol')
    argparser.add_argument('-b', '--business_date', type=str, help='Date of signal')
    argparser.add_argument('-p', '--position', type=str, help='current position')
    argparser.add_argument('-f', '--position_price', type=float, help='position open price')
    args = argparser.parse_args()
    return args

if __name__ == '__main__':
    args = sys.argv
    argc = len(args)
    conf = common.read_conf()
    dbfile = conf['dbfile']
    args = get_option()
    if args.symbol is None:
        symbol_txt = conf['symbol']
    else:
        symbol_txt = args.symbol_file
    if args.position is None: #ポジションなし
        investment_director.direct_open_order(dbfile, symbol_txt)
    else:
        symbol = args.symbol
        position = args.position # long or short
        position_price = float(args.position_price)
        investment_director.direct_close_order(dbfile, symbol, position, position_price)
