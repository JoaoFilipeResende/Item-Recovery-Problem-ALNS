import copy


class Solution:
    class SolutionState:

        def __init__(self):
            # A list of item (indexes) picked up at a given site. An empty list means no item is picked up
            # These indexes correspond to the indexes of "ItemRecoveryProblem.get_items_at_each_site()"
            self.items_picked = []

            # A list containing lists of the item sizes at each site.
            # Should always be the return of "ItemRecoveryProblem.get_items_at_each_site()" with zeros where items
            # have been picked up
            self.remaining_items_per_site = []

            # A list containing the sizes of the items that the robot is carrying
            self.robot_cargo = []

            # A variable containing the accumulated cost of the path taken up to this point
            self.accumulated_cost = 0

    # Constructor creates first state at the base
    def __init__(self, item_recovery_problem):

        self._irp = item_recovery_problem

        # List of site indexes that the solution comprises
        self._path = [0]

        # A list of solution states. Each state is *after* the robot picks up the items
        self._solution_states = []

        first_state = self.SolutionState()
        first_state.remaining_items_per_site = self._irp.get_items_at_each_site()
        first_state.accumulated_cost = 0

        self._solution_states.append(first_state)

    # Returns a tuple of (Bool, Int), where the "Bool" indicates if the solution is valid, and "Int" is the index of
    # the path where the first problem that makes the solution invalid occurs
    def check_validity(self):
        max_cargo = self._irp.get_robot_cargo_size()

        # Path must always begin at the base
        if self._path[0] != 0:
            return False, 0

        # The robot can never carry more than the maximum cargo size
        for idx in range(len(self._path)):
            cargo_carried = self._solution_states[idx].robot_cargo
            # Check for cargo overload
            if sum(cargo_carried) > max_cargo:
                return False, idx
            # Check for valid connection between sites
            if idx != 0:
                if self._irp.get_cost_between_adjacent_sites(self.path[idx - 1], self.path[idx]):
                    return False, idx

        # At the end of the solution, no items can remain on any site
        remaining_items = self._solution_states[-1].remaining_items_per_site
        for site_idx in range(1, len(remaining_items)):
            items = remaining_items[site_idx]
            if sum(items) != 0:
                return False, len(self._path) - 1

        # Path must always end at the base
        if self._path[-1] != 0:
            return False, len(self._path) - 1

        return True, None

    def get_cost(self):
        return self._solution_states[-1].accumulated_cost

    def get_path(self):
        return self._path

    # Items picked up at that given site are already excluded from the return of this function
    def get_remaining_items_at_path_index(self, index):
        return self._solution_states[index].remaining_items_per_site

    def get_robot_cargo_at_path_index(self, index):
        return self._solution_states[index].robot_cargo

    def get_accumulated_cost_at_path_index(self, index):
        return self._solution_states[index].accumulated_cost

    def append_subpath(self, subpath, subpath_items_picked):
        if len(subpath) != len(subpath_items_picked):
            raise Exception("Tried to append a path into the solution but length of new sites and length of items"
                            " picked did not match the path length")

        original_path_length = len(self._path)

        for i in range(0, len(subpath)):
            self._path.append(subpath[i])
            self._solution_states.append(self.SolutionState())
            self._solution_states[-1].items_picked = subpath_items_picked[i]

        self._rectify_solution(start_idx=original_path_length)
        return

    def insert_subpath(self, insertion_index, subpath, subpath_items_picked):
        if len(subpath) != len(subpath_items_picked):
            raise Exception("Tried to insert a path into the solution but length of new sites and length of items"
                            " picked did not match the path length")

        for i in range(0, len(subpath)):
            self._path.insert(insertion_index + i, subpath[i])
            self._solution_states.insert(insertion_index + i, self.SolutionState())
            self._solution_states[insertion_index + i].items_picked = subpath_items_picked[i]

        self._rectify_solution(start_idx=insertion_index)
        return

    # Updates remaining items, robot cargo and accumulated cost along the path, from "start_idx" to its end, according
    # to the items picked at each node
    def _rectify_solution(self, start_idx=0):

        if start_idx == 0:
            if self._solution_states[0].items_picked:
                raise Exception("Attempt to pick up items at the base detected when rectifying the solution")
            self._solution_states[0].remaining_items_per_site = self._irp.get_items_at_each_site()
            self._solution_states[0].robot_cargo = []
            self._solution_states[0].accumulated_cost = 0
            start_idx += 1

        for path_idx in range(start_idx, len(self._path)):
            prev_state = self._solution_states[path_idx - 1]
            current_state = self._solution_states[path_idx]

            # Update accumulated cost
            cost_prev_current_sites = self._irp.get_cost_between_adjacent_sites(self._path[path_idx - 1],
                                                                                self._path[path_idx])
            if cost_prev_current_sites is None:
                # Inserting unconnected sites results in infinite cost and in an invalid solution
                current_state.accumulated_cost = float('+inf')
            else:
                current_state.accumulated_cost = prev_state.accumulated_cost + cost_prev_current_sites

            # Update remaining items per site and the robot cargo
            current_state.remaining_items_per_site = copy.deepcopy(prev_state.remaining_items_per_site)
            if self._path[path_idx] == 0:
                current_state.robot_cargo = []
                if current_state.items_picked:
                    raise Exception("Attempt to pick up items at the base detected when rectifying the solution")
            else:
                current_state.robot_cargo = prev_state.robot_cargo
                # Some items may have already been picked up before, so this also removes items that were already picked
                new_items_picked = []
                for item_picked in current_state.items_picked:
                    if current_state.remaining_items_per_site[self._path[path_idx]][item_picked] != 0:
                        new_items_picked.append(item_picked)
                        current_state.robot_cargo.append(current_state.remaining_items_per_site[self._path[path_idx]]
                                                         [item_picked])
                        current_state.remaining_items_per_site[self._path[path_idx]][item_picked] = 0

                current_state.items_picked = new_items_picked



