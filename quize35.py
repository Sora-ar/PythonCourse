import random


def function_1():
    return random.sample(range(1, 101), 5)


num = function_1()
print(*num)

result = num[1] * num[3]
print(result)
