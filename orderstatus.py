
from enum import IntEnum

class OrderStatus(IntEnum):
    BEFORE_ORDER = 0 #注文前
    ORDERING = 1 #注文中
    FAIL = 2 #未済
    EXECUTION = 3 #約定
