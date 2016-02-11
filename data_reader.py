import sys
from collections import defaultdict as dd, Counter
import numpy as np


def read_data(input_file):
    f = open(input_file)
    simulation_parameters = f.readline().split()
    r, c, d, sim_deadline, drone_load = map(int, simulation_parameters)
    simulation_parameters = r, c, d, sim_deadline, drone_load
    num_of_product_type = int(f.readline().split()[0])
    weights = map(int, f.readline().split())
    num_of_warehouse = int(f.readline().split()[0])
    warehouse_info = dd(lambda: dict())
    for i in xrange(num_of_warehouse):
        warehouse_info[i]['loc'] = map(int, f.readline().split())
        warehouse_info[i]['stock'] = map(int, f.readline().split())

    order_info = dd(lambda: dict())
    num_of_orders = int(f.readline().split()[0])
    order_location_matrix = np.zeros((num_of_orders, 2), dtype=np.int)
    for i in xrange(num_of_orders):
        location = map(int, f.readline().split())
        order_info[i]['loc'] = location
        order_location_matrix[i] = location
        f.readline()  # doesn't necessary to read how many product.
        order_info[i]['types'] = Counter(map(int, f.readline().split()))
        order_info[i]['weight'] = sum([weights[order_id] for order_id in order_info[i]['types']])

    return simulation_parameters, weights, warehouse_info, order_info, order_location_matrix


if __name__ == '__main__':
    print read_data(sys.argv[1])

