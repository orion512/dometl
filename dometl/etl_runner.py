"""
This page contains the class which is used to run queries

Author: Dominik Zulovec Sajovic, November 2022
"""

import os
import logging
from dataclasses import dataclass

from dometl.db_utils import DBCreds, DBHandler
from dometl.exceptions import DataTestError

logger = logging.getLogger(__name__)

@dataclass
class ETLRunner:
    """Class for running quesries on the db"""

    db_credentials: DBCreds

    def run_queries(self, list_of_queries: list[str]):
        """Runs a list of queries in order"""

        for query in list_of_queries:
            self.run_query(query)

    def run_query(self, query: str) -> int:
        """Runs a single query"""

        with DBHandler(self.db_credentials) as cur:
            cur.execute(query)
            rows_affected = cur.rowcount

        return rows_affected

    def run_select_query(self, query: str) -> list:
        """Runs a single query and return the results"""

        with DBHandler(self.db_credentials) as cur:
            cur.execute(query)
            records = cur.fetchall()

        return records

    def handle_staging(self, path: str, table_name: str) -> int:
        """runs run_staging if path is a file or a dir"""
        self._delete_from(table_name)

        if os.path.isdir(path):
            for file in os.listdir(path):
                full_file_path = os.path.join(path, file)
                self.run_staging(full_file_path, table_name)
            return len(os.listdir(path))

        if os.path.isfile(path):
            self.run_staging(path, table_name)
            return 1

        raise ValueError("The path needs to be either a file or a dir")

    def run_staging(self, file_path: str, table_name: str):
        """Copies a CSV file into a SQL table"""

        with DBHandler(self.db_credentials) as cur:
            with open(file_path, "r", encoding="UTF-8") as read_file:
                next(read_file)  # ignores the first row (header)
                cur.copy_from(read_file, table_name, sep=",")

    def run_tests(self, test_queries: list[tuple]):
        """runs multiple test"""

        for query_name, query in test_queries:
            logger.info(f"Running test {query_name}")
            self.run_test(query)


    def run_test(self, query: str):
        """runs a single test query"""

        res = self.run_select_query(query)
        
        if len(res) > 0:
            raise DataTestError(res)
    

    def _delete_from(self, table_name: str):
        """deletes all rows from table name"""
        with DBHandler(self.db_credentials) as cur:
            cur.execute(f"DELETE FROM {table_name};")
