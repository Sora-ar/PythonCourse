"""
Module for performing various financial transactions and analyses.

This module contains functions for transferring money between accounts, retrieving exchange rates,
adding discounts to users, analyzing transaction data, and working with banks.
"""
import os
import random
from datetime import datetime, timedelta
from http import HTTPStatus
from collections import defaultdict
from freecurrencyapi import Client
from dotenv import load_dotenv
from constants import logger
from work_with_db import (get_account_balance, update_account_balance, add_transaction_into_db, get_all_user_ids,
                          get_all_transactions, get_all_accounts, get_all_users)

load_dotenv()


def get_exchange_rate(base_currency, target_currency):
    """
    Fetches the exchange rate between two currencies.

    :param base_currency: The base currency code (e.g., "USD").
    :param target_currency: The target currency code (e.g., "EUR").
    :return: The exchange rate from base_currency to target_currency.
    """
    if HTTPStatus == 200:
        client = Client(os.getenv('API_KEY'))
        exchange_rates = client.latest(base_currency, [target_currency])
        exchange_rate = exchange_rates['data'][target_currency]
        return exchange_rate
    if HTTPStatus == 429:
        logger.error('API request limit exceeded')
        return None
    else:
        logger.error(f'HTTP error occurred: {HTTPStatus}')
        return None


def convert_currency(from_currency, to_currency, amount):
    """
    Converts an amount from one currency to another.

    :param from_currency: The currency code of the original currency.
    :param to_currency: The currency code of the target currency.
    :param amount: The amount to be converted.
    :return: The converted amount in the target currency.
    """
    exchange_rate = get_exchange_rate(from_currency, to_currency)
    if exchange_rate is None:
        raise Exception(f'Cannot get exchange rate from {from_currency} to {to_currency}')
    converted_amount = amount * exchange_rate
    return converted_amount


def transfer_money(sender_id, receiver_id, amount):
    """
    Transfers money from one account to another.

    :param sender_id: The ID of the sender's account.
    :param receiver_id: The ID of the receiver's account.
    :param amount: The amount of money to transfer.
    """
    try:
        sender_balance, sender_currency, sender_bank = get_account_balance(sender_id)
        receiver_balance, receiver_currency, receiver_bank = get_account_balance(receiver_id)

        if sender_balance < amount:
            raise Exception('Insufficient funds')

        if sender_currency != receiver_currency:
            converted_amount = convert_currency(sender_currency, receiver_currency, amount)
        else:
            converted_amount = amount

        new_sender_balance = sender_balance - amount
        new_receiver_balance = receiver_balance + converted_amount

        add_transaction_into_db(sender_id, receiver_id, sender_currency, sender_bank, receiver_bank, amount)

        update_account_balance(sender_id, new_sender_balance)
        update_account_balance(receiver_id, new_receiver_balance)

        logger.info(f'Transferred {amount} from account {sender_id} to account {receiver_id}')

    except Exception as e:
        logger.error(f'Error during transfer: {e}')
        raise


def assign_random_discounts(user_ids, max_users=10):
    """
    Assigns random discounts to a subset of users.

    :param user_ids: List of user IDs to select from.
    :param max_users: Maximum number of users to assign discounts to.
    :return: A dictionary with user IDs as keys and their assigned discounts as values.
    """
    num_users = random.randint(1, min(len(user_ids), max_users))
    selected_users = random.sample(user_ids, num_users)
    discounts = [25, 30, 50]
    user_discounts = {user_id: random.choice(discounts) for user_id in selected_users}
    return user_discounts


def add_discounts():
    """
    Adds random discounts to a subset of users and logs the assignments.

    :return: None.
    """
    user_ids = get_all_user_ids()
    user_discounts = assign_random_discounts(user_ids)
    for user_id, discount in user_discounts.items():
        logger.info(f'Assigned discounts: User ID: {user_id}, Discount: {discount}')


def get_user_transactions(user_id):
    """
    Retrieves transactions for a specific user over the last three months.

    :param user_id: The ID of the user.
    :return: None.
    """
    current_date = datetime.now()
    three_months_ago = current_date - timedelta(days=90)

    transactions = get_all_transactions()
    accounts = get_all_accounts()

    user_accounts = [account[0] for account in accounts if account[1] == user_id]

    user_transactions = []
    for transaction in transactions:
        if (transaction[2] in user_accounts or transaction[4] in user_accounts) \
                and datetime.strptime(transaction[7], '%Y-%m-%d %H:%M:%S.%f') >= three_months_ago:
            user_transactions.append(transaction)
    logger.info(f'Transactions of user {user_id} for last 3 months: \n{user_transactions}')


def bank_with_most_unique_senders():
    """
    Determines the bank with the unique senders of transactions.

    :return: None.
    """
    bank_user_counts = {}
    transactions = get_all_transactions()

    for transaction in transactions:
        sender_bank = transaction[1]
        sender_id = transaction[2]

        if sender_bank not in bank_user_counts:
            bank_user_counts[sender_bank] = set()

        bank_user_counts[sender_bank].add(sender_id)

    max_unique_users_bank = None
    max_unique_users_count = 0

    for bank, users in bank_user_counts.items():
        if len(users) > max_unique_users_count:
            max_unique_users_count = len(users)
            max_unique_users_bank = bank

    logger.info(f'Bank with most unique senders: {max_unique_users_bank} '
                f'with {max_unique_users_count} unique senders')


def find_bank_of_oldest_client():
    """
    Finds the bank serving the oldest client based on the date of the first transaction.

    :return: None.
    """
    transactions = get_all_transactions()

    oldest_transaction = min(transactions, key=lambda x: datetime.strptime(x[7], '%Y-%m-%d %H:%M:%S.%f'))
    oldest_client_bank = oldest_transaction[1]

    logger.info(f'Bank serving the oldest client: {oldest_client_bank} '
                f'(first transaction date: {oldest_transaction[7]})')


def find_bank_with_largest_capital():
    """
    Finds the bank with the largest capital based on the sum of user account balances.

    :return: None.
    """
    bank_capitals = defaultdict(int)
    accounts = get_all_accounts()

    for account in accounts:
        bank_id = account[4]
        amount = account[6]
        bank_capitals[bank_id] += amount

    bank_with_largest_capital = max(bank_capitals, key=bank_capitals.get)

    logger.info(f'Bank with the largest capital: {bank_with_largest_capital} '
                f'(total capital: {bank_capitals[bank_with_largest_capital]})')


def get_users_with_debts():
    """
    Retrieves the full names of users with debts based on their account balances.

    :return: None.
    """
    users = get_all_users()
    accounts = get_all_accounts()

    user_balances = {user[0]: 0 for user in users}

    for account in accounts:
        user_id = account[0]
        amount = account[1]
        user_balances[user_id] += amount

    users_with_debts = [user for user in users if user_balances[user[0]] < 0]

    if len(users_with_debts) > 0:
        user_names_with_debts = [f'{user[1]} {user[2]}' for user in users_with_debts]
        logger.info(f"Users with debts: {', '.join(user_names_with_debts)}")
    else:
        logger.info('No debtors found.')
