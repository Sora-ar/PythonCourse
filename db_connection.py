"""
Module for database connection decorators.

This module provides a decorator `conn_db` for managing database connections.
"""
import sqlite3
from functools import wraps


def conn_db(func):
    """
    Decorator for database connection.

    :param func: internal function, for database connection.
    :return: wrapper function that establishes a connection to the database,
            passes the cursor and other arguments to an internal function,
            commits the changes, and closes the connection.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('task3_db.db')
        cursor = conn.cursor()
        smth = func(cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return smth
    return wrapper
