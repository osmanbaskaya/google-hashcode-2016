from drone import DeliveryDrone, AssistantDrone
from simulation import Simulation
from warehouse import Warehouse
import sys
from data_reader import read_data
from collections import Counter, defaultdict as dd
from kmeans import assign_orders_and_drones_to_warehouses


class WarehouseManager(object):

    def __init__(self, num_of_drones, warehouse_drone_nums, warehouse_order_ids, warehouse_info):
        self.warehouses = WarehouseManager.create_warehouses(warehouse_info)
        self.delivery_drones, self.assistant_drones = self.initialize_drones(num_of_drones,
                                                                                         warehouse_drone_nums,
                                                                                         self.warehouses)
        self.assign_orders_to_warehouse(warehouse_order_ids)
        self.simulation = Simulation()

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
            warehouses[w_id].assign_drones(ddrones, asdrones)
        return delivery_drones, assistant_drones

    def assign_orders_to_warehouse(self, warehouse_order_ids):
        for warehouse_id, orders in warehouse_order_ids.iteritems():
            self.warehouses[warehouse_id].assign_orders(orders)

    def start_delivering(self, order_info):
        # Not Finished
        for warehouse in self.warehouses:
            for order in warehouse.orders:
                if order in warehouse.stock:
                    pass

    def transfer_remaining_orders_to_warehouses(self):
        # find the closest warehouse pairs.
        w2w_distances = Warehouse.calc_w2w_distances(self.warehouses)
        orders = dd(list)
        for w in self.warehouses:
            for order in w.orders:
                for product in order:
                    # product id
                    w1 = Warehouse.find_product_closest_warehouse(product, w2w_distances[w.id])
                    # key: (from_warehouse, to_warehouse)
                    orders[(w1.id, w.id)].append(product)

        optimized_orders = {}
        for k, order_list in orders.iteritems():
            optimized_orders[k] = Counter(order_list)


def main():
    simulation_parameters, weights, warehouse_info, order_info, order_location_matrix = read_data(sys.argv[1])
    r, c, d, sim_deadline, drone_load = simulation_parameters
    warehouse_drone_nums, warehouse_order_ids = assign_orders_and_drones_to_warehouses(simulation_parameters, weights,
                                                                                      warehouse_info,
                                                                                      order_info, order_location_matrix)
    manager = WarehouseManager(d, warehouse_drone_nums, warehouse_order_ids, warehouse_info)
    manager.start_delivering(order_info)


if __name__ == '__main__':
    main()
