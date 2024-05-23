import csv

from constants import logger
from db_connection import conn_db
from transaction import get_exchange_rate, transfer_money
from work_with_db import add_user_into_db, add_account_into_db, add_bank_into_db, delete_data_fr_db


@conn_db
def get_table_names(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    print(table_names)
    return [name[0] for name in table_names]


def add_user(users, table_name):
    """
    Adds user information to the database.

    :param users: Variable number of dictionaries containing user information.
    :return: None
    """
    # add_data_into_db(table_name[2], users)
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


def add_data_from_csv(file_path, table_name):
    """
    Adds data from a CSV file to the database.

    :param file_path: The path to the CSV file containing the data to be inserted.
    :param table_name: The name of the table into which the data should be inserted.
                       This parameter is used for logging and validation purposes.
    :return:
    """
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'user_full_name' in row:
                add_user(row, table_name)
            if 'bank_name' in row:
                add_bank(row)
            if 'account_type' in row:
                add_account(row)
            else:
                logger.error(f'Unknown data type in CSV file "{file_path}". Cannot add data.')


def main():
    delete_data_fr_db()
    file_path = 'data.csv'
    table_names = get_table_names()
    print(table_names[2])
    add_data_from_csv(file_path, table_names)
    hj = get_exchange_rate()
    print(hj)
    sender = 2
    receiver = 4
    transfer_money(sender, receiver)


if __name__ == "__main__":
    main()
