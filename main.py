import argparse
import pandas as pd

from tabulate import tabulate
from getpass import getpass
from src.scraper import Scraper
from src.database import DataBase


def parse_args():

    parser = argparse.ArgumentParser(description='Arguments description.')

    parser.add_argument(
        '-s',
        '--show',
        required=False,
        dest='show',
        action='store_true',
        help='Print scraped data in DataFrame table.',
    )

    parser.add_argument(
        '-u',
        '--update',
        required=False,
        dest='update',
        action='store_true',
        help='Update database with found data.',
    )

    parser.add_argument(
        '--csvname',
        required=False,
        dest='csvname',
        default='tsd.csv',
        help='Name of csv file with data for psql COPY command. Default value is tsd.csv',
    )

    return parser.parse_args()


def main():

    url = 'http://seasonvar.ru'
    arguments = parse_args()

    sp = Scraper()
    data: pd.DataFrame = sp.pull_data(url)

    if arguments.show:
        print(
            tabulate(
                data, 
                headers=data.columns.values, 
                colalign='center'
            ), 
            '\n'
        )


    if arguments.update:

        dbname = input('Database: ')
        user = input('User: ')
        password = getpass('Password: ')

        db = DataBase()
        db.connect(dbname, user, password)
        db.update_database(data, arguments.csvname)


if __name__ == '__main__':
    main()
