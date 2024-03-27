my_list = [5, 17, 22, 23, 1, 6, 89, 49, 99, 15]
filtered = list(filter(lambda x: x % 3 == 0, my_list))
print(filtered)
