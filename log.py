import logging
from constants import LOG_FILE, LOG_FORMAT


def get_log(log_level):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('user_data')

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(log_level)
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logging.getLogger().handlers = []

    return logger
