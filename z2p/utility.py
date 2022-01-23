#!/usr/bin/env python3

"""
Miscellaneous utilities
"""

import collections
import json
import itertools
import operator
import os

import numpy as np
import matplotlib.pyplot as plt

import z2p.tilepath

TilePath = z2p.tilepath.TilePath


def get_neighbors(node: tuple) -> list:
    """
    Calculates all neighbors in cardinal directions on a
    coordinate plane (left, right, up, down)
    (X, Y) - Coordinate Pair

    (X, Y) + (1, 0) -> (X+1, Y)
    (X, Y) + (0, 1) -> (X, Y+1)
    (X, Y) + (-1, 0) -> (X-1, Y)
    (X, Y) + (0, -1) -> (X, Y-1)

    Output: ((X+1, Y), (X, Y+1), (X-1, Y), (X, Y-1))
    """
    return [
        tuple(map(operator.add, node, move))
        for move in ((1, 0), (-1, 0), (0, 1), (0, -1))
    ]


def manhattan_distance(node1: tuple, node2: tuple) -> tuple:
    """
    Calculates the manhattan distance
    (X1, Y1) - Coordinate Pair 1
    (X2, Y2) - Coordinate Pair 2
    manhattan_distance = |(X1 - X2)| + |(Y1 - Y2)|
    """
    return np.abs(node1[0] - node2[0]) + np.abs(node1[1] - node2[1])


def chunker(iterable, chunk_size: int, fillvalue=None):
    """ Collect data into fixed-length chunks or blocks """
    args = [iter(iterable)] * chunk_size
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def view_tile_path(tpath: TilePath, keyset: set):
    """ Basic method for visualizing the tile path in matplotlib """
    plt.figure()
    (ykey, xkey) = zip(*keyset)
    (ypath, xpath) = zip(*tpath.collection)
    plt.scatter(xkey, ykey)
    plt.scatter(xpath, ypath)
    plt.gca().invert_yaxis()
    plt.show()


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
