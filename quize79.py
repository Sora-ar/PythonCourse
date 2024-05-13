def even_numbers():
    n = 0
    while True:
        yield n
        n += 2


even_gen = even_numbers()
for _ in range(10):
    print(next(even_gen))
