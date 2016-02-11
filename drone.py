
class Drone(object):

    def __init__(self, id):
        self.current_loc = (0, 0)
        self.drone_id = id
        self.weight = 0

    def go(self, loc):
        self.current_loc = loc

    def load(self, warehouse, product_types, counts):
        self.go(warehouse.loc)
        for t, c in zip(product_types, counts):
            print "{} L {} {} {}".format(self.drone_id, warehouse.id, t, c)

    def unload(self, warehouse, product_types, counts):
        self.go(warehouse.loc)
        for t, c in zip(product_types, counts):
            print "{} U {} {} {}".format(self.drone_id, warehouse.id, t, c)

    def deliver(self, order, product_types, counts):
        self.go(order.loc)
        for t, c in zip(product_types, counts):
            print "{} D {} {} {}".format(self.drone_id, order.id, t, c)

    def wait(self, num_turn):
        print "{} W {}".format(self.drone_id, num_turn)
