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
def update_user(cursor, user_id, new_name, new_surname, new_birth_day=None, new_accounts=None):
    """
    Update user information in the database.

    :param cursor: Database cursor.
    :param user_id: ID of the user to be updated.
    :param new_name: New name of the user.
    :param new_surname: New surname of the user.
    :param new_birth_day: New birthday of the user (optional).
    :param new_accounts: New accounts of the user (optional).
    :return: None
    """
    try:
        cursor.execute("""
            UPDATE users 
            SET name=?, surname=?, birth_day=?, accounts=? 
            WHERE id=?
        """, (new_name, new_surname, new_birth_day, new_accounts, user_id))
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
    :return: None
    """
    try:
        cursor.execute("""
            UPDATE banks 
            SET name=? 
            WHERE id=?
        """, (new_name, bank_id))
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
    :return: None
    """
    try:
        cursor.execute("""
            UPDATE accounts
            SET type=?, account_number=?, currency=?, amount=?, status=?
            WHERE id=?
        """, (new_type, new_number, new_currency, new_amount, new_status, account_id))
        logger.info(f'Account information updated successfully.')
    except sqlite3.Error as e:
        logger.error(f"Error updating account information: {e}")


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
