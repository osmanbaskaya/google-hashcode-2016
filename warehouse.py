class Warehouse(object):

    def __init__(self, id, loc, stock):
        self.loc = loc
        self.id = id
        self.stock = set(stock)
        self.orders = None
        self.drones = None

    def assign_orders(self, orders):
        self.orders = orders

    def assign_drones(self, drones):
        self.orders = drones



class Order(object):

    def __init__(self, id, loc):
        self.loc = loc
        self.id = id
