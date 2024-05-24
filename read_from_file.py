import csv


def read_from_file(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        return list(csv.DictReader(file))
