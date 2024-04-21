import random

N, M = 5, 5


def create_and_print_array():
    arr = [[random.randint(0, 9) for _ in range(M)] for _ in range(N)]
    print_array(arr)
    return arr


def sum_min_items(arr):
    min_sum = min(arr[i + j][j] + arr[j][i + j] for i in range(1, N) for j in range(M - i))
    print(f'Min sum: {min(min_sum, arr[0][-1])}')


def sum_non_negativ_rows(arr):
    for i, row in enumerate(arr):
        row_sum = sum(row)
        print(f'Row {i + 1}: sum =',
              row_sum if all(element >= 0 for element in row) else '{} row: there is a negative element'.format(i + 1))


def print_array(lst):
    [print(' '.join(map(str, row))) for row in lst]


def main():
    arr = create_and_print_array()
    sum_non_negativ_rows(arr)
    sum_min_items(arr)


if __name__ == "__main__":
    main()
