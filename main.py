import argparse
import pandas as pd

from getpass import getpass
from scraper import Scraper
from database import DataBase

LINK = "http://seasonvar.ru"


def parse_args():

    parser = argparse.ArgumentParser(description="Arguments description.")

    parser.add_argument(
        "-s",
        "--show",
        required=False,
        dest="show",
        action="store_true",
        help="Print scraped data in DataFrame table.",
    )

    parser.add_argument(
        "-u",
        "--update",
        required=False,
        dest="update",
        action="store_true",
        help="Update database with found data.",
    )

    parser.add_argument(
        "--csvname",
        required=False,
        dest="csvname",
        default="tsd.csv",
        help="Name of csv file with data for psql COPY command. Default value is tsd.csv",
    )

    return parser.parse_args()


def main():

    arguments = parse_args()

    sp = Scraper()
    request_result: pd.DataFrame = sp.pull_data(LINK, arguments.show)

    if arguments.update:

        query: str = """
         COPY collected_data
         FROM STDIN
         DELIMITER '|' CSV;
         """

        dbname = input("Database: ")
        user = input("User: ")
        password = getpass("Password: ")

        db = DataBase()
        db.connect(dbname, user, password)
        db.update_database(request_result, query, arguments.csvname)


if __name__ == "__main__":
    main()
