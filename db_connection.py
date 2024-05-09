import sqlite3


def conn_db(func):
    """
    Decorator for database connection

    :param func: internal function, for database connection
    :return: wrapper function that establishes a connection to the database,
            passes the cursor and other arguments to an internal function,
            commits the changes, and closes the connection
    """
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('task3_db.db')
        cursor = conn.cursor()
        func(cursor, *args, **kwargs)
        conn.commit()
        cursor.close()
        conn.close()

    return wrapper
