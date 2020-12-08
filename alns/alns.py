from itemrecoveryproblem.itemrecoveryproblem import ItemRecoveryProblem
from itemrecoveryproblem.solution import Solution


class Alns:
    def __init__(self, item_recovery_problem):
        self.item_recovery_problem = item_recovery_problem

    def solve(self):
        solution = self.initial_solution()
        return solution

    def initial_solution(self):
        solution = Solution()
        while not solution.is_valid(self.item_recovery_problem):
            pass

        return solution
