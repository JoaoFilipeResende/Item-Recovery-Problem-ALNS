class Solution:
    def __init__(self):
        # List of site indexes that the solution comprises
        self.path = []

        # List containing lists of items picked up along the path.
        # Must be the same size as "self.path" and can contain empty lists
        self.items_picked = []

    def is_valid(self, item_recovery_problem):
        items_at_each_site = item_recovery_problem.get_items_at_each_site()
        max_cargo = item_recovery_problem.get_robot_cargo_size()
        robot_cargo = []

        # Path must always begin and end at the base
        if (self.path[0] != 0) or (self.path[-1] != 0):
            return False

        for path_idx in range(0, len(self.path)):
            site = self.path[path_idx]
            if site == 0:
                robot_cargo = []
            else:
                for item_idx in self.items_picked[site]:
                    item_size = items_at_each_site[site][item_idx]
                    items_at_each_site[site][item_idx] = 0  # A zero means that item was picked up
                    robot_cargo.append(item_size)
                    if sum(robot_cargo) > max_cargo:
                        return False

        for items_idx in range(1, len(items_at_each_site)):
            items = items_at_each_site[items_idx]
            if sum(items) != 0:
                return False
        return True

    def get_cost(self, item_recovery_problem):
        prev_site = self.path[0]
        cost = 0
        for idx in range(1, len(self.path)):
            current_site = self.path[idx]
            cost += item_recovery_problem.get_path_cost(prev_site, current_site)
        return cost

    def insert(self, index, new_path, new_items_picked):
        if len(new_path) != len(new_items_picked):
            raise Exception("Tried to insert a path into the solution but length of new sites and length of items"
                            " picked did not match the path length")

        for i in range(0, len(new_path)):
            self.path.insert(index + i, new_path[i])
            self.items_picked.insert(index + i, new_path[i])
