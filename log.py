"""
Module for creating a logger.

This module provides a function `get_log()` to create and configure a logger for writing messages to a log file.
"""
import logging

LOG_FORMAT = '%(name)s - %(asctime)s - %(levelname)s - %(message)s'


def get_log():
    """
    Creates and returns a logger to write messages to the 'logger.log' file.

    :return: message logger.
    """
    logger = logging.getLogger("data_base")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('logger.log')
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
