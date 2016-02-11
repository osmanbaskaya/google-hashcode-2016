from math import floor

from sklearn.cluster import KMeans
import numpy as np
from collections import defaultdict as dd

from data_reader import read_data

def find_centers(orders, n_warehouses):

    k_means = KMeans(n_clusters=n_warehouses)

    k_means.fit(orders)
    # print k_means.cluster_centers_
    return k_means, k_means.predict(orders)


def find_closest_warehouse(cluster_centers_, warehouse_location_matrix):
    warehouses = []
    for center in cluster_centers_:
        dist = map(lambda x: np.sqrt(np.sum((center-x)**2)), warehouse_location_matrix)
        # print np.argmin(dist)
        # print dist
        warehouses.append(np.argmin(dist))
    return warehouses

def assign_orders_and_drones_to_warehouses(simulation_parameters, weights, warehouse_info, order_info, order_location_matrix):
    #
    # print order_location_matrix
    kmeans, cluster_assignments = find_centers(order_location_matrix, len(warehouse_info))
    warehouse_location_matrix = np.array([w['loc'] for w in warehouse_info.values()])
    # print warehouse_location_matrix
    # print kmeans.predict(warehouse_location_matrix)

    cluster_to_warehouses = find_closest_warehouse(kmeans.cluster_centers_, warehouse_location_matrix)
    warehouses_to_orders = dd(lambda: dict())
    warehouses_order_ids = dd(lambda: dict())
    warehouses_drone_numbers = dd(lambda: dict())
    total_order_weight = sum([order['weight'] for order in order_info.values()])
    # print total_order_weight
    # print simulation_parameters[2]
    for (cluster, warehouse) in enumerate(cluster_to_warehouses):
        assigned_orders = [order for (order, assignment) in enumerate(cluster_assignments) if assignment == cluster]
        total_order_weight_for_warehouse = sum([order_info[order]['weight'] for order in assigned_orders])
        # print total_order_weight_for_warehouse
        warehouses_to_orders[warehouse]['orders'] = [order for order in assigned_orders]
        warehouses_order_ids[warehouse] = [order for order in assigned_orders]
        warehouses_to_orders[warehouse]['n_drones'] = floor(float(total_order_weight_for_warehouse)/total_order_weight*simulation_parameters[2])
        warehouses_drone_numbers[warehouse] = [None, None]
        warehouses_drone_numbers[warehouse][0] = floor(float(total_order_weight_for_warehouse)/float(total_order_weight+len(warehouse_info))*simulation_parameters[2])
        warehouses_drone_numbers[warehouse][1] = floor((1-float(total_order_weight_for_warehouse)/float(total_order_weight+len(warehouse_info)))*simulation_parameters[2])
        # print warehouses_to_orders[warehouse]
        # print len(warehouses_to_orders[warehouse])

    #print warehouses_to_orders
    return warehouses_drone_numbers, warehouses_order_ids

if __name__ == "__main__":
    simulation_parameters, weights, warehouse_info, order_info, order_location_matrix = read_data("busy_day.in")
    assign_orders_and_drones_to_warehouses(simulation_parameters, weights, warehouse_info, order_info, order_location_matrix)






