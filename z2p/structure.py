#!/usr/bin/env python3

"""
Definitions for the project structure
|-- bin
|-- data
|-- config
|-- dev
|-- include
|-- lib
|-- lib64 -> lib
|-- req
|-- share
|-- tests
`-- z2p
    `-- tile
"""

import pathlib

Z2P_DIR = pathlib.Path(__file__)
ROOT_DIR = Z2P_DIR.parents[1]
CONFIG_DIR = ROOT_DIR.joinpath("config")


def config_file_str(filepath: str) -> str:
    """Generate string for configuration file path"""
    return str(CONFIG_DIR.joinpath(filepath))


def root_file_str(filepath: str) -> str:
    """Generate string for root project file path"""
    return str(ROOT_DIR.joinpath(filepath))


def z2p_file_str(filepath: str) -> str:
    """Generate string for module file path"""
    return str(Z2P_DIR.joinpath(filepath))
