from unittest.mock import MagicMock, patch
from main import add_user


@patch('main.add_user_into_db')
@patch('main.logger')
def test_add_user(mock_logger, mock_add_user_into_db):
    users = {'user_id': '1', 'user_full_name': 'John Doe', 'birth_day': '27.02.1989', 'user_accounts': '123,897',
             'account_type': 'credit', 'account_number': '1568468', 'account_currency': 'USD',
             'account_amount': '2000', 'account_status': 'gold', 'bank_id': '1', 'bank_name': 'Bank Aaa'}
    add_user(users)

    mock_add_user_into_db.assert_called_once_with(users)

    mock_logger.info.assert_called_once_with('User information add successfully.')
