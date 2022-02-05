import requests
import time
import pandas as pd

from tabulate import tabulate
from typing import Iterator
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import date


class Scraper:

    def __init__(self):

        self.todays_content_class = 'news'
        self.current_date_class = 'news-head'

        self.series_class = 'news-w'
        self.series_name_class = 'news_n'
        self.series_episode_added_class = 'news_s'
        self.imdb_rating_class = 'pgs-sinfo_list rating'

        self.genre = 'pgs-sinfo_list'

        self.href_tag = 'a'

    @staticmethod
    def _send_request(link):
        return BeautifulSoup(requests.get(link).text, 'lxml')

    @staticmethod
    def _process_data(raw_data) -> Iterator[str]:
        return [data.get_text(strip=True) for data in raw_data]

    @staticmethod
    def _convert_to_df(req_res: dict) -> pd.DataFrame:

        df = pd.DataFrame.from_dict(req_res, orient='columns')
        df['V'] = df['V'].astype('Int64')
        return df

    @staticmethod
    def _print_pulled_data(df: pd.DataFrame):
        print(tabulate(df, headers=df.columns.values, colalign="center"))

    def pull_data(self, link: str, show_res: bool) -> pd.DataFrame:

        start = time.time()

        req_res: dict = {}
        r1: list[float | None] = []
        r2: list[int | None] = []

        data = self._send_request(link).find(class_=self.todays_content_class)

        req_res['Name'] = self._process_data(
            data.find_all(class_=self.series_name_class)
        )

        req_res['Episodes added'] = self._process_data(
            data.find_all(class_=self.series_episode_added_class)
        )

        req_res['Link'] = [
            link + link_.get('href') for link_ in data.find_all(self.href_tag)
        ]

        for lnk in tqdm(req_res['Link'], desc='Links processing: '):

            concr_ser = self._send_request(lnk)

            rating_info = concr_ser.find(class_=self.imdb_rating_class)
            if rating_info is None:
                r1.append(None)
                r2.append(None)
            else:
                rating_info = rating_info.get_text().split()
                r1.append(float(rating_info[1]))
                r2.append(int(rating_info[2]))

        req_res['R'] = r1
        req_res['V'] = r2

        r_date: list[str] = [date.today().__str__()] * len(r1)
        req_res['Date'] = r_date

        finding_data_time = round(time.time() - start, 2)
        print(f'\nData found successfully in {finding_data_time} sec.\n')

        req_res_df = self._convert_to_df(req_res)

        if show_res:
            self._print_pulled_data(req_res_df)

        return req_res_df

