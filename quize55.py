class UndefinedClass:
    def __init__(self):
        raise Exception()


def dangerous_function(var):
    return UndefinedClass()


def calculate():
    some_number = dangerous_function().mtd_1().mtd_2()
    return some_number * 4 + 12
