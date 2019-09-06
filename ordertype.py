
from enum import IntEnum

class OrderType(IntEnum):
    NONE_ORDER = 0 
    STOP_MARKET_LONG = 1 #逆指値成行買い
    STOP_MARKET_SHORT = 2 #逆指値成行売り
    LIMIT_LONG = 3 #指値成行買い
    LIMIT_SHORT = 4 #指値成行売り
    CLOSE_STOP_MARKET_LONG = 5 #逆指値成行返売(longを返済)
    CLOSE_STOP_MARKET_SHORT = 6 #逆指値成行返買(shortを返済)
    CLOSE_MARKET_LONG = 7 #成行返売(longを返済)
    CLOSE_MARKET_SHORT = 8 #成行返買(shortを返済)
    MARKET_LONG = 9 #成行買い
    MARKET_SHORT = 10 #成行売り
    CLOSE_LIMIT_LONG = 11 #指値返売(longを返済)
    CLOSE_LIMIT_SHORT = 12 #指値返買(shortを返済)
