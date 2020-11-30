import numpy as np


class Graph:
    def __init__(self, number_of_sites):
        self.n_nodes = number_of_sites + 1
        self.items_at_nodes = {}

        self.transitions = np.full((self.n_nodes, self.n_nodes), np.inf)

        for node in range(1, self.n_nodes + 1):
            self.items_at_nodes[node] = []

    def add_item_to_node(self, node, item_size):
        self.items_at_nodes[node].append(item_size)

    def add_edge(self, node_a, node_b, cost):
        self.transitions[node_a, node_b] = cost
