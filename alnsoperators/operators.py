import numpy as np
from copy import deepcopy


# Randomly remove between 10% and 60% of all positions along the path
def remove_rand_pos(solution, random_state):
    solution = solution.copy()
    positions_to_remove = int(random_state.uniform(0.1, 0.6) * len(solution.get_path()))

    if positions_to_remove < 1:
        positions_to_remove = 1

    while positions_to_remove != 0 and len(solution.get_path()) > 1:
        idx_to_remove = random_state.randint(1, len(solution.get_path()) - 1)
        solution.remove_path_index(idx_to_remove)
        positions_to_remove -= 1

    return solution


# Randomly swap 20% of all positions along the path
def swap_rand_pos(solution, random_state):
    solution = solution.copy()
    num_pos_to_swap = int(0.20 * (len(solution.get_path())))

    if num_pos_to_swap < 1:
        num_pos_to_swap = 1

    for _ in range(num_pos_to_swap):
        pos_1_idx = random_state.randint(1, len(solution.get_path()) - 1)
        pos_2_idx = random_state.randint(1, len(solution.get_path()) - 1)

        # Ensure that the pos 2 is higher than 1
        if pos_2_idx < pos_1_idx:
            pos_1_idx, pos_2_idx = pos_2_idx, pos_1_idx

        pos_1_items = solution.get_items_picked_up_at_path_index(pos_1_idx)
        pos_2_items = solution.get_items_picked_up_at_path_index(pos_2_idx)

        pos_1_site = solution.get_path()[pos_1_idx]
        pos_2_site = solution.get_path()[pos_2_idx]

        solution.remove_path_index(pos_1_idx)
        solution.remove_path_index(pos_2_idx)
        solution.insert_subpath(pos_1_idx, [pos_2_site], [pos_2_items])
        solution.insert_subpath(pos_2_idx, [pos_1_site], [pos_1_items])

    return solution


# Randomly removes between 10% and 60% of all subpaths in the solution
def remove_rand_sps(solution, random_state):
    solution = solution.copy()
    subpath_indexes = np.where(np.array(solution.get_path()) == 0)[0]
    num_subpaths_to_remove = int(random_state.uniform(0.1, 0.6) * (len(subpath_indexes) - 1))

    if (num_subpaths_to_remove < 1) and (len(solution.get_path()) > 1):
        num_subpaths_to_remove = 1

    for _ in range(num_subpaths_to_remove):
        rand_idx = random_state.randint(0, len(subpath_indexes) - 1)
        subpath_size = subpath_indexes[rand_idx + 1] - subpath_indexes[rand_idx]
        solution.remove_path_index_multiple(subpath_indexes[rand_idx], subpath_size)
        subpath_indexes = np.where(np.array(solution.get_path()) == 0)[0]

    return solution


# Remove between 10% and 60% of all subpaths ordered by (total item weight retrieved in subpath) / (cost of subpath)
def remove_worst_sps(solution, random_state):
    solution = solution.copy()
    subpath_indexes = np.where(np.array(solution.get_path()) == 0)[0]
    num_subpaths_to_remove = int(random_state.uniform(0.1, 0.6) * (len(subpath_indexes) - 1))

    if (num_subpaths_to_remove < 1) and (len(solution.get_path()) > 1):
        num_subpaths_to_remove = 1

    for _ in range(num_subpaths_to_remove):
        subpath_idx_worst = 0
        subpath_worst = float('inf')

        for idx in range(len(subpath_indexes) - 1):
            subpath_value = solution.get_accumulated_cost_at_path_index(subpath_indexes[idx + 1]) - \
                            solution.get_accumulated_cost_at_path_index(subpath_indexes[idx])
            subpath_value = sum(solution.get_robot_cargo_at_path_index(subpath_indexes[idx + 1] - 1)) / subpath_value

            if subpath_value < subpath_worst:
                subpath_idx_worst = idx
                subpath_worst = subpath_value

        subpath_size = subpath_indexes[subpath_idx_worst + 1] - subpath_indexes[subpath_idx_worst]
        solution.remove_path_index_multiple(subpath_indexes[subpath_idx_worst], subpath_size)
        subpath_indexes = np.where(np.array(solution.get_path()) == 0)[0]

    return solution


# Splits between 10% and 60% of all subpaths
def split_sps(solution, random_state):
    solution = solution.copy()
    subpath_indexes = np.where(np.array(solution.get_path()) == 0)[0]
    num_subpaths_to_split = int(random_state.uniform(0.1, 0.6) * (len(subpath_indexes) - 1))

    for _ in range(num_subpaths_to_split):
        rand_idx = random_state.randint(0, len(subpath_indexes) - 1)
        subpath_size = subpath_indexes[rand_idx + 1] - subpath_indexes[rand_idx]

        if subpath_size <= 3:
            continue

        # The +2 here is important to ensure that a split doesn't generate two consecutive zeros
        idx_to_split = random_state.randint(subpath_indexes[rand_idx] + 2, subpath_indexes[rand_idx + 1])
        solution.insert_subpath(idx_to_split, [0], [[]])
        subpath_indexes = np.where(np.array(solution.get_path()) == 0)[0]

    return solution


def greedy_repair(solution, random_state):
    is_valid, problem_index = solution.check_validity()

    if is_valid:
        #print("Warning: A valid solution was passed to the greedy_repair() method")
        return solution
    irp = solution.get_irp_instance()

    # 1st step: fix beginning and end of the solution
    # Fix beginning of the solution
    if solution.get_path()[0] != 0:
        solution.insert_subpath(0, [0], [[0]])

    # Truncate solution if it does not end at the base
    while solution.get_path()[-1] != 0:
        solution.remove_path_index(-1)

    # 2nd step: repair path by joining "broken" transitions with the shortest path between them, and join
    # repeated transitions
    if len(solution.get_path()) > 1:
        idx = 0
        while True:
            path = solution.get_path()
            if irp.get_cost_between_adjacent_sites(path[idx], path[idx + 1]) is None:
                repair_subpath = irp.graph.shortest_path(path[idx], path[idx + 1])
                repair_subpath.pop(0)
                repair_subpath.pop()
                repair_subpath_items_picked = []
                for _ in repair_subpath:
                    repair_subpath_items_picked.append([])
                solution.insert_subpath(idx + 1, repair_subpath, repair_subpath_items_picked)
                idx += 2
            elif path[idx] == path[idx + 1]:
                for item_idx in solution.get_items_picked_up_at_path_index(idx + 1):
                    solution.add_picked_up_item_at_path_index(idx, item_idx)
                solution.remove_path_index(idx + 1)
            else:
                idx += 1
            if idx == len(solution.get_path()) - 1:
                break

    # 3rd step, randomly remove items in subpaths until the carry weight is no longer exceeded in those subpaths
    subpath_indexes = np.where(np.array(solution.get_path()) == 0)[0]
    subpaths_to_check = []
    is_valid, problem_index = solution.check_validity()
    if is_valid:
        return solution
    for i in range(len(subpath_indexes)):
        if subpath_indexes[i] >= problem_index:
            subpaths_to_check.append(subpath_indexes[i])
        elif subpath_indexes[i] <= problem_index < subpath_indexes[i + 1]:
            subpaths_to_check.append(subpath_indexes[i])

    max_cargo = irp.get_robot_cargo_size()
    # If the problem is at the end of the solution (i.e. not all items were picked), then this is ignored
    for i in range(len(subpaths_to_check) - 1):
        items_carried_at_subpath_end = solution.get_robot_cargo_at_path_index(subpaths_to_check[i + 1] - 1)
        cargo = sum(items_carried_at_subpath_end)
        if cargo > max_cargo:
            item_tuple_list = []  # List containing tuples of (item weight, item idx, path index where item is picked)
            for path_idx in range(subpaths_to_check[i], subpaths_to_check[i + 1]):
                items_picked_up_at_path_idx = solution.get_items_picked_up_at_path_index(path_idx)
                for j in range(len(items_picked_up_at_path_idx)):
                    item_index = items_picked_up_at_path_idx[j]
                    item_weight = irp.get_items_at_site(solution.get_path()[path_idx])[item_index]
                    item_tuple_list.append((item_weight, item_index, path_idx))

            items_to_remove = []
            while cargo > max_cargo:
                items_to_remove.append(item_tuple_list.pop(random_state.randint(0, len(item_tuple_list))))
                cargo -= items_to_remove[-1][0]
            for item in items_to_remove:
                solution.remove_picked_up_item_at_path_index(item[2], item[1])

    # 4th pass: for all remaining items, attempt zero-cost insertions
    items_remaining = solution.get_remaining_items_at_path_index(-1)
    for site in range(1, len(items_remaining)):
        if items_remaining[site]:
            for obj_idx in range(0, len(items_remaining[site])):
                if items_remaining[site][obj_idx] != 0:
                    path_idx_insertion_candidates = []
                    for path_idx in range(len(solution.get_path())):
                        if solution.get_path()[path_idx] == site:
                            path_idx_insertion_candidates.append(path_idx)

                    # Try all candidates
                    while path_idx_insertion_candidates:
                        candidate_idx = path_idx_insertion_candidates.pop(random_state.randint(0,
                                                                                               len(
                                                                                                   path_idx_insertion_candidates)))
                        candidate_subpath_end_path_idx = 0
                        for i in range(0, len(subpath_indexes)):
                            if subpath_indexes[i] >= candidate_idx:
                                candidate_subpath_end_path_idx = subpath_indexes[i]
                                break
                        # If cargo at end of subpath + this item does not exceed the max cargo, insert it
                        if sum(solution.get_robot_cargo_at_path_index(candidate_subpath_end_path_idx - 1)) \
                                + items_remaining[site][obj_idx] <= max_cargo:
                            solution.add_picked_up_item_at_path_index(candidate_idx, obj_idx)
                            break

    # 5th pass - randomly select a remaining item, append shortest path to it to the solution
    # TODO: maybe attempt zero-cost insertions of the other remaining items in each newly appended subpath?
    items = solution.get_remaining_items_at_path_index(-1)

    item_tuple_list = []
    for site in range(1, len(items)):
        for obj_idx in range(0, len(items[site])):
            item_tuple_list.append((site, obj_idx))

    while item_tuple_list:
        item = (item_tuple_list.pop(random_state.randint(0, len(item_tuple_list))))
        base_to_site = irp.graph.shortest_path(0, item[0])
        site_to_base = irp.graph.shortest_path(item[0], 0)
        subpath = base_to_site[1:] + site_to_base[1:]
        subpath_items_picked = []
        for idx in range(0, len(subpath)):
            subpath_items_picked.append([])
        subpath_items_picked[len(base_to_site) - 2] = [item[1]]
        solution.append_subpath(subpath, subpath_items_picked)

    # 6th pass: remove empty subpaths
    i = 0
    j = 0
    while i < len(solution.get_path()) - 1:
        items_were_picked = False
        j = i + 1
        while solution.get_path()[j] != 0:
            if solution.get_items_picked_up_at_path_index(j):
                items_were_picked = True
            j += 1
        if items_were_picked:
            i = deepcopy(j)  # Skip to the next subpath
        else:
            positions_to_delete = j - i
            solution.remove_path_index_multiple(i, positions_to_delete)

    if not (solution.check_validity()[0]) or (solution.get_cost() == float("inf")):
        raise Exception("Greedy repair failed")

    return solution
