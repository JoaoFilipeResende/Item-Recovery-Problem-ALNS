from itemrecoveryproblem.graph import Graph
import numpy as np
import re


class ItemRecoveryProblem:
    def __init__(self):
        self.graph = None

        self.robot_cargo_size = None
        self.items = None
        self.number_edges = None

    def load_file(self, path):
        # File is case-insensitive, whitespace not significant, \r\n or \r or \n all accepted, empty lines are ignored
        file = open(path, "r").read().replace(" ", "").replace("\r\n", "\n").replace("\r", "\n").lower().split("\n")
        file = [x for x in file if x != ""]

        if not re.match(r"sites:\d+$", file[0]):
            raise Exception('First line of instance file must be "Sites: x" where "x" is the number of sites besides '
                            'the "base"')
        if not re.match(r"cargosize:\d+$", file[1]):
            raise Exception('Second line of instance file must be "CargoSize: x" where "x" is the maximum cargo '
                            'the robot can carry at any given time')
        if not re.match(r"siteswithitems:\d+$", file[2]):
            raise Exception('Third line of instance file must be "SitesWithItems: x" where "x" is the number of sites'
                            ' that contain items')

        number_of_sites = int(file[0][6:])
        self.graph = Graph(number_of_sites)
        self.robot_cargo_size = int(file[1][10:])

        sites_with_items = int(file[2][15:])

        self.items = {}
        file_idx = 3
        for x in range(0, sites_with_items):
            line = file[file_idx + x]

            if not re.match(r"\d:(\d+)(,\d+)*$", line):
                raise Exception('Please specify the items at each site with the following format: "x: a,b,c,...",'
                                ' where x is the site and a,b,c... are the sizes of the items at that site')

            site_idx = int(line.split(":")[0])

            if site_idx == 0:
                raise Exception('Invalid site 0 in item specification. Site 0 is the "base" and cannot have items')

            if site_idx > number_of_sites:
                raise Exception('Invalid site ' + str(site_idx) + ' in item specification.')

            for item_size in line.split(":")[1].split(","):
                if int(item_size) < self.robot_cargo_size:
                    self.graph.add_item_to_node(site_idx, int(item_size))
                else:
                    raise Exception('Items cannot exceed the cargo capacity.')

        file_idx = file_idx + sites_with_items

        if re.match("paths:\d+$", file[file_idx]):
            self.number_edges = int(file[file_idx][6:])
        else:
            raise Exception('Number of paths between sites must be indicated after specifying the items at each site. '
                            'Format: "Paths: x", where x is the number of paths between sites')

        file_idx += 1
        for x in range(0, self.number_edges):
            line = file[file_idx + x]

            if re.match("\d+,\d+:\d+$", line):
                line = re.split(",|:", line)
                if int(line[0]) > number_of_sites:
                    raise Exception('Invalid path. Site ' + line[0] + ' does not exist.')
                if int(line[1]) > number_of_sites:
                    raise Exception('Invalid path. Site ' + line[1] + ' does not exist.')
                if not self.graph.edge_exists(int(line[0]), int(line[1])):
                    self.graph.add_edge(int(line[0]), int(line[1]), int(line[2]))
                    self.graph.add_edge(int(line[1]), int(line[0]), int(line[2]))
                else:
                    raise Exception(
                        'Multiple declaration between site ' + line[0] + ' and ' + line[1] + '.')
            else:
                raise Exception('Invalid format for specifying an edge. Format: "x,y: z", where x and y'
                                ' are nodes and z is the cost of the edge')

        for site in range(0, number_of_sites + 1):
            self.graph.add_edge(site, site, 0)

    def get_items_at_all_sites(self):
        return self.graph.get_items_at_nodes()

    def get_items_at_site(self, site_index):
        return self.graph.get_items_at_nodes()[site_index]

    def get_robot_cargo_size(self):
        return self.robot_cargo_size

    # Returns None if sites are not connected
    def get_cost_between_adjacent_sites(self, site_a, site_b):
        return self.graph.get_edge_cost(site_a, site_b)
