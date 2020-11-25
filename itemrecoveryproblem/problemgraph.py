import numpy as np
import re


class ProblemGraph:
    def __init__(self):
        self.number_nodes = None
        self.robot_capacity = None
        self.items = None
        self.transitions = None


    def load_file(self, path):
        # File is case-insensitive, whitespace not significant, \r\n or \r or \n all accepted, empty lines are ignored
        file = open(path, "r").read().replace(" ", "").replace("\r\n", "\n").replace("\r", "\n").lower().split("\n")
        file = [x for x in file if x != ""]

        if not re.match("nodes:\d", file[0]):
            raise Exception('First line of instance file must be "Nodes: x" where "x" is the number of nodes besides '
                            'the "base" node')
        if not re.match("cargosize:\d", file[1]):
            raise Exception('Second line of instance file must be "CargoSize: x" where "x" is the maximum cargo '
                            'the robot can carry at any given time')
        if not re.match("nodeswithitems:\d", file[2]):
            raise Exception('Third line of instance file must be "NodesWithItems: x" where "x" is the number of nodes'
                            ' that contain items')

        self.number_nodes = int(file[0][6:])
        self.robot_capacity = int(file[1][15:])
        nodes_with_items = int(file[2][1:])

        self.items = {}
        file_idx = 2
        for x in range(0, nodes_with_items):
            line = file[file_idx + x]
            node_idx = int(line.split(":")[0])
            items_in_node = [int(x) for x in line.split(":")[1].split(",")]

            if node_idx > number_nodes:
                raise Exception('Invalid index ' + str(node_idx) + " found in transitions, but only "
                                + str(number_nodes) + " nodes exist.")

            self.items[node_idx] = items_in_node

        print(self.items)

