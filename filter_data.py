from constants import GENDER
from read_from_file import read_from_file


def filter_by_gender(source_file, filter_value):
    csv_reader = read_from_file(source_file)
    filtered_rows = [row for row in csv_reader if row[GENDER] == filter_value]

    return filtered_rows


def filter_by_number(source_file, filter_value):
    csv_reader = read_from_file(source_file)
    filtered_rows = [row for idx, row in enumerate(csv_reader) if idx < int(filter_value)]

    return filtered_rows


def filter_data(source_file, filter_by, filter_value):
    if filter_by == 'filter_by_gender':
        filter_gen = filter_by_gender(source_file, filter_value)
        return filter_gen
    else:
        filter_num = filter_by_number(source_file, filter_value)
        return filter_num
