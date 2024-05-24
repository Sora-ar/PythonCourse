from constants import GENDER
from read_from_file import read_from_file


def filter_by_gender(source_file, filter_value):
    return [row for row in read_from_file(source_file) if row[GENDER] == filter_value]


def filter_by_number(source_file, filter_value):
    return [row for idx, row in enumerate(read_from_file(source_file)) if idx < int(filter_value)]


def filter_data(source_file, filter_value):
    return filter_by_gender(source_file, filter_value) if filter_value == 'male' or filter_value == 'female' \
        else filter_by_number(source_file, filter_value)
