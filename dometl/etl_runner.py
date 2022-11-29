"""
This page contains the class which is used to run queries

Author: Dominik Zulovec Sajovic, November 2022
"""

import os
from dataclasses import dataclass, field
import yaml
import psycopg2

from dometl.db_utils import DBCreds, DBHandler


@dataclass
class ETLRunner():
    """Class for running quesries on the db"""

    db_credentials: DBCreds

    def run_queries(self, list_of_queries: list[str]):
        """ Runs a list of queries in order """
        
        for query in list_of_queries:
            self.run_query(query)

    def run_query(self, query: str):
        """ Runs a single query """

        with DBHandler(self.db_credentials) as cur:
            cur.execute(query)

    def handle_staging(self, path: str, table_name: str):
        """ runs run_staging if path is a file or a dir """
        if os.path.isdir(path):
            for file in os.listdir(path):
                full_file_path = os.path.join(path, file)
                self.run_staging(full_file_path, table_name)
        elif os.path.isfile(path):
            self.run_staging(path, table_name)


    def run_staging(self, file_path: str, table_name: str) -> int:
        """ Copies a CSV file into a SQL table """

        with DBHandler(self.db_credentials) as cur:
            with open(file_path, "r") as f:
                cur.copy_from(f, table_name, sep=',')


    def _collect_queries():
        """ """


