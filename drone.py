
class Drone(object):

    def __init__(self, id):
        self.current_loc = (0, 0)
        self.drone_id = id
        self.weight = 0
        self.warehouse = None

    def assign_to_warehouse(self, warehouse):
        self.warehouse = warehouse

    def go(self, loc):
        self.current_loc = loc

    def load(self, product_types, counts):
        self.go(self.warehouse.loc)
        for t, c in zip(product_types, counts):
            print "{} L {} {} {}".format(self.drone_id, self.warehouse.id, t, c)

    def wait(self, num_turn):
        print "{} W {}".format(self.drone_id, num_turn)


class DeliveryDrone(Drone):

    def deliver(self, order, product_types, counts):
        self.go(order.loc)
        for t, c in zip(product_types, counts):
            print "{} D {} {} {}".format(self.drone_id, order.id, t, c)


class AssistantDrone(Drone):

    def deliver(self, product_types, counts):
        self.go(self.warehouse.loc)
        for t, c in zip(product_types, counts):
            print "{} U {} {} {}".format(self.drone_id, self.warehouse.id, t, c)
