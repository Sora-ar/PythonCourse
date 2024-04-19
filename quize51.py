def dangerous_function(var):
    return 3 / var


def calculate(a, b=0):
    x = a + b
    return x * dangerous_function(x)
