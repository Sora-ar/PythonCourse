# import requests
# from constants import API_KEY, logger
# from pprint import pprint
# from db_connection import conn_db
#
#
# def get_exchange_rate():
#     """
#     Gets the current exchange rate between two currencies.
#
#     :return: Exchange rate between base and target currencies.
#     """
#     base_currency = 'USD'
#     target_currency = 'account_currency'
#     url = f'https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}&base={base_currency}&targets={target_currency}'
#
#     try:
#         response = requests.get(url)
#         data = response.json()
#         pprint(data)
#         exchange_rate = data['data'][target_currency]
#         return exchange_rate
#     except Exception as e:
#         logger.info(f'Error while getting the exchange rate: {e}')
#         return None
#
#
# @conn_db
# def get_account_balance(cursor, account_id):
#     cursor.execute('SELECT amount, currency FROM accounts WHERE id=?', (account_id,))
#     account = cursor.fetchone()
#     return account['amount'], account['currency']
#
#
# @conn_db
# def update_account_balance(cursor, account_id, new_balance):
#     cursor.execute('UPDATE accounts SET amount=? WHERE id=?', (new_balance, account_id))
#
#
# def convert_currency(from_currency, to_currency, amount):
#     exchange_rate = get_exchange_rate()
#     if exchange_rate is None:
#         raise Exception(f'Cannot get exchange rate from {from_currency} to {to_currency}')
#     return amount * exchange_rate
#
#
# def transfer_money(sender_id, receiver_id):
#     try:
#         amount = 1000
#         sender_balance, sender_currency = get_account_balance(sender_id)
#         receiver_balance, receiver_currency = get_account_balance(receiver_id)
#
#         if sender_balance < amount:
#             raise Exception('Insufficient funds')
#
#         if sender_currency != receiver_currency:
#             converted_amount = convert_currency(sender_currency, receiver_currency, amount)
#         else:
#             converted_amount = amount
#
#         new_sender_balance = sender_balance - amount
#         new_receiver_balance = receiver_balance + converted_amount
#
#         update_account_balance(sender_id, new_sender_balance)
#         update_account_balance(receiver_id, new_receiver_balance)
#
#         logger.info(f'Transferred {amount} from account {sender_id} to account {receiver_id}')
#
#     except Exception as e:
#         logger.error(f'Error during transfer: {e}')
#         raise
