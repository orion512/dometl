"""
Entrypoint module for calling the package from the command line.

Author: Dominik Zulovec Sajovic - November 2022
"""

import sys
import os
import argparse
import logging
from typing import Callable

from dometl.settings import Settings, InLine
from dometl.config import DometlConfig
from dometl.etl_runner import ETLRunner


logger = logging.getLogger(__name__)


def run_dometl() -> None:
    """Entry point script which runs dometl"""

    logging.basicConfig(
        stream=sys.stdout,
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="""[%(asctime)s]\t%(levelname)s\t"""
        """%(name)s:%(lineno)d\t%(message)s""",
    )

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--type",
        help="""
        Specifcy type of scraping (
            init - initializes the database/tables/SPs,
            stage - loads files into a table (dir or file)
            live - staging to live SQL transformation
        )
        """,
        choices=["init", "stage", "live", "test"],
        type=str,
    )

    parser.add_argument(
        "-ep",
        "--extract_path",
        help="""
        path to the folder from where to extract the data.
        """,
        type=str,
    )

    parser.add_argument(
        "-tb",
        "--table",
        help="""
        Name of the database table into which to load the data.
        """,
        type=str,
    )

    parser.add_argument(
        "-cp",
        "--config_path",
        help="""
        Path to the dometl config folder.
        """,
        default="dometl_config",
        type=str,
    )

    parameters = parser.parse_args()

    main(parameters)


def main(args: argparse.Namespace) -> None:
    """Extension of the dometl entrypoint."""

    in_line = InLine(
        type=args.type,
        extract_path=args.extract_path,
        table=args.table,
        config_path=args.config_path,
    )

    settings = Settings(in_line=in_line)

    run_etl_manager(settings)


## ETL Functions


def run_etl_manager(settings: Settings) -> list:
    """This function runs the selected mode of etl"""

    logger.info("Started the etl manager")

    etl_modes: dict[str, Callable] = {
        "init": run_etl_init,
        "stage": run_etl_stage,
        "live": run_etl_live,
        "test": run_etl_test,
    }

    if settings.in_line.type not in etl_modes:
        raise ValueError(
            f"{settings.in_line.type} is not a valid value for the type ",
            "(-t) argument. "
            "Choose one of the following: init, cdc, full, live, livep",
        )

    return etl_modes[settings.in_line.type](settings)


def run_etl_init(settings: Settings):
    """This function orchestrates the initialization of the ETL"""

    logger.info("ETL INIT MODE")

    # 1. Read Init Config
    init_config = DometlConfig(settings.in_line.config_path)
    logger.info("Read the init config")

    # 2. Run the init order queries
    etl_runner = ETLRunner(init_config.db_credentials)
    queries = [init_config.sqls[name] for name in init_config.init_order]
    etl_runner.run_queries(queries)
    logger.info(f"Finished Initialization: ({len(init_config.init_order)})")


def run_etl_stage(settings: Settings):
    """This function runs the ETL staging step"""

    logger.info("ETL STAGE MODE")

    # 1. Read Init Config
    init_config = DometlConfig(settings.in_line.config_path)
    logger.info("Read the init config")

    # 2. Run the staging for the passed parameters
    etl_runner = ETLRunner(init_config.db_credentials)
    num_files = etl_runner.handle_staging(
        settings.in_line.extract_path, settings.in_line.table
    )
    logger.info(f"Finished staging of {num_files} files")


def run_etl_live(settings: Settings):
    """This function runs the ETL to transform ST to live with SQL"""

    logger.info("ETL LIVE MODE")

    # 1. Read Init Config
    init_config = DometlConfig(settings.in_line.config_path)
    logger.info("Read the init config")

    # 2. Run live transformations for the table requested
    etl_runner = ETLRunner(init_config.db_credentials)
    table_query = init_config.sqls[init_config.etl[settings.in_line.table]]
    rows = etl_runner.run_query(table_query)
    logger.info(
        f"Finished for table {settings.in_line.table} ({rows} rows affected)"
    )


def run_etl_test():
    """This function runs the tests for the ETL"""
    raise NotImplementedError
