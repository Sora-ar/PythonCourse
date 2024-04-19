import random

N, M = (5, 5)


def sum_max_items():
    max_sum = max(arr[i + j][j] + arr[j][i + j] for i in range(1, N) for j in range(M - i))
    print('Max sum:', max(max_sum, arr[0][-1]))


def multiplication_positive_num():
    for i, row in enumerate(arr):
        counter = 1
        for element in row:
            if element < 0:
                print(i + 1, ' row: there is a negative element')
                break
            counter *= element
        else:
            print('Multiplication of positive numbers of ', i + 1, ' row: ', counter)


def print_array(lst):
    [print(' '.join(map(str, row))) for row in lst]


def create_array():
    return [[random.randint(0, 9) for _ in range(M)] for _ in range(N)]


arr = create_array()
print_array(arr)
multiplication_positive_num()
sum_max_items()
