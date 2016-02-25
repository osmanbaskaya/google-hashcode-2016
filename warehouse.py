import math
import numpy as np


def find_distance(loc1, loc2):
    x1, y1 = loc1
    x2, y2 = loc2
    x = x1 - x2
    y = y1 - y2
    return math.sqrt(x ** 2 + y ** 2)


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

    def dist(self, other):
        return find_distance(self.loc, other.loc)

    @staticmethod
    def calc_w2w_distances(warehouses):
        distances = {}
        for w1 in warehouses:
            d = []
            for w2 in warehouses:
                d.append((w1.dist(w2), w2))
            distances[w1.id] = sorted(d)[1:] # skip itself.
        return distances

    @staticmethod
    def find_product_closest_warehouse(product, warehouses):
        warehouse = None
        for _, w in warehouses:
            if w.stock[product] > 0:
                warehouse = w
                break

        assert warehouse is not None, "Product cannot be found which is an error in our calculation"
        return warehouse


class Order(object):

    def __init__(self, id, loc):
        self.loc = loc
        self.id = id
