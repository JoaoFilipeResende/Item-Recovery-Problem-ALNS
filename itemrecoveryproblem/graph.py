

class Graph:
    def __init__(self, number_of_nodes):
        self.n_nodes = number_of_nodes

        for node in range(1, self.n_nodes):
            self.items_at_nodes[node] = []

    def add_item_to_node(self, node, item_size):
        self.items_at_nodes[node].append(item_size)