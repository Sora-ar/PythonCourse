import random


def create_and_print_array(N, M):
    arr = [[random.randint(0, 9) for _ in range(M)] for _ in range(N)]
    print_array(arr)
    return arr


def print_array(lst):
    print('\n'.join([' '.join(map(str, row)) for row in lst]))
