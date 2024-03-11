import random

N, M = (5, 5)


def sum_min_items():
    print('')
    print('part 2')
    min_sum = arr[0][-1]
    print('Start min sum = ', min_sum)
    print('')

    for i in range(1, N):
        l_side = 0
        r_side = 0
        for j in range(M - i):
            l_side += arr[i + j][j]
            r_side += arr[j][i + j]
        if l_side < min_sum:
            min_sum = l_side
        if r_side < min_sum:
            min_sum = r_side
        print(f'Left side {l_side}')
        print(f'Right side {r_side}')

    print('')
    print('Min sum: ', min_sum)


def sum_non_negativ_rows():
    print('part 1')

    for i in range(N):
        counter = 0
        stop = True
        for j in range(M):
            counter += arr[i][j]
            if arr[i][j] < 0:
                stop = False
                break
        if stop:
            print('Row ', i + 1, ': sum = ', counter)
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
sum_non_negativ_rows()
sum_min_items()
