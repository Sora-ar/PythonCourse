var_x = 10


def fnc_1(param1):
    """
    Take a parameter and multiply it by the global variable value

    :param param1: new parameter
    :return: multiply param1 by a global variable
    """
    return param1 * var_x


def fnc_2():
    """
    Increase value of the global variable by 5

    :return: increase var_x by 5.
    """
    global var_x
    return var_x + 5


def fnc_3(var_x, param2):
    """
    The function for multiplication of the parameters

    :param var_x: First param
    :param param2: Second param
    :return: multiplication of var_x and param2
    """
    return var_x * param2


def main():
    """
    Main: Calls other functions.
    """
    param = 4
    var_x = 3
    param2 = 8

    print(fnc_1(param))
    print(fnc_2())
    print(fnc_1(param))
    print(fnc_3(var_x, param2))


if __name__ == "__main__":
    main()
