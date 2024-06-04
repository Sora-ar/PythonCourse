"""
Initialize the logger instance for logging purposes.

This code imports the `get_log` function from the `log` module and uses it to create a `logger` instance. This logger
will be used throughout the application for logging informational, warning, error, and debug messages.

Modules:
    log: A module containing the `get_log` function to initialize the logger.
"""
from log import get_log
logger = get_log()
