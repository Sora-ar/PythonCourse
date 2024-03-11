import random

N, M = (5, 5)


def sum_max_items():
    print('')
    print('part 2')
    max_sum = arr[0][-1]
    print('Start max sum = ', max_sum)
    print('')

    for i in range(1, N):
        l_side = 0
        r_side = 0
        for j in range(M - i):
            l_side += arr[i + j][j]
            r_side += arr[j][i + j]
        if l_side > max_sum:
            max_sum = l_side
        if r_side > max_sum:
            max_sum = r_side
        print('Left side ', l_side)
        print('Right side ', r_side)

    print('')
    print('Max sum: ', max_sum)


def multiplication_positive_num():
    print('part 1')

    for i in range(N):
        counter = 1
        stop = True
        for j in range(M):
            counter *= arr[i][j]
            if arr[i][j] < 0:
                stop = False
                break
        if stop:
            print('Multiplication of positive number of ', i + 1, ' row: ', counter)
        else:
            print(i + 1, ' row: there is a negative element')


def print_array(lst):
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            print(f"{lst[i][j]} ", end=' ')
        print()

    print('')


def create_array():
    return [
        [random.randint(0, 9) for _ in range(M)] for _ in range(N)
    ]


arr = create_array()
print_array(arr)
multiplication_positive_num()
sum_max_items()
