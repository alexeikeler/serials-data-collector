import argparse
import pandas as pd

from scraper import Scraper
from database import DataBase

CONNECTION_STRING = "postgresql://postgres:postgres@localhost/SerialsData"
LINK = "http://seasonvar.ru"


def initialize_argparser():

    parser = argparse.ArgumentParser(description='Arguments description.')

    parser.add_argument(
        '-s',
        '--show',
        required=False,
        dest='show',
        action='store_true',
        help='Print scraped data in DataFrame table.'
    )

    parser.add_argument(
        '-u',
        '--update',
        required=False,
        dest='update',
        action='store_true',
        help='Update database with found data.'
    )

    parser.add_argument(
        '--csvname',
        required=False,
        dest='csvname',
        default='tsd.csv',
        help='Name of csv file with data for psql COPY command. Default value is tsd.csv'
    )

    return parser.parse_args()


def main():

    arguments = initialize_argparser()

    sp = Scraper()
    request_result: pd.DataFrame = sp.pull_data(LINK, arguments.show)

    if arguments.update:

        querry: str = """
         COPY collected_data
         FROM STDIN
         DELIMITER '|' CSV;
         """

        db = DataBase()
        db.connect(CONNECTION_STRING)
        db.update_database(request_result, querry, arguments.csvname)


if __name__ == "__main__":
    main()
