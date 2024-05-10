import re


def validate_user_full_name(full_name):
    """
    Validates and splits the full name into separate parts: first name and last name.
    Filters out all non-alphabetic characters.

    :param full_name: a string containing the user's full name
    :return: a tuple of two elements: first name and last name
    """
    filtered_name = re.sub(r'[^a-zA-Z\s]', '', full_name)
    parts = filtered_name.split()

    if len(parts) == 2:
        return tuple(parts)
    else:
        raise ValueError("Invalid full name format. Please provide both first name and last name separated by space.")


def validate_account_type(account_type):
    """
    Validate the account type against a strict set of allowed values.

    :param account_type: The account type to validate.
    :return: True if the account type is valid, False otherwise.
    """
    allowed_types = ['credit', 'debit']
    if account_type not in allowed_types:
        raise ValueError(f"Not allowed value '{account_type}' for field 'account_type'!")
    return True


def validate_account_status(account_status):
    """
    Validate the account status against a strict set of allowed values.

    :param account_status: The account status to validate.
    :return: True if the account status is valid, False otherwise.
    """
    allowed_statuses = ['gold', 'silver', 'platinum']
    if account_status not in allowed_statuses:
        raise ValueError(f"Not allowed value '{account_status}' for field 'account_status'!")
    return True


def validate_account_number(account_number):
    """
    Validate the account number according to the specified criteria.

    :param account_number: The account number to validate.
    :return: True if the account number is valid, False otherwise.
    """
    if not isinstance(account_number, str):
        raise ValueError("Account number must be a string!")

    account_number = account_number.replace('#', '-').replace('%', '-').replace('_', '-').replace('?', '-').replace('&', '-')

    if len(account_number) != 18:
        raise ValueError("Account number must be 18 characters long!")

    if not account_number.startswith('ID--'):
        raise ValueError("Invalid format! Account number must start with 'ID--'.")

    pattern = re.compile(r'^ID--[a-zA-Z]{1,3}-\d+-[a-zA-Z]{1,3}-\d+$')
    if not pattern.match(account_number):
        raise ValueError("Broken ID! Account number does not match the desired pattern.")

    return True
