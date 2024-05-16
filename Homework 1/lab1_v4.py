from work_with_array import create_and_print_array
from functools import reduce

N, M = 5, 5


def sum_max_items(arr):
    max_sum = max(arr[i + j][j] + arr[j][i + j] for i in range(1, N) for j in range(M - i))
    print(f'Max sum: {max(max_sum, arr[0][-1])}')


def multiplication_positive_num(arr):
    for i, row in enumerate(arr):
        counter = reduce(lambda x, y: x * y, row, 1)
        for element in row:
            if element < 0:
                print(i + 1, ' row: there is a negative element')
                break
        else:
            print('Multiplication of positive numbers of ', i + 1, ' row: ', counter)


def main():
    arr = create_and_print_array(N, M)
    multiplication_positive_num(arr)
    sum_max_items(arr)


if __name__ == "__main__":
    main()
