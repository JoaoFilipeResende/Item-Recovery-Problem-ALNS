from itemrecoveryproblem.itemrecoveryproblem import ItemRecoveryProblem
from itemrecoveryproblem.solution import Solution
import numpy.random as rnd
from alns import ALNS
from alns.criteria import HillClimbing, SimulatedAnnealing
from alnsoperators.operators import *
import matplotlib.pyplot as plt

seed = 12345

if __name__ == '__main__':
    random_state = rnd.RandomState(seed)

    irp = ItemRecoveryProblem()
    irp.load_file("./instances/test_instance")

    alns = ALNS(random_state)
    alns.add_destroy_operator(remove_rand_pos)
    alns.add_destroy_operator(swap_rand_pos)
    alns.add_destroy_operator(remove_rand_sps)
    alns.add_destroy_operator(remove_worst_sps)
    alns.add_destroy_operator(split_sps)
    alns.add_repair_operator(greedy_repair)

    initial_solution = greedy_repair(Solution(irp), random_state)
    print("Initial solution:", initial_solution.get_cost())
    #criterion = HillClimbing()
    criterion = SimulatedAnnealing(100, 10, 5, method='linear')
    result = alns.iterate(initial_solution, [3, 2, 1, 0.5], 0.8,
                          criterion, iterations=100, collect_stats=True)
    solution = result.best_state
    print("Best solution:", solution.objective())
    print("Is it valid?", solution.check_validity())

    _, ax = plt.subplots(figsize=(12, 6))
    result.plot_objectives(ax=ax, lw=2)
    figure = plt.figure("operator_counts", figsize=(14, 6))
    figure.subplots_adjust(bottom=0.15, hspace=.5)
    result.plot_operator_counts(figure=figure, title="Operator diagnostics", legend=["Best", "Better", "Accepted"])