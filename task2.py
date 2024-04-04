import argparse
import logging
import csv
import requests
import os.path
from datetime import datetime
import pytz  # work with timezone

URL = "https://randomuser.me/api/?results=5000"
CHANGE_FILE = 'new_change_data.csv'


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
    if response.status_code == 200:
        result = response.json()['results']
        with open(destination_file, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.DictWriter(file, fieldnames=result[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(result)
    else:
        return None


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


def replacement_content(value):
    replacements = {
        'Mrs': 'missis',
        'Ms': 'miss',
        'Mr': 'mister',
        'Madame': 'mademoiselle'
    }
    return replacements.get(value, value)


def convert_date(date_str, date_format):
    user_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return user_date.strftime(date_format)


def change_and_add_content_into_csv(destination_file):
    with open(destination_file, 'r', newline='', encoding='utf-8') as file, \
            open(CHANGE_FILE, 'w', newline='', encoding='utf-8') as new_file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['global_index', 'current_time']

        writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            user_timezone = row.get('location.timezone')
            if user_timezone:
                return pytz.timezone(user_timezone)

        for i, row in enumerate(reader, start=1):
            # global_index (row number in csv file)
            row['global_index'] = i

            # current_time (time of a user based on their timezone)
            row['current_time'] = datetime.now(user_timezone).strftime('%Y-%m-%d %H:%M:%S')

            # change the content in the field name.title using following rule:
            # Mrs  missis; Ms miss; Mr mister; Madame mademoiselle;
            # other values should remain the same.
            row['name.title'] = replacement_content(row['name.title'])

            # Convert dob.date to the format "month/day/year”
            row['dob.date'] = convert_date(row['dob.date'], '%m/%d/%Y')

            # Convert register.date to the format "month-day-year, hours:minutes:second"
            row['registered.date'] = convert_date(row['registered.date'], '%m-%d-%Y, %H:%M:%S')

            writer.writerow(row)


def main():
    args = args_parser()

    logger = get_log(args.log_level)
    logger.info("Starting data retrieval and CSV writing process")

    destination_file = os.path.join(args.destination_folder, f"{args.file_name}.csv")
    get_user_data(URL, destination_file)

    if args.filter_by and args.filter_value:
        filter_data(destination_file, destination_file, args.filter_by, args.filter_value)
        logger.info(f"Filtered data based on {args.filter_by} = {args.filter_value}")

    logger.info("Data retrieval and CSV writing process completed")
    logger.info("Started changing the csv file")

    change_and_add_content_into_csv(destination_file)

    logger.info("Changing the cc file was successful")


# Script that can be run from command line:
# python task2.py --destination_folder C:\Users\Admin\Desktop\University\2_year\2st_semester\MultiparadigmProgrammingLanguages\homeworks --file_name filtered_data --filter_by gender --filter_value male --log_level DEBUG
if __name__ == "__main__":
    main()
