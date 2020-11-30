from itemrecoveryproblem.graph import Graph
import numpy as np
import re


class ItemRecoveryProblem:
    def __init__(self):
        self.graph = None

        self.number_nodes = None
        self.robot_capacity = None
        self.items = None
        self.number_edges = None
        self.transitions = None

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
        if not re.match(r"nodeswithitems:\d+$", file[2]):
            raise Exception('Third line of instance file must be "NodesWithItems: x" where "x" is the number of nodes'
                            ' that contain items')

        self.graph = Graph(int(file[0][6:]))
        self.robot_capacity = int(file[1][10:])

        nodes_with_items = int(file[2][15:])

        self.items = {}
        file_idx = 3
        for x in range(0, nodes_with_items):
            line = file[file_idx + x]

            if not re.match(r"\d:(\d+)(,\d+)*$", line):
                raise Exception('Please specify the items at each node with the following format: "x: a,b,c,...",'
                                ' where x is the node and a,b,c... are the sizes of the items at that node')

            node_idx = int(line.split(":")[0])
            items_in_node = [int(x) for x in line.split(":")[1].split(",")]

            if node_idx > self.number_nodes:
                raise Exception('Invalid index ' + str(node_idx) + " found in transitions, but only "
                                + str(self.number_nodes) + " nodes exist.")

            self.items[node_idx] = items_in_node
        file_idx = file_idx + nodes_with_items

        # Sanity check - No item can be bigger than the cargo
        biggest_item_size_in_graph = 0
        for node_items in self.items.values():
            biggest_item_size_in_node = max(node_items)
            if biggest_item_size_in_node > biggest_item_size_in_graph:
                biggest_item_size_in_graph = biggest_item_size_in_node

        if re.match("edges:\d+$", file[file_idx]):
            self.number_edges = int(file[file_idx][6:])
        else:
            raise Exception('Number of edges of the graph must be indicated after specifying the items at each node. '
                            'Format: "Edges: x"')

        self.transitions = np.full((self.number_nodes, self.number_nodes), np.inf)

        file_idx += 1
        for x in range(0, self.number_edges):
            line = file[file_idx + x]

            if re.match("\d+,\d+:\d+$", line):
                line = re.split(",|:", line)
                if int(line[0]) > (self.number_nodes-1):
                    raise Exception('Invalid edge. Node ' + line[0] + ' does not exist.')
            else:
                raise Exception('Invalid format for specifying an edge. Format: "x,y: z", where x and y'
                                ' are nodes and z is the cost of the edge')

