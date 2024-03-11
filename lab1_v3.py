import random

N = 4
M = 6


def length_finding():
    print('part 2')
    longest_lenght = 0
    row_len = 0
    elemen_long = 0
    row_longest = 0

    for i in range(0, N):
        count_length = 0
        for j in range(0, M - 1):
            if arr[i][j] == arr[i][j + 1]:
                count_length += 1
                elemen = arr[i][j]
            else:
                elemen = arr[i][j + 1]
                count_length = 1
            if count_length > longest_lenght:
                longest_lenght = count_length
                elemen_long = elemen
                row_longest = i + 1
        row_len += 1

    if longest_lenght > 1:
        print(row_longest, ' row that contains the longest series of identical elements: ', elemen_long)
        print('long ', longest_lenght)


def zero_search():
    print('part 1')
    counter = 0

    for i in range(0, N):
        for j in range(0, M):
            if arr[i][j] == 0:
                counter += 1
                break

    print('Number of rows with zero element: ', counter)
    print('')


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
zero_search()
length_finding()
