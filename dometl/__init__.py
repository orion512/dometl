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
from dometl.config import ConfigInit


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
            cdc - for change data capture (first file alphabetically),
            full - for a full load,
            live - staging to live SQL transformation,
            livep - staging to live python transformation (FUTURE)
        )
        """,
        choices=["init", "cdc", "full", "live", "livep"],
        type=str,
    )


    parser.add_argument(
        "-ep",
        "--extract_path",
        help="""
        path to the folder from where to extract the data.
        """,
        default="",
        type=str,
    )

    parser.add_argument(
        "-tb",
        "--table",
        help="""
        Name of the database table into which to load the data.
        """,
        required=True,
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
        config_path=args.config_path
    )

    settings = Settings(in_line=in_line)

    run_etl_manager(settings)


## ETL Functions

def run_etl_manager(settings: Settings) -> list:
    """This function runs the selected mode of etl"""

    logger.info("Started the etl manager")

    etl_modes: dict[str, Callable] = {
        "init": run_etl_init,
        "cdc": run_etl_cdc,
        "full": run_etl_full,
        "live": run_etl_live,
        "livep": run_etl_live_py,
    }

    if settings.in_line.type not in etl_modes:
        raise ValueError(
            f"{settings.in_line.type} is not a valid value for the type ",
            "(-t) argument. "
            "Choose one of the following: init, cdc, full, live, livep",
        )

    return etl_modes[settings.in_line.type](settings)


def run_etl_init(settings: Settings) -> list:
    """ This function orchestrates the initialization of the ETL """

    logger.info("ETL INIT MODE")

    # 1. Read Init Config
    init_config = ConfigInit(settings.in_line.config_path)
    logger.info(f"Read the init config")

    # 2. Get the game data for the list of games
    # TODO: run the queries
    logger.info(f"Initialized the database {'name'} and created {4} tables")


def run_etl_cdc():
    """This function runs the ETL with Change Data Capture"""
    raise NotImplementedError


def run_etl_full():
    """This function runs the ETL for the entire dataset load"""
    raise NotImplementedError


def run_etl_live():
    """This function runs the ETL to transform ST to live with SQL"""
    raise NotImplementedError


def run_etl_live_py():
    """This function runs the ETL to transform ST to live with python"""
    raise NotImplementedError
