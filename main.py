import os
import requests
from constants import *
from log import get_log
from args_parser import args_parser
from filter_data import filter_data
from change_data import change_content
from work_with_folders import (create_new_data_structure, create_sub_folders, del_data_before_1960th,
                               get_full_folder_structure, archive_destination_folder)


def get_user_data(url, destination_file):
    response = requests.get(url)
    with open(destination_file, 'w', encoding='utf-8') as f:
        f.write(response.text)


def main():
    args = args_parser()
    logger = get_log(args.log_level)

    logger.info('Starting data retrieval and CSV writing process')
    destination_folder = args.destination_folder
    destination_file = os.path.join(destination_folder, f'{args.file_name}.csv')
    get_user_data(URL, destination_file)

    if args.filter_by_gender or args.filter_by_number and args.filter_value:
        filtered_data = filter_data(destination_file, args.filter_by_gender or args.filter_by_number, args.filter_value)

        logger.info(f'Filtered data based on {args.filter_by_gender or args.filter_by_number} = {args.filter_value}')
    logger.info('Data retrieval and CSV writing process completed')

    logger.info('Started changing the csv file')
    filtered_data = change_content(filtered_data, logger)
    logger.info('Changing the csv file was successful')

    logger.info('Checking if a path exists')
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        logger.info(f'Destination folder "{destination_folder}" created')

    os.chdir(destination_folder)
    logger.info(f'Changed working directory to "{destination_folder}"')

    moving_file = f'{args.file_name}.csv'
    new_destination_path = os.path.join(destination_folder, moving_file)
    os.rename(moving_file, new_destination_path)
    logger.info(f'File "{moving_file}" has been moved to the destination folder "{destination_folder}"')

    logger.info('Started changing the user data structure')
    user_data_group, user_data = create_new_data_structure(filtered_data, logger)
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
# python main.py --destination_folder . --file_name begin_data --filter_by_gender filter_by_gender --filter_value male --log_level DEBUG
# python main.py --destination_folder C:\Users\Admin\Desktop\University\2_year\2st_semester\MultiparadigmProgrammingLanguages\homeworks\ --file_name begin_data --filter_by_gender filter_by_gender --filter_value male --log_level DEBUG
if __name__ == '__main__':
    main()
