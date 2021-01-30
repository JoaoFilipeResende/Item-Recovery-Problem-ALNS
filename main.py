from itemrecoveryproblem.itemrecoveryproblem import ItemRecoveryProblem
from itemrecoveryproblem.solution import Solution
import numpy.random as rnd
from alns import ALNS
from alns.criteria import HillClimbing, SimulatedAnnealing
from alnsoperators.operators import *
import matplotlib.pyplot as plt
import time
import sys

seed = 12345
iterations = 200
instance_to_run = 9  # Only used when not run with command line arguments

if __name__ == '__main__':
    random_state = rnd.RandomState(seed)

    irp = ItemRecoveryProblem()
    try:
        instance_path = "./instances/" + str(sys.argv[1])
    except IndexError:
        instance_path = "./instances/" + str(instance_to_run)
        print("Executing hard-coded instance:", instance_to_run)

    irp.load_file(instance_path)

    alns = ALNS(random_state)
    alns.add_destroy_operator(remove_rand_pos)
    alns.add_destroy_operator(swap_rand_pos)
    alns.add_destroy_operator(remove_rand_sps)
    alns.add_destroy_operator(remove_worst_sps)
    alns.add_repair_operator(greedy_repair)

    initial_solution = greedy_repair(Solution(irp), random_state)
    print(instance_path)
    print("Initial solution:", int(initial_solution.get_cost()))
    #criterion = HillClimbing()
    criterion = SimulatedAnnealing(100, 5, 5, method='linear')
    start_time = time.time()
    result = alns.iterate(initial_solution, [3, 2, 1, 0.5], 0.8,
                          criterion, iterations=iterations, collect_stats=True)
    end_time = time.time()
    solution = result.best_state
    print("Best solution:", int(solution.objective()))
    print("Time taken (s):", int(end_time - start_time))
    print("Iterations:", iterations)
    #_, ax = plt.subplots(figsize=(12, 6))
    #result.plot_objectives(ax=ax, lw=2)
    #figure = plt.figure("operator_counts", figsize=(14, 6))
    #figure.subplots_adjust(bottom=0.15, hspace=.5)
    #result.plot_operator_counts(figure=figure, title="Operator diagnostics", legend=["Best", "Better", "Accepted"])

    print("Is best solution valid?", solution.check_validity()[0])
