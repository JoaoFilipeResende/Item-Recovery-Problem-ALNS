import numpy as np
from copy import deepcopy


# Randomly removes between 10% and 60% of all subpaths in the solution
def remove_rand_sps(solution, random_state):
    return solution


# Orders subpaths by the normalized (total item size retrieved) / cost and
def remove_sps_by_dispatch_rule(solution, random_state):
    return solution


# Splits between 10% and 60% of all subpaths
def split_sps(solution, random_state):
    return solution


# Randomly swap subpaths
def swap_sps(solution, random_state):
    return solution


def greedy_repair(solution, random_state):
    is_valid, problem_index = solution.check_validity()

    # TODO: uncomment this later
    # if is_valid:
    #    print("Warning: A valid solution was passed to the greedy_repair() method")
    #    return solution

    # First, randomly remove items in subpaths until the carry weight is no longer exceeded in those subpaths
    subpath_indexes = np.where(np.array(solution.get_path()) == 0)[0]
    subpaths_to_check = np.where(subpath_indexes >= problem_index)[0]
    max_cargo = solution.get_irp_instance().get_robot_cargo_size()

    for i in range(len(subpaths_to_check) - 1):
        items_carried_at_subpath_end = solution.get_robot_cargo_at_path_index(subpaths_to_check[i + 1] - 1)
        cargo = sum(items_carried_at_subpath_end)
        if cargo > max_cargo:
            item_tuple_list = [] # List containing tuples of (item weight, item idx, path index where item is picked up)
            for path_idx in range(subpaths_to_check[i], subpaths_to_check[i+1]):
                items_picked_up_at_path_idx = solution.get_items_picked_up_at_path_index(path_idx)
                for j in range(len(items_picked_up_at_path_idx)):
                    item_index = items_picked_up_at_path_idx[j]
                    item_weight = solution.get_irp_instance().get_items_at_site(solution.get_path[path_idx])[item_index]
                    item_tuple_list.append((item_weight, item_index, path_idx))

            items_to_remove = []
            while cargo > max_cargo:
                items_to_remove.append(item_tuple_list.pop(random_state.randint(0, len(item_tuple_list))))
                cargo -= items_to_remove[-1][0]
            for item in items_to_remove:
                solution.remove_picked_up_item_at_path_index(item[2], item[1])

    # TODO: 2nd pass - for all remaining items, attempt zero-cost insertions
    items_remaining = solution.get_remaining_items_at_path_index(-1)
    for site_idx in range(len(items_remaining)):
        if items_remaining[site_idx]:
            for obj_idx in range(0, len(items_remaining[site_idx])):
                if items_remaining[site_idx][obj_idx] != 0:
                    # Do insertion here
                    pass

    # TODO: 3rd pass - randomly select a remaining item, append shortest path to it to the solution, and attempt
    #  zero-cost insertions of the other remaining items in this subpath

    items = solution.get_remaining_items_at_path_index(-1)
    irp = solution.get_irp_instance()
    for site_idx in range(1, len(items)):
        if items[site_idx]:
            base_to_site = irp.graph.shortest_path(0, site_idx)
            site_to_base = irp.graph.shortest_path(site_idx, 0)
            subpath = base_to_site[1:] + site_to_base[1:]
            subpath_site_idx = len(base_to_site) - 2

            subpath_items_picked = []
            for idx in range(0, len(subpath)):
                subpath_items_picked.append([])

            for obj_idx in range(0, len(items[site_idx])):
                if items[site_idx][obj_idx] != 0:
                    subpath_items_picked[subpath_site_idx] = [obj_idx]
                    solution.append_subpath(subpath, subpath_items_picked)
    return solution
