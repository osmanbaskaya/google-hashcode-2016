from drone import Drone
from warehouse import Warehouse
import sys
from data_reader import read_data
from kmeans import assign_orders_to_drones_to_warehouses


class WarehouseManager(object):
    def __init__(self, num_of_drones, warehouse_drone_nums, warehouse_order_ids):
        self.warehouses = WarehouseManager.create_warehouses()
        self.drones = WarehouseManager.initialize_drones(num_of_drones, warehouse_drone_nums, self.warehouses)
        self.assign_orders_to_warehouse(warehouse_order_ids)

    @staticmethod
    def create_warehouses(self, warehouse_info):
        return [Warehouse(i, w['loc'], w['stock']) for i, w in enumerate(warehouse_info)]

    @staticmethod
    def initialize_drones(self, num_of_drones, warehouse_drone_nums, warehouses):
        drones = [Drone(i) for i in num_of_drones]
        i = 0
        for w_id, count in warehouse_drone_nums:
            map(lambda d: d.go(warehouses[w_id]['loc']) in drones[i:count+i])
            i += count
        return drones

    def assign_orders_to_warehouse(self, warehouse_order_ids):
        for warehouse_id, orders in warehouse_order_ids.iteritems():
            self.warehouses[warehouse_id].assign_orders(orders)


def main():
    simulation_parameters, weights, warehouse_info, order_info, order_location_matrix = read_data(sys.argv[1])
    r, c, d, sim_deadline, drone_load = simulation_parameters
    warehouse_drone_nums, warehouse_order_ids = assign_orders_to_drones_to_warehouses(simulation_parameters, weights,
                                                                                      warehouse_info,
                                                                                      order_info, order_location_matrix)
    manager = WarehouseManager(d, warehouse_drone_nums, warehouse_order_ids)


if __name__ == '__main__':
    main()
