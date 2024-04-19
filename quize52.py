def dangerous_function(var):
    x_1 = 4 / var
    return x_1 % 2


def calculate(some_collection):
    x = 0
    for i in some_collection:
        if dangerous_function(i):
            x += 9
        else:
            x -= 6
    return x
