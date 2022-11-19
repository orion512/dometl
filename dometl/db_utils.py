from dataclasses import dataclass


@dataclass
class DBCreds:
    """ Class to hold Postgres credentials"""
    username: str
    password: str
    hostname: str
    port: str
    db_name: str


class TrinoConnectionHandler:
    """Trino Connection Handler as a context manager"""

    def __init__(self, conn_details: TrinoConnDetails):
        self.conn_details = conn_details
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = trino.dbapi.connect(
            host=self.conn_details.hostname,
            port=self.conn_details.port,
            user=self.conn_details.username,
            catalog=self.conn_details.catalog,
            schema=self.conn_details.schema,
            http_scheme="https",
            auth=trino.auth.BasicAuthentication(
                self.conn_details.username, self.conn_details.password
            ),
        )

        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()