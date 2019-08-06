
from ordertype import OrderType
from orderstatus import OrderStatus

class Order():
    def __init__(self):
        pass

    def set_order(self, create_date, order_type, price, vol):
        self.create_date = create_date
        self.order_date = ''
        self.close_order_date = ''
        self.order_type = order_type
        self.order_status = OrderStatus.BEFORE_ORDER
        self.price = price
        self.vol = vol

    def order(self, order_date):
        self.order_date = order_date
        self.order_status = OrderStatus.ORDERING

    def execution_order(self, close_order_date):
        self.close_order_date = close_order_date
        self.order_status = OrderStatus.EXECUTION

    def fail_order(self):
        self.close_order_date = ''
        self.order_status = OrderStatus.FAIL
