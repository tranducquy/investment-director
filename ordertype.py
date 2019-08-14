
from enum import Enum

class OrderType(Enum):
    NONE_ORDER = 0 
    STOP_MARKET_LONG = 1 #逆指値成行買い
    STOP_MARKET_SHORT = 2 #逆指値成行売り
    LIMIT_LONG = 3 #指値成行買い
    LIMIT_SHORT = 4 #指値成行売り
    CLOSE_STOP_MARKET_LONG = 5 #逆指値成行買い返済
    CLOSE_STOP_MARKET_SHORT = 6 #逆指値売り返済
    CLOSE_MARKET_LONG = 7 #成行買い返済
    CLOSE_MARKET_SHORT = 8 #成行売り返済
