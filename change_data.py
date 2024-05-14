from datetime import datetime, timedelta
from constants import (TIMEZONE_OFFSET, CURRENT_TIME, CURRENT_TIME_DATA_FORMAT, TIME_FORMAT,
                       GLOBAL_INDEX, TITLE, DATA_FORMAT, DOB_DATE, REGISTERED_DATE)


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


def change_content(filtered_data, logger):
    try:
        for i, row in enumerate(filtered_data, start=1):
            row[GLOBAL_INDEX] = i
            row[TITLE] = replacement_prefix(row[TITLE])
            row[DOB_DATE] = convert_date(row[DOB_DATE], DATA_FORMAT)
            row[REGISTERED_DATE] = convert_date(row[REGISTERED_DATE],
                                                '{data}, {time}'.format(data=DATA_FORMAT, time=TIME_FORMAT))
            row[CURRENT_TIME] = get_current_time(row)

        logger.info('Data changed successfully')

        return filtered_data
    except TypeError:
        logger.error("filtered_data is empty or not iterable")
        return None
