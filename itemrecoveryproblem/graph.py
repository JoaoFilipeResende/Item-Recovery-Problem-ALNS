import numpy as np
import heapq


class Graph:
    def __init__(self, number_of_sites):
        self._n_nodes = number_of_sites + 1
        self._items_at_nodes = []

        self._edges = np.full((self._n_nodes, self._n_nodes), np.inf)

        self._items_at_nodes.append(None)
        for node in range(1, self._n_nodes):
            self._items_at_nodes.append([])

    def add_item_to_node(self, node, item_size):
        self._items_at_nodes[node].append(item_size)

    def add_edge(self, node_a, node_b, cost):
        self._edges[node_a, node_b] = cost

    def edge_exists(self, node_a, node_b):
        return self._edges[node_a, node_b] != np.inf

    def get_items_at_nodes(self):
        return self._items_at_nodes

    # Returns None if nodes are not connected
    def get_edge_cost(self, node_a, node_b):
        cost = self._edges[node_a, node_b]
        if cost == np.inf:
            return None
        else:
            return cost

    def shortest_path(self, start, destination):
        shortest_dist = np.full(self._n_nodes, np.inf)
        prev = [None] * self._n_nodes
        processed_nodes = [False] * self._n_nodes
        priority_queue = []

        shortest_dist[start] = 0

        for node in range(self._n_nodes):
            heapq.heappush(priority_queue, (shortest_dist[node], node))

        while not processed_nodes[destination]:
            node_dist, node = heapq.heappop(priority_queue)
            processed_nodes[node] = True

            for neighbor in range(self._n_nodes):
                if (processed_nodes[neighbor] is False) and (self._edges[node, neighbor] != np.inf):
                    dist_to_neighbor = node_dist + self._edges[node, neighbor]
                    if dist_to_neighbor < shortest_dist[neighbor]:
                        shortest_dist[neighbor] = dist_to_neighbor
                        prev[neighbor] = node

                        for index, elem in enumerate(priority_queue):
                            if elem[1] == neighbor:
                                priority_queue[index] = (dist_to_neighbor, neighbor)
                                break
                        heapq.heapify(priority_queue)
        path = [destination]
        while path[-1] != start:
            path.append(prev[path[-1]])
        path.reverse()
        return path

    def print_graph(self, cargo_size):
        sites_with_items = 0
        num_of_paths = 0

        output = "Sites: " + str(self._n_nodes - 1) + "\n"
        output += "CargoSize: " + str(cargo_size) + "\n"

        str_items = ""
        for node in range(1, self._n_nodes):
            if self._items_at_nodes[node]:
                str_items += str(node) + ": "
                sites_with_items += 1
                for item in self._items_at_nodes[node]:
                    str_items += str(item) + ","
                str_items = str_items[:-1] + "\n"

        str_path = ""
        for node_a in range(self._n_nodes):
            for node_b in range(node_a, self._n_nodes):
                if self.edge_exists(node_a,node_b):
                    num_of_paths += 1
                    str_path += str(node_a) + "," + str(node_b) + ": " + str(int(self.get_edge_cost(node_a,node_b))) + "\n"

        str_num_of_paths = "Paths: " + str(num_of_paths) + "\n"
        output += "SitesWithItems: " + str(sites_with_items) + "\n"

        output += str_items + str_num_of_paths + str_path

        return output