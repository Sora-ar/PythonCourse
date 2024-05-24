import requests
from datetime import datetime, timedelta
from constants import (TIMEZONE_OFFSET, CURRENT_TIME, API_DATE_FORMAT, TIME_FORMAT,
                       GLOBAL_INDEX, TITLE, DATE_FORMAT, DOB_DATE, REGISTERED_DATE)


def get_user_data(url, destination_file):
    response = requests.get(url)
    with open(destination_file, 'w', encoding='utf-8') as f:
        f.write(response.text)


def get_current_time(row):
    hours_offset, minutes_offset = map(int, row[TIMEZONE_OFFSET].split(':'))
    offset = timedelta(hours=hours_offset, minutes=minutes_offset)
    current_time = datetime.now() + offset
    return current_time.strftime(f'{API_DATE_FORMAT} {TIME_FORMAT}')


def convert_date(date_str, date_format):
    user_date = datetime.strptime(date_str, f'{API_DATE_FORMAT}T{TIME_FORMAT}.%fZ')
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


def change_content(filtered_data, logger):
    try:
        for i, row in enumerate(filtered_data, start=1):
            row[GLOBAL_INDEX] = i
            row[TITLE] = replacement_prefix(row[TITLE])
            row[DOB_DATE] = convert_date(row[DOB_DATE], DATE_FORMAT)
            row[REGISTERED_DATE] = convert_date(row[REGISTERED_DATE], f'{DATE_FORMAT}, {TIME_FORMAT}')
            row[CURRENT_TIME] = get_current_time(row)

        logger.info('Data changed successfully')

        return filtered_data
    except TypeError:
        logger.error("filtered_data is empty or not iterable")
        return None
