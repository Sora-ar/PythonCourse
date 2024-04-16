some_string = "  Python  "

modified_string = some_string.lower().strip().center(11, '-').split()
print(modified_string)
