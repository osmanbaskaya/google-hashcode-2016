class Warehouse(object):

    def __init__(self, id, loc, stock):
        self.loc = loc
        self.id = id
        self.stock = stock

    def assign_orders(self, orders):
        pass


class Order(object):

    def __init__(self, id, loc):
        self.loc = loc
        self.id = id
