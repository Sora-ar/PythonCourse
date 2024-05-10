import argparse
import logging
import csv
import requests
import os
from datetime import datetime, timedelta
from collections import Counter
import shutil
from constants import *


def get_log(log_level):
    logger = logging.getLogger('user_data')

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(log_level)
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def args_parser():
    parser = argparse.ArgumentParser(
        usage='task2.py [-h] [--destination_folder path --file_name name '
              '(--filter_by_gender selected_filter / --filter_by_number num) '
              '--filter_value value --log_level selected_level]')
    parser.add_argument('--destination_folder', metavar='DESTINATION_FOLDER',
                        help='Path to a folder where output file is going to be placed', required=True)

    parser.add_argument('--file_name', metavar='FILE', default='output',
                        help='Filename for the output CSV file', required=True)

    exclusive_group = parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument('--filter_by_gender', metavar='GENDER', help='Filter data by gender')
    exclusive_group.add_argument('--filter_by_number', metavar='NUMBER', help='Filter data by number of rows')

    parser.add_argument('--filter_value', metavar='VALUE', help='Value to filter data by')
    parser.add_argument('--log_level', metavar='LOG', nargs='?', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Log level')

    return parser.parse_args()


def get_user_data(url, destination_file):
    response = requests.get(url)
    with open(destination_file, 'w', encoding='utf-8') as f:
        f.write(response.text)


def write_to_file(data, destination_file):
    with open(destination_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(data)


def read_from_file(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)


def filter_by_gender(source_file, destination_file, filter_value):
    csv_reader = read_from_file(source_file)
    filtered_rows = [row for row in csv_reader if row[GENDER] == filter_value]

    write_to_file(filtered_rows, destination_file)


def filter_by_number(source_file, destination_file, filter_value):
    csv_reader = read_from_file(source_file)
    filtered_rows = [row for idx, row in enumerate(csv_reader) if idx < int(filter_value)]

    write_to_file(filtered_rows, destination_file)


def filter_data(source_file, destination_file, filter_by, filter_value):
    if filter_by == 'filter_by_gender':
        filter_by_gender(source_file, destination_file, filter_value)
    else:
        filter_by_number(source_file, destination_file, filter_value)


def get_current_time(row):
    hours_offset, minutes_offset = map(int, row[TIMEZONE_OFFSET].split(':'))
    offset = timedelta(hours=hours_offset, minutes=minutes_offset)
    current_time = datetime.now() + offset
    row[CURRENT_TIME] = current_time.strftime('{data} {time}'.format(data=CURRENT_TIME_DATA_FORMAT,
                                                                     time=TIME_FORMAT))

    return row[CURRENT_TIME]


def convert_date(date_str, date_format):
    user_date = datetime.strptime(date_str, '{data}T{time}.%fZ'.format(data=CURRENT_TIME_DATA_FORMAT,
                                                                       time=TIME_FORMAT))

    return user_date.strftime(date_format)


def replacement_prefix(title):
    match title:
        case 'Mr':
            return 'mister'
        case 'Mrs':
            return 'missis'
        case 'Ms':
            return 'miss'
        case 'Madame':
            return 'mademoiselle'

    return title


def change_content_into_csv(destination_file, logger):
    rows = read_from_file(destination_file)

    with open(CHANGE_FILE, 'w', newline='', encoding='utf-8') as new_file:
        writer = csv.DictWriter(new_file, fieldnames=list(rows[0].keys()) + [CURRENT_TIME, GLOBAL_INDEX])
        writer.writeheader()
        for i, row in enumerate(rows, start=1):
            row[GLOBAL_INDEX] = i
            row[TITLE] = replacement_prefix(row[TITLE])
            row[DOB_DATE] = convert_date(row[DOB_DATE], DATA_FORMAT)
            row[REGISTERED_DATE] = convert_date(row[REGISTERED_DATE],
                                                '{data}, {time}'.format(data=DATA_FORMAT, time=TIME_FORMAT))
            row[CURRENT_TIME] = get_current_time(row)

            writer.writerow(row)

        logger.info('Data changed successfully')


def create_new_data_structure(destination_file, logger):
    data = [row for row in read_from_file(destination_file)]
    grouped_user_data = {}

    for user in data:
        user_year = user[DOB_DATE][:4]
        user_country = user[COUNTRY]
        decade = f'{user_year[2:3]}0-th'

        grouped_user_data.setdefault(decade, {})

        grouped_user_data[decade].setdefault(user_country, [])

        grouped_user_data[decade][user_country].append(user)

    logger.info('Data append successfully')

    return grouped_user_data, data


def generate_filename(grouped_user_data, decade, country):
    max_age = max(user[DOB_AGE] for user in grouped_user_data[decade][country])

    total_registered_years = sum(int(user[AGE]) for user in grouped_user_data[decade][country])
    num_users = len(grouped_user_data[decade][country])
    avr_registered_years = total_registered_years / num_users

    all_id_names = [user[NAME] for user in grouped_user_data[decade][country]]
    id_name_counts = Counter(all_id_names)
    popular_id = id_name_counts.most_common(1)[0][0]

    file_name = f'max_age_{max_age}_avg_registered_{avr_registered_years}_ popular_id_{popular_id}.csv'

    return file_name


def create_dirs(path, purpose):
    folder = os.path.join(path, purpose)
    os.makedirs(folder, exist_ok=True)

    return folder


def file_entry_for_folders(file_path, user_data, grouped_user_data, decade, country):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=user_data[0].keys())

        writer.writeheader()
        for row in grouped_user_data[decade][country]:
            writer.writerow(row)


def create_sub_folders(destination_folder, grouped_user_data, user_data, logger):
    for decade in grouped_user_data.keys():
        decade_folder = create_dirs(destination_folder, decade)

        for country in grouped_user_data[decade].keys():
            country_folder = create_dirs(decade_folder, country)

            file_name = generate_filename(grouped_user_data, decade, country)
            file_path = os.path.join(country_folder, file_name)

            file_entry_for_folders(file_path, user_data, grouped_user_data, decade, country)

    logger.info('All folders created')


def del_data_before_1960th(destination_folder, logger):
    for decade_folder in os.listdir(destination_folder):
        if decade_folder.endswith('-th'):
            decade_year = int(decade_folder.split('-')[0])
            if decade_year < 60:
                folder_path = os.path.join(destination_folder, decade_folder)
                shutil.rmtree(folder_path)
                logger.info(f'Removed folder: {folder_path}')


def get_full_folder_structure(destination_folder, level=0):
    items = os.listdir(destination_folder)

    items.sort()

    for item in items:
        item_path = os.path.join(destination_folder, item)
        is_folder = os.path.isdir(item_path)
        type_flag = 'DIR' if is_folder else 'FILE'
        print('\t' * level + f'{item}: {type_flag}')

        if is_folder:
            get_full_folder_structure(item_path, level + 1)


def archive_destination_folder(destination_folder):
    shutil.make_archive(destination_folder, 'zip', destination_folder)


def main():
    args = args_parser()
    logger = get_log(args.log_level)

    logger.info('Starting data retrieval and CSV writing process')
    destination_folder = args.destination_folder
    destination_file = os.path.join(destination_folder, f'{args.file_name}.csv')
    get_user_data(URL, destination_file)

    if args.filter_by and args.filter_value:
        filter_data(destination_file, destination_file, args.filter_by_gender or args.filter_by_number, args.filter_value)

        logger.info(f'Filtered data based on {args.filter_by_gender or args.filter_by_number} = {args.filter_value}')
    logger.info('Data retrieval and CSV writing process completed')

    logger.info('Started changing the csv file')
    change_content_into_csv(destination_file, logger)
    logger.info('Changing the csv file was successful')

    logger.info('Checking if a path exists')
    if not os.path.exists(args.destination_folder):
        os.makedirs(destination_folder)
        logger.info(f'Destination folder "{destination_folder}" created')

    os.chdir(args.destination_folder)
    logger.info(f'Changed working directory to "{destination_folder}"')

    moving_file = f'{args.file_name}.csv'
    new_destination_path = os.path.join(destination_folder, moving_file)
    os.rename(moving_file, new_destination_path)
    logger.info(f'File "{moving_file}" has been moved to the destination folder "{destination_folder}"')

    logger.info('Started changing the user data structure')
    user_data_group, user_data = create_new_data_structure(destination_file, logger)
    logger.info('Changed successfully')

    logger.info('Started creating subfolders')
    create_sub_folders(destination_folder, user_data_group, user_data, logger)
    logger.info('Successful creation of subfolders')

    logger.info('Started removing folders')
    del_data_before_1960th(destination_folder, logger)
    logger.info('Removed successfully')

    get_full_folder_structure(destination_folder)
    logger.info('Structure formed successfully')

    archive_destination_folder(destination_folder)
    logger.info('Folder is archived')


# Script that can be run from command line:
# python task2.py --destination_folder . --file_name filtered_data --filter_by gender --filter_value male --log_level DEBUG
# python task2.py --destination_folder C:\Users\Admin\Desktop\University\2_year\2st_semester\MultiparadigmProgrammingLanguages\homeworks\ --file_name filtered_data --filter_by gender --filter_value male --log_level DEBUG
if __name__ == '__main__':
    main()
