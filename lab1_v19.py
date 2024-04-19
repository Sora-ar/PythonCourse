import random

N, M = (5, 5)


def sum_min_items():
    min_sum = min(arr[i + j][j] + arr[j][i + j] for i in range(1, N) for j in range(M - i))
    print('Min sum:', min(min_sum, arr[0][-1]))


def sum_non_negativ_rows():
    for i, row in enumerate(arr):
        row_sum = sum(row)
        if all(element >= 0 for element in row):
            print('Row', i + 1, ': sum =', row_sum)
        else:
            print(i + 1, 'row: there is a negative element')


def print_array(lst):
    [print(' '.join(map(str, row))) for row in lst]


def create_array():
    return [[random.randint(0, 9) for _ in range(M)] for _ in range(N)]


arr = create_array()
print_array(arr)
sum_non_negativ_rows()
sum_min_items()
