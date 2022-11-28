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
        pass

    def run_staging_query(self, path_extract: str, table_name: str) -> int:
        """
        ......
        """

        with DBHandler(self.db_credentials) as cur:

            path_to_csv = 'C:\\Users\\Dominik\\Documents\\Projects\\dometl\\datasets\\game_data\\daily\\20221105_g.csv'
            with open(path_to_csv, "r") as f:
                cur.copy_from(f, "st_game", sep=',')

            cur.execute("SELECT COUNT(id) FROM nba.game")
            res = cur.fetchall()

    def _collect_queries():
        """ """


