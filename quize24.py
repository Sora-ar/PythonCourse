input_list = input('Введите 10 целых чисел: ')
my_list = [int(x) for x in input_list.split()]

even_items = [i for i in my_list if i % 2 == 0]

print(my_list)
print(even_items)
print(1 in my_list)
