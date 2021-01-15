
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

    # TODO: 1st pass - randomly remove items in problematic subpaths until carry weight is OK

    # TODO: 2nd pass - for all remaining items, attempt zero-cost insertions

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
