import random


def fnc():
    first_num = random.randint(10, 24)
    second_num = round(random.uniform(-7, -4), 2)

    return first_num, second_num


def main():
    result = fnc()
    print(result)
    chosen_num = random.choice(result)
    print(chosen_num)


if __name__ == "__main__":
    main()
