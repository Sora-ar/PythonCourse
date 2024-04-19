class UndefinedClass:
    def __init__(self):
        raise Exception()


def dangerous_function(var):
    return UndefinedClass()


def calculate(some_collection):
    some_object = dangerous_function(some_collection)
    some_object.mtd_1()
    some_object.mtd_2()
