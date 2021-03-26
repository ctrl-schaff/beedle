#!/usr/bin/env python3

"""
Definitions for the project structure 
|-- bin
|-- data
|   `-- config
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

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
CONFIG_DIR = os.path.join(DATA_DIR, "config")
