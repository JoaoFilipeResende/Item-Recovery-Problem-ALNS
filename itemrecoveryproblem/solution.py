
class Solution:
    def __init__(self, item_recovery_problem):

        self._irp = item_recovery_problem

        # List of site indexes that the solution comprises
        self._path = [0]

        # A list of solution states. Each state is *after* the robot picks up the items
        self._solution_states = []

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

        first_state = SolutionState()
        first_state.remaining_items_per_site = self._irp.get_items_at_each_site()
        first_state.accumulated_cost = 0

        self._solution_states.append(first_state)

    # Returns a tuple of Bool, Index, where the bool indicates if the solution is valid.
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
                if self._irp.get_cost_between_adjacent_sites(self.path[idx-1], self.path[idx]):
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

    # TODO: WIP
    def insert_subpath(self, insertion_index, subpath, subpath_items_picked):
        if len(subpath) != len(subpath_items_picked):
            raise Exception("Tried to insert a path into the solution but length of new sites and length of items"
                            " picked did not match the path length")
        pass

        for i in range(0, len(subpath)):
            self._path.insert(insertion_index + i, subpath[i])
            self._solution_states.insert(insertion_index + i, self.SolutionState())
            current_state = self._solution_states[i]

            if (insertion_index + i) == 0:
                if subpath[0] != 0:
                    raise Exception("Attempted to insert subpath at the beginning of the solution, but subpath"
                                    " starts at site ", subpath[0], " and not at the base (site 0)")
                if subpath_items_picked[0]:
                    raise Exception("Attempted to insert subpath at the beginning of the solution, and items to be"
                                    " picked were specified, which is not possible at the base (site 0)")

                current_state.items_picked = []
                current_state.remaining_items_per_site = self._irp.get_items_at_each_site()
                current_state.robot_cargo = []
                current_state.accumulated_cost = 0
            else:
                prev_state = self._solution_states[insertion_index + i - 1]
                current_state.items_picked = subpath_items_picked[i]
                current_state.remaining_items_per_site = prev_state.remaining_items_per_site

                if subpath[i] == 0:
                    if subpath_items_picked[i]:
                        raise Exception("Attempted to insert subpath that picks up items at site 0")
                    current_state.robot_cargo = []
                else:
                    for item_idx in subpath_items_picked[i]:
                        current_state.robot_cargo.append(current_state.remaining_items_per_site[subpath[i]][item_idx])
                        current_state.remaining_items_per_site[subpath[i]][item_idx] = 0

                try:
                    current_state.accumulated_cost = prev_state.accumulated_cost \
                                       + self._irp.get_cost_between_adjacent_sites(self._path[insertion_index + i - 1],
                                                                                   self._path[insertion_index + i])
                except TypeError():
                    current_state.accumulated_cost = float('+inf')

        # Propagate changes along the path after the insertion
        for path_idx in range(insertion_index + len(subpath), len(self._path)):
            prev_state = self._solution_states[path_idx - 1]
            current_state = self._solution_states[path_idx]

            current_state.remaining_items_per_site = prev_state.remaining_items_per_site

            if self._path[path_idx] == 0:
                current_state.robot_cargo = []
                continue

            current_state.robot_cargo = prev_state.robot_cargo

            new_items_picked = []
            for item_picked in current_state.items_picked:
                if current_state.remaining_items_per_site[self._path[path_idx]][item_picked] != 0:
                    new_items_picked.append(item_picked)
                    current_state.robot_cargo.append(current_state.remaining_items_per_site[self._path[path_idx]]
                                                     [item_picked])
                    current_state.remaining_items_per_site[self._path[path_idx]][item_picked] = 0

            current_state.items_picked = new_items_picked

    # TODO: WIP
    # Updates remaining items, robot cargo and accumulated cost along the path, from "index" to its end
    # Assumes that the items picked at each
    def rectify_solution(self, index):
        pass
