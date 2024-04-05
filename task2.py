import argparse
import logging
import csv
import requests
import os
from datetime import datetime, timedelta


URL = "https://randomuser.me/api/?results=5&format=csv"
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
    with open(destination_file, 'w', encoding='utf-8')as f:
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


def replacement_content(row):
    match row['name.title']:
        case 'Mr':
            row['name.title'] = 'mister'
        case 'Mrs':
            row['name.title'] = 'missis'
        case 'Ms':
            row['name.title'] = 'miss'
        case 'Madame':
            row['name.title'] = 'mademoiselle'
    return row['name.title']


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
            # row['name.title'] = replacement_content(row['name.title'])match row['name.title']:
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
            print(row['location.timezone.offset'])
            hours_offset = int(row['location.timezone.offset'].split(':')[0])
            minutes_offset = int(row['location.timezone.offset'].split(':')[1])
            offset = timedelta(hours=hours_offset, minutes=minutes_offset)
            current_time = datetime.now() + offset
            row['current_time'] = current_time.strftime('%Y-%m-%d %H:%M:%S')

            writer.writerow(row)

        logger.info("Data changed successfully")


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
    change_and_add_content_into_csv(destination_file, logger)
    logger.info("Changing the csv file was successful")

    logger.info("Checking if a path exists")
    if not os.path.exists(args.destination_folder):
        os.makedirs(args.destination_folder)
        logger.info(f"Destination folder '{args.destination_folder}' created")

    os.chdir(args.destination_folder)
    logger.info(f"Changed working directory to '{args.destination_folder}'")

    moving_file = f"{args.file_name}.csv"
    new_destination_path = os.path.join(args.destination_folder, moving_file)
    os.rename(moving_file, new_destination_path)
    logger.info(f"File '{moving_file}' has been moved to the destination folder '{args.destination_folder}'")


# Script that can be run from command line:
# python task2.py --destination_folder . --file_name filtered_data --filter_by gender --filter_value male --log_level DEBUG
if __name__ == "__main__":
    main()
