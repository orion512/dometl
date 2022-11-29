"""
This page contains the class which is used to read and parse the
etl configurations

Author: Dominik Zulovec Sajovic, November 2022
"""

import os
from dataclasses import dataclass, field
import yaml

from dometl.db_utils import DBCreds


@dataclass
class DometlConfig():
    """Class for reading and parsing the ETL configurations"""

    config_path: str
    db_credentials: DBCreds = field(init=False) 
    init_order: list[str] = field(init=False) 
    etl: dict[str, str] = field(init=False) 
    sqls: dict[str, str] = field(init=False) 

    def __post_init__(self):
        """
        This method runs right after init.
        It reads the sql files provided in the user config.
        Provided the structure and naming is correct.
        """

        config_yaml_path = os.path.join(self.config_path, "config.yaml")

        with open(config_yaml_path, 'r') as yaml_file:
            read_config = yaml.safe_load(yaml_file)
        
        db_creds = read_config["db_credentials"]
        self.db_credentials = DBCreds(**db_creds)

        self.init_order = read_config["init_order"]
        self.etl = read_config["etl"]

        self.sqls = {}
        for sql_file in filter(self._is_sql, self._files()):
            self.sqls[sql_file] = self._file_contents(sql_file)

    def _files(self) -> list:
        """
        reads the config_path/sub_conf folder and returns all the files in it.
        """
        return os.listdir(self.config_path)

    def _is_sql(self, some_str: str) -> list:
        """
        returns true if the file has .sql extension
        """
        if some_str.endswith(".sql"):
            return True
        return False

    def _file_contents(self, file: str) -> str:
        """
        If file is present amongst the files it reads the contents
        else it returns None
        """
        path_to_file = os.path.join(self.config_path, file)

        with open(path_to_file, "r") as file:
            return_val = file.read()
        
        return return_val
