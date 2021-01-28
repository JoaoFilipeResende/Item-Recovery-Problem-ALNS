import random
from itemrecoveryproblem.graph import Graph
import os


def instance_gen(number_of_sites, cargo_size, max_items_in_site, max_edges_in_site, min_cost, max_cost, min_item_size, max_item_size):

    if cargo_size < max_item_size:
        raise Exception("Maximum item size is bigger then the cargo size!")

    graph = Graph(number_of_sites)

    for site in range(1, number_of_sites + 1):
        items_in_site = random.randrange(max_items_in_site)

        for item in range(items_in_site):
            item_size = random.randrange(min_item_size, max_item_size)
            graph.add_item_to_node(site, item_size)

    for site in range(number_of_sites + 1):

        for _ in range(random.randrange(1, max_edges_in_site)):
            dst = random.randint(0, number_of_sites)
            while (dst == site) and (not graph.edge_exists(site, dst)):
                dst = random.randint(0, number_of_sites)

            cost = random.randrange(min_cost, max_cost)
            graph.add_edge(site, dst, cost)
            graph.add_edge(dst, site, cost)

    file = graph.print_graph(cargo_size)

    return file


if __name__ == '__main__':

    for instance in range(40, 105, 5):
        number_of_sites = instance
        cargo_size = random.randint(2, 10)
        max_items_in_site = random.randint(5, 10)
        max_edges_in_site = random.randint(2, 5)
        min_cost = random.randint(1, 6)
        max_cost = random.randint(10, 20)
        min_item_size = 1
        max_item_size = random.randint(2, cargo_size)

        output = instance_gen(number_of_sites, cargo_size, max_items_in_site, max_edges_in_site, min_cost, max_cost, min_item_size, max_item_size)

        f = open(os.path.join(os.curdir, "instances", "instance_"+str(instance)), "w")

        f.write(output)
        f.close()
