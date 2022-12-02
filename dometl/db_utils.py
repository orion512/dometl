"""
This file contains the module for databse utilities
"""

from dataclasses import dataclass, field

import psycopg2
import psycopg2.extras

from psycopg2._psycopg import connection, cursor


@dataclass
class DBCreds:
    """Class to hold Postgres credentials"""

    username: str
    password: str
    hostname: str
    port: str
    db_name: str


@dataclass
class DBHandler:
    """This class is a context manager wrapper for a postgres DB."""

    db_credentials: DBCreds
    conn: connection = field(init=False)
    cur: cursor = field(init=False)

    def __enter__(self):
        """This function gets invoked at the start of a with statement"""
        self.conn = psycopg2.connect(
            dbname=self.db_credentials.db_name,
            user=self.db_credentials.username,
            password=self.db_credentials.password,
            host=self.db_credentials.hostname,
        )
        self.conn.set_session(autocommit=True)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        return self.cur

    def __exit__(self, exc_type, ex_value, ex_traceback):
        """This function gets invoked at the end of the with statement"""
        self.cur.close()
        self.conn.close()
