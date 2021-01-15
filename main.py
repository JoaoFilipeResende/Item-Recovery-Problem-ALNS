from itemrecoveryproblem.itemrecoveryproblem import ItemRecoveryProblem
from itemrecoveryproblem.solution import Solution
import numpy.random as rnd
from alns import ALNS
from alns.criteria import HillClimbing
from alnsoperators.operators import *

seed = 12345

if __name__ == '__main__':
    random_state = rnd.RandomState(seed)

    irp = ItemRecoveryProblem()
    irp.load_file("./instances/test_instance_2")

    alns = ALNS(random_state)
    alns.add_destroy_operator(remove_rand_sps)
    alns.add_destroy_operator(remove_sps_by_dispatch_rule)
    alns.add_destroy_operator(split_sps)
    alns.add_destroy_operator(swap_sps)
    alns.add_repair_operator(greedy_repair)

    initial_solution = greedy_repair(Solution(irp), random_state)
    result = alns.iterate(initial_solution, [3, 2, 1, 0.5], 0.8,
                          HillClimbing(), iterations=30, collect_stats=True)
    solution = result.best_state

    print(len(solution._path))
    print(solution.check_validity())