import argparse


def args_parser():
    parser = argparse.ArgumentParser(
        usage='main.py [-h] [--destination_folder path --file_name name '
              '(--filter_by_gender male/female / --filter_by_number num) '
              '--log_level selected_level]')
    parser.add_argument('--destination_folder', metavar='DESTINATION_FOLDER',
                        help='Path to a folder where output file is going to be placed', required=True)

    parser.add_argument('--file_name', metavar='FILE', default='output',
                        help='Filename for the output CSV file', required=True)

    exclusive_group = parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument('--filter_by_gender', metavar='GENDER', help='Filter data by gender')
    exclusive_group.add_argument('--filter_by_number', metavar='NUMBER', help='Filter data by number of rows')

    parser.add_argument('--log_level', metavar='LOG', nargs='?', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Log level')

    return parser.parse_args()
