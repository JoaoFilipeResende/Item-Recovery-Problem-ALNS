from itemrecoveryproblem.itemrecoveryproblem import ItemRecoveryProblem
from itemrecoveryproblem.solution import Solution


class Alns:
    def __init__(self, item_recovery_problem):
        self.irp = item_recovery_problem

    def solve(self):
        solution = self.initial_solution()
        return solution

    def initial_solution(self):
        solution = Solution(self.irp)

        items = self.irp.get_items_at_each_site()

        for site_idx in range(1, len(items)):
            if items[site_idx]:
                base_to_site = self.irp.graph.shortest_path(0, site_idx)
                site_to_base = self.irp.graph.shortest_path(site_idx, 0)
                subpath = base_to_site[1:] + site_to_base[1:]
                subpath_site_idx = len(base_to_site) - 2

                subpath_items_picked = []
                for idx in range(0, len(subpath)):
                    subpath_items_picked.append([])

                for obj_idx in range(0, len(items[site_idx])):
                    subpath_items_picked[subpath_site_idx] = [obj_idx]
                    solution.append_subpath(subpath, subpath_items_picked)
        return solution
