"""
This page contains the class which is used to read and parse the
etl configurations

Author: Dominik Zulovec Sajovic, November 2022
"""

import os
from dataclasses import dataclass
import yaml

from dometl.db_utils import DBCreds


@dataclass
class DometlConfig():
    """Class for reading and parsing the ETL configurations"""

    config_path: str
    db_credentials: DBCreds
    init_order: list[str]
    table_to_live: dict[str, tuple[str, str]]
    transformations: dict[str, str]

    def __post_init__(self):
        """
        This method runs right after init.
        It reads the sql files provided in the user config.
        Provided the structure and naming is correct.
        """

        config_yaml_path = os.path.join(self.config_path, "config.yaml")

        with open(config_yaml_path, 'r') as yaml_file:
            read_config = yaml.safe_load(yaml_file)
        
        # TODO: parse yaml to get db_creds, init_order, table_to live
        # TODO: loop through all non yaml files in config
        # TODO: read all into self.transformations dictionary dict[file_name] = contents
        
        init_files = self._files(self.sub_folder_name)

        self.db_create = self._file_contents(
            self.sub_folder_name, self.db_create, init_files)

        self.tables_st_create = self._file_contents(
            self.sub_folder_name, self.tables_st_create, init_files)
        
        self.tables_create = self._file_contents(
            self.sub_folder_name, self.tables_create, init_files)
        
        self.post_init = self._file_contents(
            self.sub_folder_name, self.post_init, init_files)

    def _files(self, sub_conf: str) -> list:
        """
        reads the config_path/sub_conf folder and returns all the files in it.
        """

        init_folder = os.path.join(self.config_path, sub_conf)
        return os.listdir(init_folder)

    def _file_contents(
        self, sub_folder: str, file: str, files: list[str]) -> str | None:
        """
        If file is present amongst the files it reads the contents
        else it returns None
        """
        return_val = None

        if f"{file}.sql" in files:
            path_to_file = os.path.join(
                self.config_path, sub_folder, f"{file}.sql")
            with open(path_to_file, "r") as file:
                return_val = file.read()
        
        return return_val

    def get_run_jobs(self):
        """ """

        job_order = [
            self.db_create, self.tables_st_create, 
            self.tables_create, self.post_init]
        
        for job in job_order:
            if job:
                yield job
