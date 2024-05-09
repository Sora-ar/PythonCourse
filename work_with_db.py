import sqlite3

from db_connection import conn_db
from constants import logger
from validation import validate_user_full_name


@conn_db
def delete_data_fr_db(cursor):
    """
    Deletes all data from the users, banks, and accounts tables in the database.

    :param cursor: SQLite cursor object for executing SQL queries.
    :return: None
    """
    try:
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM banks")
        cursor.execute("DELETE FROM accounts")
        cursor.connection.commit()

        logger.info("All data successfully deleted from the database.")
    except sqlite3.Error as e:
        logger.error(f"Error deleting data from the database: {e}")


@conn_db
def add_user_into_db(cursor, users):
    """
    Adds user information to the database.

    :param cursor: SQLite cursor object for executing SQL queries.
    :param users: Variable number of dictionaries containing user information.
    :return: None
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
    :return: None
    """
    if isinstance(banks, dict):
        banks = [banks]

    for bank in banks:
        cursor.execute('INSERT INTO banks (name, id) VALUES (?, ?)', (bank['bank_name'], bank['bank_id']))


@conn_db
def add_account_into_db(cursor, accounts):
    """
    Adds account information to the database.

    :param cursor: SQLite cursor object for executing SQL queries.
    :param accounts: Variable number of dictionaries containing account information.
    :return: None
    """
    if isinstance(accounts, dict):
        accounts = [accounts]

    for account in accounts:
        cursor.execute('INSERT INTO accounts (type, account_number, currency, amount, status, bank_id, user_id) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?)', (account['account_type'], account['account_number'],
                                                        account['account_currency'], account['account_amount'],
                                                        account['account_status'], account['bank_id'],
                                                        account['user_id']))


@conn_db
def delete_user(cursor, user_id):
    """
    Deletes a specific user from the database.

    :param cursor: SQLite cursor object for executing SQL queries.
    :param user_id: The ID of the user to be deleted.
    :return: None
    """
    cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
    logger.info(f'User with ID {user_id} deleted successfully.')
