def factorial(n):
    """
    Calculate the factorial of a number using recursion.

    :param n: An integer.
    :return: The factorial of n.
    """
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


number = 5
result = factorial(number)
print(f"The factorial of {number} is:", result)
