import random
from itemrecoveryproblem.graph import Graph
import os

number_of_sites = 100
cargo_size = 18
max_items_in_site = 8
max_edges_in_site = 3
min_cost = 1
max_cost = 25
min_item_size = 1
max_item_size = 8

graph = Graph(number_of_sites)

for site in range(1, number_of_sites+1):
    items_in_site = random.randrange(max_items_in_site)

    for item in range(items_in_site):
        item_size = random.randrange(min_item_size, max_item_size)
        graph.add_item_to_node(site, item_size)

for site in range(number_of_sites+1):

    for _ in range(random.randrange(1, max_edges_in_site)):
        dst = random.randint(0, number_of_sites)
        while (dst == site) and (not graph.edge_exists(site, dst)):
            dst = random.randint(0, number_of_sites)

        cost = random.randrange(min_cost, max_cost)
        graph.add_edge(site, dst, cost)
        graph.add_edge(dst, site, cost)

file = graph.print_graph(cargo_size)

f = open(os.path.join(os.curdir, "instances", "instance_38"), "w")
f.write(file)
f.close()

