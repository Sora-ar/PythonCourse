import argparse
import logging
import csv
import requests


# 1. Set up new file logger and don’t forget to log information about each step
def get_log():
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


# 2. Explore the data provider site and download a csv file with 5k user accounts using your script.
def get_data_into_csv(logger):
    logger.info("Starting data retrieval and CSV writing process")

    url = "https://randomuser.me/api/?results=5000"
    response = requests.get(url)
    result = response.json()['results']

    with open('user_data.csv', 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=list(result[0].keys()))
        csv_writer.writeheader()
        csv_writer.writerows(result)

    logger.info("Data retrieval and CSV writing process completed")

    # with open('user_data.csv', 'r', encoding='utf-8') as file:
    #     csv_reader = csv.DictReader(file)
    #     for row in csv_reader:
    #         print(row)


def main():
    logger = get_log()
    get_data_into_csv(logger)


if __name__ == "__main__":
    main()
