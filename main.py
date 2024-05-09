import csv

from db_connection import conn_db
from constants import logger
from work_with_db import *


# def parse_user_full_name(user):
#     """
#     Splits the full username into separate parts: first name and last name.
#
#     :param user: a string containing the user's full name
#     :return: a tuple of two elements: first name and last name
#     """
#     full_name = user['user_full_name']
#     name, surname = full_name.split()
#     logger.info(f'Full name "{full_name}" successfully split into: name "{name}" and surname "{surname}".')
#     return name, surname


def add_user(users):
    """
    Adds user information to the database.

    :param users: Variable number of dictionaries containing user information.
    :return: None
    """
    add_user_into_db(users)
    logger.info(f'User information add successfully.')


def add_bank(banks):
    """
    Adds bank information to the database.

    :param banks: Variable number of dictionaries containing bank information.
    :return: None
    """
    add_bank_into_db(banks)
    logger.info(f'Bank information add successfully.')


def add_account(accounts):
    """
    Adds account information to the database.

    :param accounts: Variable number of dictionaries containing account information.
    :return: None
    """
    add_account_into_db(accounts)
    logger.info(f'Account information add successfully.')


def add_data_from_csv(file_path):
    """
    Adds data from a CSV file to the database.

    :param file_path: Path to the CSV file containing the data.
    :return: None
    """
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'user_full_name' in row:
                add_user(row)
            if 'bank_name' in row:
                add_bank(row)
            if 'account_type' in row:
                add_account(row)
            else:
                logger.error(f'Unknown data type in CSV file "{file_path}". Cannot add data.')


#
# @conn_db
# def update_user(cursor):


#
# @conn_db
# def transfer_money(cursor):


#
# def convert_currency():


def main():
    delete_data_fr_db()
    file_path = 'data.csv'
    add_data_from_csv(file_path)


if __name__ == "__main__":
    main()
