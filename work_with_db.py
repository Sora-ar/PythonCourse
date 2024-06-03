"""
Module for database operations.

This module provides functions for interacting with the SQLite database,
including adding, updating, and deleting data, as well as retrieving data.
"""
import sqlite3
from db_connection import conn_db
from constants import logger
from datetime import datetime
from validation import validate_user_full_name


@conn_db
def delete_data_fr_db(cursor):
    """
    Deletes all data from the users, banks, and accounts tables in the database.

    :param cursor: SQLite cursor object for executing SQL queries.
    :return: None.
    """
    try:
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM banks")
        cursor.execute("DELETE FROM accounts")
        cursor.execute("DELETE FROM transactions")
        cursor.connection.commit()

        logger.info("All data successfully deleted from the database.")
    except sqlite3.Error as e:
        logger.error(f"Error deleting data from the database: {e}")


@conn_db
def get_table_names(cursor):
    """
    Retrieve the names of all tables in the database.

    :param cursor: Database cursor.
    :return: List of table names.
    """
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    return [name[0] for name in table_names]


# @conn_db
# def add_data_into_db(cursor, table_name, data_list):
#     """
#     Adds data into the specified table of the database.
#
#     :param cursor: SQLite cursor object for executing SQL queries.
#     :param table_name: Name of the table to which data will be added.
#     :param data_list: List of dictionaries containing data to be added.
#     :return: None
#     """
#     if isinstance(data_list, dict):
#         data_list = [data_list]
#
#     for data in data_list:
#         values = tuple(data[key] for key in data.keys())
#         placeholders = ', '.join(['?' for _ in range(len(data))])
#
#         columns = ', '.join(data.keys())
#         print(columns)
#         query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
#
#         try:
#             cursor.execute(query, values)
#             logger.info(f'{table_name.capitalize()} information added successfully.')
#         except sqlite3.Error as e:
#             logger.error(f"Error adding {table_name} information: {e}")


@conn_db
def add_user_into_db(cursor, users):
    """
    Adds user information to the database.

    :param cursor: SQLite cursor object for executing SQL queries.
    :param users: Variable number of dictionaries containing user information.
    :return: None.
    """
    if isinstance(users, dict):
        users = [users]

    for user in users:
        name, surname = validate_user_full_name(user['user_full_name'])
        cursor.execute('INSERT INTO users (name, surname, birth_day, accounts) VALUES (?, ?, ?, ?)',
                       (name, surname, user['birth_day'], user['user_accounts']))


@conn_db
def add_bank_into_db(cursor, banks):
    """
    Adds bank information to the database.

    :param cursor: SQLite cursor object for executing SQL queries.
    :param banks: Variable number of dictionaries containing bank information.
    :return: None.
    """
    if isinstance(banks, dict):
        banks = [banks]

    for bank in banks:
        cursor.execute('INSERT INTO banks (name) VALUES (?)', (bank['bank_name']))


@conn_db
def add_account_into_db(cursor, accounts):
    """
    Adds account information to the database.

    :param cursor: SQLite cursor object for executing SQL queries.
    :param accounts: Variable number of dictionaries containing account information.
    :return: None.
    """
    if isinstance(accounts, dict):
        accounts = [accounts]

    for account in accounts:
        cursor.execute('INSERT INTO accounts (type, account_number, currency, amount, status, bank_id, user_id) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?)', (account['account_type'], account['account_number'],
                                                        account['account_currency'], account['account_amount'],
                                                        account['account_status'], account['bank_id'],
                                                        account['user_id']))


# @conn_db
# def update_data(cursor, table_name, **kwargs):
#     """
#     Update data in the specified table of the database.
#
#     :param cursor: Database cursor.
#     :param table_name: Name of the table to be updated.
#     :param kwargs: Key-value pairs where keys represent column names and values represent new values.
#     :return: None
#     """
#     try:
#         columns = ', '.join([f"{column} = ?" for column in kwargs.keys()])
#         values = tuple(kwargs.values())
#         query = f"UPDATE {table_name} SET {columns} WHERE id=?"
#
#         cursor.execute(query, (*values, kwargs['id']))
#
#         logger.info(f'{table_name.capitalize()} information updated successfully.')
#     except sqlite3.Error as e:
#         logger.error(f"Error updating {table_name} information: {e}")


@conn_db
def update_user(cursor, user_id, new_name, new_surname, new_birth_day=None, new_accounts=None):
    """
    Update user information in the database.

    :param cursor: Database cursor.
    :param user_id: ID of the user to be updated.
    :param new_name: New name of the user.
    :param new_surname: New surname of the user.
    :param new_birth_day: New birthday of the user (optional).
    :param new_accounts: New accounts of the user (optional).
    :return: None.
    """
    try:
        cursor.execute('UPDATE users ounSET name=?, surname=?, birth_day=?, accounts=? WHERE id=?',
                       (new_name, new_surname, new_birth_day, new_accounts, user_id))
        logger.info(f'User information updated successfully.')
    except sqlite3.Error as e:
        logger.error(f"Error updating user information: {e}")


@conn_db
def update_bank(cursor, bank_id, new_name):
    """
    Update bank information in the database.

    :param cursor: Database cursor.
    :param bank_id: ID of the bank to be updated.
    :param new_name: New name of the bank.
    :return: None.
    """
    try:
        cursor.execute('UPDATE banks SET name=? WHERE id=?', (new_name, bank_id))
        logger.info(f'Bank information updated successfully.')
    except sqlite3.Error as e:
        logger.error(f"Error updating bank information: {e}")


@conn_db
def update_account(cursor, account_id, new_type, new_number, new_currency, new_amount, new_status):
    """
    Update account information in the database.

    :param cursor: Database cursor.
    :param account_id: ID of the account to be updated.
    :param new_type: New type of the account.
    :param new_number: New number of the account.
    :param new_currency: New currency of the account.
    :param new_amount: New amount of the account.
    :param new_status: New status of the account.
    :return: None.
    """
    try:
        cursor.execute('UPDATE accounts SET type=?, account_number=?, currency=?, amount=?, status=? WHERE id=?',
                       (new_type, new_number, new_currency, new_amount, new_status, account_id))
        logger.info(f'Account information updated successfully.')
    except sqlite3.Error as e:
        logger.error(f"Error updating account information: {e}")


@conn_db
def delete_user(cursor, user_id):
    """
    Deletes a specific user from the database.

    :param cursor: SQLite cursor object for executing SQL queries.
    :param user_id: The ID of the user to be deleted.
    :return: None.
    """
    cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
    logger.info(f'User with ID {user_id} deleted successfully.')


@conn_db
def get_account_balance(cursor, account_id):
    """
     Retrieve the balance, currency, and bank name for a given account ID.

    :param cursor: Database cursor.
    :param account_id: ID of the account to retrieve balance for.
    :return: Tuple containing (amount, currency, bank_name).
    :raises ValueError: If account with the specified ID is not found.
    """
    cursor.execute('SELECT amount, currency, bank_id FROM accounts WHERE id=?', (account_id,))
    account = cursor.fetchone()
    cursor.execute('SELECT name FROM banks WHERE id=?', (account[2],))
    bank = cursor.fetchone()
    if account:
        return account[0], account[1], bank[0]
    else:
        raise ValueError(f'Account with ID {account_id} not found')


@conn_db
def update_account_balance(cursor, account_id, new_balance):
    """
    Update the balance for a given account ID.

    :param cursor: Database cursor.
    :param account_id: ID of the account to update balance for.
    :param new_balance: New balance to set for the account.
    :return: None.
    """
    cursor.execute('UPDATE accounts SET amount=? WHERE id=?', (new_balance, account_id))


@conn_db
def add_transaction_into_db(cursor, sender_id, receiver_id, sender_currency, sender_bank, receiver_bank, amount,
                            transaction_time=None):
    """
    Add a transaction to the database.

    :param cursor: Database cursor.
    :param sender_id: ID of the sender's account.
    :param receiver_id: ID of the receiver's account.
    :param sender_currency: Currency in which the amount was sent.
    :param sender_bank: Name of the sender's bank.
    :param receiver_bank: Name of the receiver's bank.
    :param amount: Amount of the transaction.
    :param transaction_time: Time of the transaction. If None, current time is used.
    :return: None.
    """
    if transaction_time is None:
        transaction_time = datetime.now()

    cursor.execute('INSERT INTO transactions (bank_sender_name, account_sender_id, bank_receiver_name, '
                   'account_receiver_id, sent_currency, sent_amount, datetime) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (sender_bank, sender_id, receiver_bank, receiver_id, sender_currency, amount, transaction_time))


@conn_db
def get_all_user_ids(cursor):
    """
    Retrieve all user IDs from the database.

    :param cursor: Database cursor.
    :return: List of user IDs.
    """
    cursor.execute('SELECT id FROM users')
    user_ids = cursor.fetchall()
    return [user_id[0] for user_id in user_ids]


@conn_db
def get_all_accounts(cursor):
    """
    Retrieve all accounts from the database.

    :param cursor: Database cursor.
    :return: List of tuples containing account information.
    """
    cursor.execute('SELECT id, user_id, type, account_number, bank_id, currency, amount, status FROM accounts')
    return cursor.fetchall()


@conn_db
def get_all_users(cursor):
    """
    Retrieve all users from the database.

    :param cursor: Database cursor.
    :return: List of tuples containing user information.
    """
    cursor.execute('SELECT id, name, surname, birth_day, accounts FROM users')
    return cursor.fetchall()


@conn_db
def get_all_transactions(cursor):
    """
    Retrieve all transactions from the database.

    :param cursor: Database cursor.
    :return: List of tuples containing transaction information.
    """
    cursor.execute('SELECT id, bank_sender_name, account_sender_id, bank_receiver_name, account_receiver_id, '
                   'sent_currency, sent_amount, datetime FROM transactions')
    return cursor.fetchall()


@conn_db
def delete_user(cursor, user_id):
    """
    Delete a user from the database by user ID.

    :param cursor: Database cursor.
    :param user_id: ID of the user to be deleted.
    :return: None.
    """
    cursor.execute('DELETE FROM users WHERE id=?', (user_id,))


@conn_db
def delete_account(cursor, account_id):
    """
    Delete an account from the database by account ID.

    :param cursor: Database cursor.
    :param account_id: ID of the account to be deleted.
    :return: None.
    """
    cursor.execute('DELETE FROM accounts WHERE id=?', (account_id,))


def delete_incomplete_users():
    """
    Deletes users from the database who have incomplete information.

    A user is considered incomplete if any of the following fields are missing:
    name, surname, birth_day, accounts.

    :return: None.
    """
    users = get_all_users()
    for user in users:
        user_id, name, surname, birth_day, accounts = user
        if not (name and surname and birth_day and accounts):
            delete_user(user_id)
            logger.info(f'Deleted incomplete user with ID {user_id}')


def delete_incomplete_accounts():
    """
    Deletes accounts from the database that have incomplete information.

    An account is considered incomplete if any of the following fields are missing:
    account_type, account_number, bank_id, currency, amount, status, user_id.

    :return: None.
    """
    accounts = get_all_accounts()
    for account in accounts:
        account_id, user_id, account_type, account_number, bank_id, currency, amount, status = account
        if not (account_type and account_number and currency and amount and status and bank_id and user_id):
            delete_account(account_id)
            logger.info(f'Deleted incomplete account with ID {account_id}')


def remove_incomplete_data():
    """
    Removes all users and accounts with incomplete information from the database.

    :return: None.
    """
    delete_incomplete_users()
    delete_incomplete_accounts()
    logger.info('Removed all incomplete users and accounts')
