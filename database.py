import pandas as pd
import psycopg2
import os
import time


class DataBase:
    def __init__(self):
        self.__connection = None

    def connect(self, conn_str: str) -> None:

        try:
            self.__connection = psycopg2.connect(conn_str)

        except Exception as e:
            raise SystemError(f"ERROR IN <<DataBase.connect>> :\n{repr(e)}")

        else:
            print("\nConnection established successfully.")

    def update_database(
        self, data: pd.DataFrame, querry: str, csv_path: str, separator: str = "|"
    ) -> None:

        start = time.time()
        cursor = self.__connection.cursor()

        try:

            os.remove(csv_path)
            data.to_csv(csv_path, sep=separator, index=True, header=False)

            with open(csv_path) as csv_f:

                cursor.copy_expert(querry, csv_f)
                self.__connection.commit()
                cursor.close()

        except Exception as e:
            raise ValueError(f'\nERROR IN <<DataBase.update_database>> :\n{repr(e)}')

        else:
            update_time = round(time.time() - start, 2)
            print(f'\nDatabase updated successfully in {update_time} sec.\n')

    def exequte_querry(self, querry: str):
        pass
