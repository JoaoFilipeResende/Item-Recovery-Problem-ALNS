from itemrecoveryproblem.itemrecoveryproblem import ItemRecoveryProblem

if __name__ == '__main__':
    irp = ItemRecoveryProblem()
    irp.load_file("./instances/test_instance_2")
    irp.debug()
