from itemrecoveryproblem.itemrecoveryproblem import ItemRecoveryProblem
from itemrecoveryproblem.solution import Solution


class Alns:
    def __init__(self, item_recovery_problem):
        self.item_recovery_problem = item_recovery_problem

    def solve(self):
        solution = self.initial_solution()
        return solution

    def initial_solution(self):
        solution = Solution(self.item_recovery_problem)

        sol_is_valid, index_of_error = solution.check_validity()

        while not sol_is_valid:
            pass

        return solution
