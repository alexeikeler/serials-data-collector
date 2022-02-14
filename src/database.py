import pandas as pd
import psycopg2

from src.time_measure import measure_func_time


class DataBase:
    
    """
    Class for connecting and updating existing database.
    """
    
    def __init__(self):
        self.__connection = None
     
    def connect(self, dbname: str, user: str, password: str) -> None:
        """
        Method for establishing connection with PostgreSQL database via psycopg2 library.

        Params:    
            dbname: str - database name

            user: str - database user name
            
            password: str - database password
        """

        try:
            self.__connection = psycopg2.connect(
                dbname=dbname, user=user, password=password
            )

        except Exception as e:
            raise SystemError(f"ERROR IN <<DataBase.connect>> :\n{repr(e)}")

        else:
            print("\nConnection established successfully.")

    @measure_func_time
    def update_database(self, data: pd.DataFrame, csv_path: str, separator: str = "|") -> None:
        """
        Method for updating database with new data.

        Params:    
            data: pd.DataFrame - collected data.

            csv_name: str - name of csv file where collected data temporary stored
            for COPY command.
            
            separator: str - separtor used is csv file, default value is |.
        """

        update_querry = """
            
            COPY collected_data
            FROM STDIN
            DELIMITER '|' CSV; 
            
            """
        cursor = self.__connection.cursor()

        try:

            data.to_csv(csv_path, sep=separator, index=True, header=False, mode='w+')

            with open(csv_path) as csv_f:

                cursor.copy_expert(update_querry, csv_f)
                self.__connection.commit()
                cursor.close()

        except Exception as e:
            raise ValueError(f"\nERROR IN <<DataBase.update_database>> :\n{repr(e)}")
