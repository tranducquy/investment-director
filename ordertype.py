
from enum import Enum

class OrderType(Enum):
    STOP_MARKET_LONG = 0 #逆指値成行買い
    STOP_MARKET_SHORT = 1 #逆指値成行売り
    LIMIT_LONG = 2 #指値成行買い
    LIMIT_SHORT = 3 #指値成行売り
    CLOSE_STOP_MARKET_LONG = 4
    CLOSE_STOP_MARKET_SHORT = 5
