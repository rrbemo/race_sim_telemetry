import pkgutil

import pandas as pd
import psycopg2
import yaml


class SimStore:
    __conn = None

    def __init__(self):
        print("connecting")
        self.__connect()

    def __del__(self):
        self.__close()

    def __connect(self):
        # open the yaml file and read in the values
        db_conf = yaml.safe_load(pkgutil.get_data(__name__, "config.yaml"))
        usr = db_conf['db']['username']
        pwd = db_conf['db']['pass']
        host = db_conf['db']['host']
        port = db_conf['db']['port']
        db_name = db_conf['db']['dbname']
        try:
            # Connect to the database
            self.__conn = psycopg2.connect(
                host=host,
                port=port,
                database=db_name,
                user=usr,
                password=pwd
            )
            print("Connected to database successfully")
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")

    def __close(self):
        if self.__conn:
            self.__conn.close()
            print("Database connection closed")

    def execute_query(self, query, params=None):
        if not self.__conn:
            self.__connect()

        try:
            with self.__conn.cursor() as cur:
                cur.execute(query, params)
                if query.lower().startswith('select'):
                    data = cur.fetchall()
                    cols = list(map(lambda x: x[0], cur.description))
                    df = pd.DataFrame(data, columns=cols)
                    return df
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.__conn.rollback()
        finally:
            if self.__conn:
                self.__conn.commit()

