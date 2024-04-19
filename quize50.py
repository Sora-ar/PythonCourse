def dangerous_function():
    print(3 / 0)


def calculate(a, b):
    x = a + b
    dangerous_function()
    return x * 2
