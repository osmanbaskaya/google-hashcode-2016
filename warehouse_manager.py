from Queue import Queue

from drone import DeliveryDrone, AssistantDrone
from simulation import Simulation
from warehouse import Warehouse
import sys
from data_reader import read_data
from kmeans import assign_orders_and_drones_to_warehouses


class WarehouseManager(object):

    def __init__(self, num_of_drones, warehouse_drone_nums, warehouse_order_ids, warehouse_info, order_info, drone_load):
        self.warehouses = WarehouseManager.create_warehouses(warehouse_info)
        self.delivery_drones, self.assistant_drones = self.initialize_drones(num_of_drones,
                                                                                         warehouse_drone_nums,
                                                                                         self.warehouses)
        self.assign_orders_to_warehouse(warehouse_order_ids)
        self.simulation = Simulation()
        self.order_info = order_info
        self.drone_load = drone_load

    @staticmethod
    def create_warehouses(warehouse_info):
        return [Warehouse(i, w['loc'], w['stock']) for i, w in enumerate(warehouse_info.values())]

    def initialize_drones(self, num_of_drones, warehouse_drone_nums, warehouses):
        delivery_drones = []
        assistant_drones = []
        i = 0
        for w_id, (delivery_drone_count, assistant_drone_count) in warehouse_drone_nums.iteritems():
            delivery_drone_count = int(delivery_drone_count)
            assistant_drone_count = int(assistant_drone_count)
            ddrones = [DeliveryDrone(c) for c in xrange(i, i+delivery_drone_count)]
            map(lambda d: self.simulation.schedule_event(d.go(warehouses[w_id].loc)), ddrones)
            delivery_drones.extend(ddrones)
            i += delivery_drone_count
            asdrones = [AssistantDrone(c) for c in xrange(i, i+assistant_drone_count)]
            map(lambda d: self.simulation.schedule_event(d.go(warehouses[w_id].loc)), asdrones)
            assistant_drones.extend(ddrones)
            i += assistant_drone_count
            # TODO: It seems like this is an error (syntactically)
            warehouses[w_id].assign_drones(ddrones + asdrones)
        return delivery_drones, assistant_drones

    def assign_orders_to_warehouse(self, warehouse_order_ids):
        for warehouse_id, orders in warehouse_order_ids.iteritems():
            self.warehouses[warehouse_id].assign_orders(orders)

    def schedule_remaining_orders_in_the_warehouse(self, warehouse):
        drones = warehouse.drones
        unassigned_drones = Queue()
        for drone in drones:
            unassigned_drones.put(drone)
        orders = warehouse.orders
        inventory = warehouse.stock

        def is_satisfiable(order):
            order_as_array = [self.order_info[order][product_id] for product_id in self.order_info[order].keys()]
            return all(map(lambda x: x[0] >= x[1], zip(inventory, order_as_array)))

        for order in orders:
            if is_satisfiable(order):
                next_unassigned_drone = unassigned_drones.get()
                if next_unassigned_drone





    def start_delivering(self, order_info):
        for warehouse in self.warehouses:
            for order in warehouse.orders:
                if order in warehouse.stock:
                    warehouse.drones.deliver


def main():
    simulation_parameters, weights, warehouse_info, order_info, order_location_matrix = read_data(sys.argv[1])
    r, c, d, sim_deadline, drone_load = simulation_parameters
    warehouse_drone_nums, warehouse_order_ids = assign_orders_and_drones_to_warehouses(simulation_parameters, weights,
                                                                                      warehouse_info,
                                                                                      order_info, order_location_matrix)
    manager = WarehouseManager(d, warehouse_drone_nums, warehouse_order_ids, warehouse_info, order_info, drone_load)
    manager.start_delivering(order_info)


if __name__ == '__main__':
    main()
