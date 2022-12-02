"""
Settings skeleton for the project
"""


from dataclasses import dataclass


@dataclass
class InLine:
    """Class for storing command line passed arguments"""

    type: str
    extract_path: str
    table: str
    config_path: str


@dataclass
class Settings:
    """Class for storing project parameters"""

    in_line: InLine
