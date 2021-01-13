from itemrecoveryproblem.itemrecoveryproblem import ItemRecoveryProblem
from alns.alns import Alns

if __name__ == '__main__':
    irp = ItemRecoveryProblem()
    irp.load_file("./instances/test_instance_2")
    alns = Alns(irp)
    solution = alns.solve()
    print(solution._path)
    print(solution.check_validity())