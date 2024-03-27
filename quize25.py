import random

my_list = []

for _ in range(1, 11):
    my_list.append(random.randint(1, 50))

for i in my_list:
    if i % 2 == 0:
        print(i)
    if i == 4:
        break
else:
    print("'I'm in the clause")
