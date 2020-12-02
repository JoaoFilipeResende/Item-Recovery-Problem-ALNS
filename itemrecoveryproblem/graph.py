import numpy as np
import heapq


class Graph:
    def __init__(self, number_of_sites):
        self.n_nodes = number_of_sites + 1
        self.items_at_nodes = {}

        self.edges = np.full((self.n_nodes, self.n_nodes), np.inf)

        for node in range(1, self.n_nodes + 1):
            self.items_at_nodes[node] = []

    def add_item_to_node(self, node, item_size):
        self.items_at_nodes[node].append(item_size)

    def add_edge(self, node_a, node_b, cost):
        self.edges[node_a, node_b] = cost

    def edge_exists(self, node_a, node_b):
        return self.edges[node_a, node_b] != np.inf

    def shortest_path(self, start, destination):
        shortest_dist = np.full(self.n_nodes, np.inf)
        prev = [None] * self.n_nodes
        processed_nodes = [False] * self.n_nodes
        priority_queue = []

        shortest_dist[start] = 0

        for node in range(self.n_nodes):
            heapq.heappush(priority_queue, (shortest_dist[node], node))

        while not processed_nodes[destination]:
            node_dist, node = heapq.heappop(priority_queue)
            processed_nodes[node] = True

            for neighbor in range(self.n_nodes):
                if (processed_nodes[neighbor] is False) and (self.edges[node, neighbor] != np.inf):
                    dist_to_neighbor = node_dist + self.edges[node, neighbor]
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
