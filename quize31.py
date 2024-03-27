import csv

CONSTANT_DICTIONARY = [
    {'Name': 'John', 'Age': 25, 'Score': 85.5},
    {'Name': 'Alice', 'Age': 30, 'Score': 92.3},
    {'Name': 'Bob', 'Age': 22, 'Score': 78.9},
    {'Name': 'Eva', 'Age': 28, 'Score': 96.7},
    {'Name': 'Michael', 'Age': 35, 'Score': 89.2},
]

with open('file_csv.csv', 'w', newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames=list(CONSTANT_DICTIONARY[0].keys()))
    csv_writer.writeheader()
    for i in CONSTANT_DICTIONARY:
        csv_writer.writerow(i)

with open('file_csv.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for i in csv_reader:
        print(i)
