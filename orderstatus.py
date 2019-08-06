
from enum import Enum

class OrderStatus(Enum):
    BEFORE_ORDER = 0 #注文前
    ORDERING = 1 #注文中
    FAIL = 2 #未済
    EXECUTION = 3 #約定
