import os
import csv
import shutil
from collections import Counter
from constants import DOB_DATE, DOB_AGE, COUNTRY, NAME, AGE


def create_new_data_structure(filtered_data, logger):
    grouped_user_data = {}

    for user in filtered_data:
        user_year = user[DOB_DATE][-4:]
        user_country = user[COUNTRY]
        decade = f'{user_year[2]}0-th'

        grouped_user_data.setdefault(decade, {}).setdefault(user_country, []).append(user)

    logger.info('Data append successfully')
    return grouped_user_data, filtered_data


def generate_filename(grouped_user_data, decade, country):
    max_age = max(user[DOB_AGE] for user in grouped_user_data[decade][country])

    total_registered_years = sum(int(user[AGE]) for user in grouped_user_data[decade][country])
    num_users = len(grouped_user_data[decade][country])
    avr_registered_years = total_registered_years / num_users

    all_id_names = [user[NAME] for user in grouped_user_data[decade][country]]
    id_name_counts = Counter(all_id_names)
    popular_id = id_name_counts.most_common(1)[0][0]

    return f'max_age_{max_age}_avg_registered_{avr_registered_years}_popular_id_{popular_id}.csv'


def create_dirs(path, destination):
    folder = os.path.join(path, destination)
    os.makedirs(folder, exist_ok=True)
    return folder


def file_entry_for_folders(file_path, user_data, grouped_user_data, decade, country):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=user_data[0].keys())
        writer.writeheader()
        writer.writerows(list(grouped_user_data[decade][country]))


def create_sub_folders(destination_folder, grouped_user_data, user_data, logger):
    for decade in grouped_user_data:
        decade_folder = create_dirs(destination_folder, decade)

        for country in grouped_user_data[decade]:
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


def get_full_folder_structure(destination_folder, logger, level=0):
    items = os.listdir(destination_folder)

    items.sort()

    for item in items:
        item_path = os.path.join(destination_folder, item)
        is_folder = os.path.isdir(item_path)
        type_flag = 'DIR' if is_folder else 'FILE'
        logger.info('\t' * level + f'{item}: {type_flag}')

        if is_folder:
            get_full_folder_structure(item_path, logger, level + 1)


def archive_destination_folder(destination_folder):
    shutil.make_archive(destination_folder, 'zip', destination_folder)
