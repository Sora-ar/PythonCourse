import csv


def read_from_file(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)
