my_list = ["There's a fire starting in my heart",
           "Reaching a fever pitch, it's bringing me out the dark",
           "Finally I can see you crystal clear",
           "Go ahead and sell me out and I'll lay your ship bare",
           "See how I'll leave with every piece of you"]

input_num = input('Введите 1-5 чисел в диапазоне от 0 до 4: ')
my_num = [int(x) for x in input_num.split()]

for i in range(len(my_list) + 1):
    for num in my_num:
        if i == num:
            print(num, "--", my_list[i])
