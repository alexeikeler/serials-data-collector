import requests
import pandas as pd

from typing import Iterator
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import date

from src.time_measure import measure_func_time


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
        df['Voted'] = df['Voted'].astype('Int64')
        return df

    @measure_func_time
    def pull_data(self, link: str) -> pd.DataFrame:

        req_res: dict = dict()

        rating: list[str | None] = []
        voted: list[str | None] = []

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
                rating.append(None)
                voted.append(None)
            
            else:
                
                rating_info = rating_info.get_text().split()
                
                rating.append(
                    float(rating_info[1])
                )
                
                voted.append(
                    int(rating_info[2])
                )

        req_res['IMDB Rating'] = rating
        req_res['Voted'] = voted
        req_res['Date'] = [date.today().__str__()] * len(rating)
        
        req_res_df = self._convert_to_df(req_res)

        return req_res_df
