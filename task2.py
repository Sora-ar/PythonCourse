import argparse
import logging
import csv
import requests
import os
# from pprint import pprint
from datetime import datetime, timedelta
from collections import Counter
import shutil

URL = "https://randomuser.me/api/?results=50&format=csv"
CHANGE_FILE = 'new_change_data.csv'
NEW_DATA_STRUCTURE_FILE = 'new_data_structure.csv'


def get_log(log_level):
    logger = logging.getLogger("user_data")
    logger.setLevel(log_level)

    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def args_parser():
    parser = argparse.ArgumentParser(
        usage='task2.py [-h] [--destination_folder path --file_name name --filter_by selected_filter --filter_value value --log_level selected_level]')
    parser.add_argument('--destination_folder', metavar='DESTINATION_FOLDER',
                        help="Path to a folder where output file is going to be placed", required=True)
    parser.add_argument('--file_name', metavar='FILE', default='output',
                        help="Filename for the output CSV file", required=True)
    parser.add_argument('--filter_by', metavar='FILTER', choices=['gender', 'number'],
                        help='Filter data by gender or number of rows')
    parser.add_argument('--filter_value', metavar='VALUE', help='Value to filter data by')
    parser.add_argument('--log_level', metavar='LOG', nargs='?', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Log level')

    return parser.parse_args()


def get_user_data(url, destination_file):
    response = requests.get(url)
    with open(destination_file, 'w', encoding='utf-8') as f:
        f.write(response.text)


def filter_data(source_file, destination_file, filter_by, filter_value):
    filtered_rows = []

    with open(source_file, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if filter_by == 'gender' and row['gender'] == filter_value:
                filtered_rows.append(row)
            elif filter_by == 'number' and csv_reader.line_num <= int(filter_value) + 1:
                filtered_rows.append(row)

    with open(destination_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=filtered_rows[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(filtered_rows)


def convert_date(date_str, date_format):
    user_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return user_date.strftime(date_format)


def change_and_add_content_into_csv(destination_file, logger):
    with open(destination_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open(CHANGE_FILE, 'w', newline='', encoding='utf-8') as new_file:
        writer = csv.DictWriter(new_file, fieldnames=list(rows[0].keys()) + ['current_time', 'global_index'])
        writer.writeheader()
        for i, row in enumerate(rows, start=1):
            # global_index (row number in csv file)
            row['global_index'] = i

            # change the content in the field name.title using following rule:
            # Mrs  missis; Ms miss; Mr mister; Madame mademoiselle;
            # other values should remain the same.
            match row['name.title']:
                case 'Mr':
                    row['name.title'] = 'mister'
                case 'Mrs':
                    row['name.title'] = 'missis'
                case 'Ms':
                    row['name.title'] = 'miss'
                case 'Madame':
                    row['name.title'] = 'mademoiselle'

            # Convert dob.date to the format "month/day/year”
            row['dob.date'] = convert_date(row['dob.date'], '%m/%d/%Y')

            # Convert register.date to the format "month-day-year, hours:minutes:second"
            row['registered.date'] = convert_date(row['registered.date'], '%m-%d-%Y, %H:%M:%S')

            # current_time (time of a user based on their timezone)
            hours_offset = int(row['location.timezone.offset'].split(':')[0])
            minutes_offset = int(row['location.timezone.offset'].split(':')[1])
            offset = timedelta(hours=hours_offset, minutes=minutes_offset)
            current_time = datetime.now() + offset
            row['current_time'] = current_time.strftime('%Y-%m-%d %H:%M:%S')

            writer.writerow(row)

        logger.info("Data changed successfully")


def create_new_data_structure(destination_file, logger):
    data = []
    with open(destination_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    grouped_user_data = {}
    for user in data:
        user_year = user['dob.date'][:4]
        user_country = user['location.country']
        decade = f"{user_year[2:3]}0-th"

        if decade not in grouped_user_data:
            grouped_user_data[decade] = {}

        if user_country not in grouped_user_data[decade]:
            grouped_user_data[decade][user_country] = []

        grouped_user_data[decade].setdefault(user_country, []).append(user)

    # pprint(grouped_user_data)
    logger.info("Data append successfully")

    return grouped_user_data, data


def create_sub_folders(destination_folder, grouped_user_data, user_data, logger):
    for decade in grouped_user_data.keys():
        decade_folder = os.path.join(os.path.dirname(destination_folder), decade)
        os.makedirs(decade_folder, exist_ok=True)

        for country in grouped_user_data[decade].keys():
            country_folder = os.path.join(decade_folder, country)
            os.makedirs(country_folder, exist_ok=True)

            max_age = max(user['dob.age'] for user in grouped_user_data[decade][country])

            total_registered_years = sum(int(user['registered.age']) for user in grouped_user_data[decade][country])
            num_users = len(grouped_user_data[decade][country])
            avr_registered_years = total_registered_years / num_users

            all_id_names = [user['id.name'] for user in grouped_user_data[decade][country]]
            id_name_counts = Counter(all_id_names)
            popular_id = id_name_counts.most_common(1)[0][0]

            file_name = f"max_age_{max_age}_avg_registered_{avr_registered_years}_ popular_id_{popular_id}.csv"
            file_path = os.path.join(country_folder, file_name)

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=user_data[0].keys())

                writer.writeheader()
                for row in grouped_user_data[decade][country]:
                    writer.writerow(row)

    logger.info("All folders created")


def del_data_before_1960th(destination_folder, logger):
    for decade_folder in os.listdir(destination_folder):
        if decade_folder.endswith('-th'):
            decade_year = int(decade_folder.split('-')[0])
            if decade_year < 60:
                folder_path = os.path.join(destination_folder, decade_folder)
                shutil.rmtree(folder_path)
                logger.info(f"Removed folder: {folder_path}")


def main():
    args = args_parser()
    logger = get_log(args.log_level)

    logger.info("Starting data retrieval and CSV writing process")
    destination_folder = args.destination_folder
    destination_file = os.path.join(destination_folder, f"{args.file_name}.csv")
    get_user_data(URL, destination_file)

    if args.filter_by and args.filter_value:
        filter_data(destination_file, destination_file, args.filter_by, args.filter_value)
        logger.info(f"Filtered data based on {args.filter_by} = {args.filter_value}")
    logger.info("Data retrieval and CSV writing process completed")

    logger.info("Started changing the csv file")
    change_and_add_content_into_csv(destination_file, logger)
    logger.info("Changing the csv file was successful")

    logger.info("Checking if a path exists")
    if not os.path.exists(args.destination_folder):
        os.makedirs(destination_folder)
        logger.info(f"Destination folder '{destination_folder}' created")

    os.chdir(args.destination_folder)
    logger.info(f"Changed working directory to '{destination_folder}'")

    moving_file = f"{args.file_name}.csv"
    new_destination_path = os.path.join(destination_folder, moving_file)
    os.rename(moving_file, new_destination_path)
    logger.info(f"File '{moving_file}' has been moved to the destination folder '{destination_folder}'")

    logger.info("Started changing the user data structure")
    user_data_group, user_data = create_new_data_structure(destination_file, logger)
    logger.info("Changed successfully")

    logger.info("Started creating subfolders")
    create_sub_folders(destination_folder, user_data_group, user_data, logger)
    logger.info("Successful creation of subfolders")

    logger.info("Started removing folders")
    del_data_before_1960th(destination_folder, logger)
    logger.info("Removed successfully")


# Script that can be run from command line:
# python task2.py --destination_folder . --file_name filtered_data --filter_by gender --filter_value male --log_level DEBUG
# python task2.py --destination_folder C:\Users\Admin\Desktop\University\2_year\2st_semester\MultiparadigmProgrammingLanguages\homeworks\ --file_name filtered_data --filter_by gender --filter_value male --log_level DEBUG
if __name__ == "__main__":
    main()
