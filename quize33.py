import logging
import math


def setup_logging():
    logging.basicConfig(filename='logfile.log',
                        level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


def calculate_square_root(num):
    logging.info(f"Number: {num}")
    square_root = math.sqrt(num)
    logging.info(f"Square root of {num} is {square_root}")
    return math.sqrt(num)


setup_logging()
number = 81
calculate_square_root(number)
