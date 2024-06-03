"""
Main module for data processing.

This module contains functions for adding data from a CSV file to a database,
as well as performing various transactions and analyses on the data.
"""
import csv

from constants import logger
from transaction import (transfer_money, add_discounts, bank_with_most_unique_senders, get_user_transactions,
                         find_bank_of_oldest_client, find_bank_with_largest_capital, get_users_with_debts)
from work_with_db import add_user_into_db, add_account_into_db, add_bank_into_db, delete_data_fr_db


def add_user(users):
    """
    Adds user information to the database.

    :param users: Variable number of dictionaries containing user information.
    :return: None.
    """
    add_user_into_db(users)
    logger.info('User information add successfully.')


def add_bank(banks):
    """
    Adds bank information to the database.

    :param banks: Variable number of dictionaries containing bank information.
    :return: None.
    """
    add_bank_into_db(banks)
    logger.info('Bank information add successfully.')


def add_account(accounts):
    """
    Adds account information to the database.

    :param accounts: Variable number of dictionaries containing account information.
    :return: None.
    """
    add_account_into_db(accounts)
    logger.info('Account information add successfully.')


def add_data_from_csv(file_path):
    """
    Adds data from a CSV file to the database.

    :param file_path: The path to the CSV file containing the data to be inserted.
    :return: None.
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


def main():
    """
    Executes a series of operations:
        - Deletes all data from the database.
        - Adds data from a CSV file into the database.
        - Performs a money transfer between accounts.
        - Adds random discounts to a subset of users.
        - Retrieves users with debts.
        - Finds the bank with the largest capital.
        - Finds the bank serving the oldest client.
        - Determines the bank with the unique senders of transactions.
        - Retrieves transactions for a specific user over the last three months.

    :return: None
    """
    delete_data_fr_db()
    file_path = 'data.csv'
    # table_names = get_table_names()
    add_data_from_csv(file_path)
    transfer_money(10, 7, 4000)
    add_discounts()
    get_users_with_debts()
    find_bank_with_largest_capital()
    find_bank_of_oldest_client()
    bank_with_most_unique_senders()
    get_user_transactions(10)


if __name__ == "__main__":
    main()
