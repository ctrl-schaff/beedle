#!/usr/bin/env python3

"""
Miscellaneous utilities
"""

import collections
import json
import itertools
import os

import matplotlib.pyplot as plt

import z2p.tilepath

TilePath = z2p.tilepath.TilePath


def check_file_path(filepath: str):
    """
    Basic function intended as decorator for checking file paths
    """
    file_exist = filepath is not None
    path_exist = os.path.exists(filepath)
    file_check = os.path.isfile(filepath)
    if file_exist and path_exist and file_check:
        filepath = os.path.abspath(filepath)
    else:
        print("Unable to find file {0:s}".format(filepath))
        filepath = None
    return filepath


def check_dir_path(filepath: str):
    """
    Basic function intended as decorator for checking directory paths
    """
    file_exist = filepath is not None
    path_exist = os.path.exists(filepath)
    dir_check = os.path.isdir(filepath)

    if file_exist and path_exist and dir_check:
        filepath = os.path.abspath(filepath)
    else:
        print("Unable to find directory {0:s}".format(filepath))
        filepath = None
    return filepath


def load_json_data(json_file: str) -> dict:
    """
    Basic file reading method for reading and loading a json file
    """
    json_file_path = check_file_path(json_file)

    with open(json_file_path, "r") as jfp:
        json_data = json.load(jfp)
    return json_data


def unpack_json_data(json_data: dict) -> dict:
    """
    Uses a ChainMap to extract && combine all of the json data separated
    in the data file into one dictionary for lookup purposes
    """
    flat_json_data = dict(collections.ChainMap(*json_data.values()))
    return flat_json_data
