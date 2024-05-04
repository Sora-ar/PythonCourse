class MathException(Exception):
    pass


def calculator(param_1, param_2, action):
    """
    Perform a mathematical operation based on the given action.

    :param param_1: The first parameter.
    :param param_2: The second parameter.
    :param action: The action to perform. Valid values are 'multiplication', 'division', 'increment', 'decrement'.
    :return: The result of the mathematical operation.
    """

    try:
        match action:
            case 'multiplication':
                return param_1 * param_2
            case 'division':
                if param_2 == 0 or param_1 == 0:
                    raise MathException("Division by zero")
                return param_1 / param_2
            case 'increment':
                return param_1 + param_2
            case 'decrement':
                return param_1 - param_2
            case _:
                raise MathException(f"Unknown action: {action}")
    except MathException as e:
        print(f"MathException: {e}")
        return None


x = input("Enter action: ")
result = calculator(1, 2, x)
print("Result:", result)
