from work_with_array import create_and_print_array

N, M = 4, 6


def length_finding(arr):
    longest_length = 0
    row_longest = 0
    element_long = None

    for i, row in enumerate(arr):
        count_length = 1
        for j in range(1, len(row)):
            if row[j] == row[j - 1]:
                count_length += 1
                if count_length > longest_length:
                    longest_length = count_length
                    element_long = row[j]
                    row_longest = i + 1
            else:
                count_length = 1

    if longest_length > 1:
        print(f'{row_longest} row that contains the longest series of identical elements: {element_long}',
              f'\nLong {longest_length}')


def zero_search(arr):
    counter = sum(1 for i in range(N) for j in range(M) if arr[i][j] == 0)
    print(f'Number of rows with zero element: {counter}')


def main():
    arr = create_and_print_array(N, M)
    zero_search(arr)
    length_finding(arr)


if __name__ == "__main__":
    main()
