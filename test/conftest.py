#!/usr/bin/env python3

import functools
import itertools
import os
import pathlib
import time
from typing import (Any,
                    Callable,
                    Iterable)

import dotenv
import numpy as np
import pytest


@pytest.fixture()
def z2_map_data(romfile):
    '''
    Constructs the map data from the zelda 2 map
    > Sets the map dimensions based off the four main
      quadrants of the actual map area
    '''

    SUB_MAP_SIZE_X = 75
    SUB_MAP_SIZE_Y = 65
    MAP_SIZE_X = 2 * SUB_MAP_SIZE_X
    MAP_SIZE_Y = 2 * SUB_MAP_SIZE_Y

    map_boundary = {
        "WEST_HYRULE": (int("506C", 16), int("538C", 16)),
        "DEATH_MOUNTAIN": (int("665C", 16), int("6942", 16)),
        "EAST_HYRULE": (int("9056", 16), int("936F", 16)),
        "MAZE_ISLAND": (int("A65C", 16), int("A942", 16)),
    }

    map_data = np.zeros(
        [2 * SUB_MAP_SIZE_X, 2 * SUB_MAP_SIZE_Y], dtype=int
    )

    rompath = pathlib.Path(romfile).resolve()
    assert rompath.exists()
    
    sub_map_data = []
    with open(rompath, "rb+") as romdata:
        for mapbound in map_boundary.values():
            romdata.seek(mapbound[0])
            num_map_bytes = (mapbound[1] - mapbound[0]) + 1
            map_byte_chunk = romdata.read(num_map_bytes).hex()

            sub_map = []

            for byte in chunker(map_byte_chunk, 2, fillvalue='0'):
                sub_map += (int(byte[0], 16) + 1) * [int(byte[1], 16)]

            # Vertical water barrier to separate sub maps
            water_range = range(SUB_MAP_SIZE_Y, len(sub_map), SUB_MAP_SIZE_Y)
            for index in water_range:
                sub_map.insert(index - 1, 12)

            sub_map_data.append(
                np.resize(
                    np.array(sub_map),
                    (SUB_MAP_SIZE_X, SUB_MAP_SIZE_Y)
                )
            )

    # Cleanup the Death Mountain and Maze Island Segments
    sub_map_data[1][:, 28:] = 12
    sub_map_data[1][60:, :] = 12
    sub_map_data[3][:, :28] = 12
    sub_map_data[3][59:, :] = 12

    # Form total map
    map_data[:, :] = np.hstack(
        (
            np.vstack((sub_map_data[0], sub_map_data[1])),
            np.vstack((sub_map_data[2], sub_map_data[3])),
        )
    )

    # Transpose the map to ensure you can index with
    # (X, Y) rather than (Y, X)
    map_data = map_data.T
    (MAP_SIZE_X, MAP_SIZE_Y) = map_data.shape

    yield map_data


@pytest.fixture
def romfile():
    '''
    Fixture for loading the zelda 2 rom file
    provided in the pytest.ini [env] section
    '''
    dotenv.load_dotenv()
    yield os.getenv('ROM_PATH', default=None)


@pytest.fixture
def configuration():
    '''
    Fixture for loading the zelda 2 config file
    provided in the pytest.ini [env] section
    '''
    dotenv.load_dotenv()
    yield os.getenv('CONFIG_PATH', default=None)


def chunker(iterable: Iterable,
            length: int,
            fillvalue: Any = None) -> Iterable:
    '''
    Collect data into fixed-length chunks or blocks
    '''
    args = [iter(iterable)] * length
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def measure(func: Callable):
    @functools.wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time.time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time.time() * 1000)) - start
            print(f'Test | {func.__name__}')
            print(f'Total execution time: {end_ if end_ > 0 else 0} ms')
