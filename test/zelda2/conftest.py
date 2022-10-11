#!/usr/bin/env python3

import itertools
import json
import os
import pathlib
import shutil
from typing import Any, Iterable

import dotenv
import numpy as np
import pytest


@pytest.fixture()
def z2_map_data(romfile) -> np.array:
    """
    Constructs the map data from the zelda 2 map
    > Sets the map dimensions based off the four main
      quadrants of the actual map area
    """

    half_map_size_x_dimension = 75
    half_map_size_y_dimension = 65

    map_boundary = {
        "WEST_HYRULE": (int("506C", 16), int("538C", 16)),
        "DEATH_MOUNTAIN": (int("665C", 16), int("6942", 16)),
        "EAST_HYRULE": (int("9056", 16), int("936F", 16)),
        "MAZE_ISLAND": (int("A65C", 16), int("A942", 16)),
    }

    map_data = np.zeros(
        [2 * half_map_size_x_dimension, 2 * half_map_size_y_dimension],
        dtype=int,
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

            for byte in chunker(map_byte_chunk, 2, fillvalue="0"):
                sub_map += (int(byte[0], 16) + 1) * [int(byte[1], 16)]

            # Vertical water barrier to separate sub maps
            water_range = range(
                half_map_size_y_dimension,
                len(sub_map),
                half_map_size_y_dimension,
            )
            for index in water_range:
                sub_map.insert(index - 1, 12)

            sub_map_data.append(
                np.resize(
                    np.array(sub_map),
                    (half_map_size_x_dimension, half_map_size_y_dimension),
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
    yield map_data


@pytest.fixture
def romfile() -> pathlib.Path:
    """
    Fixture for loading the zelda 2 rom file
    provided in the pytest.ini [env] section
    """
    env_variable_name = "ROM_PATH"
    yield load_environment_variable(env_variable_name)


@pytest.fixture
def configuration(build_test_structure) -> dict:
    """
    Fixture for loading the zelda 2 config file
    provided in the pytest.ini [env] section
    """
    config_name = "zelda2.json"
    config_path = (build_test_structure / config_name).resolve().absolute()
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as config_handle:
            config_data = json.load(config_handle)
        yield config_data
    else:
        raise FileNotFoundError(f"Unable to load {config_path}")


@pytest.fixture(scope="module")
def build_test_structure(tmp_path_factory, request):
    """
    Builds a module level test structure to avoid potentially modifying
    repository test data

    > searches for a folder with the same name as the test module
    > if available, moves all contests to a temporary directory
    > yields this test directory with newly copied data
    > upon completion of the module level tests, removes this test directory
    """
    module_name = request.node.name
    module_path = pathlib.Path(module_name).resolve().absolute()
    data_directory = module_path.with_name(module_path.stem)

    temp_directory_name = "merchant"
    temp_directory = tmp_path_factory.mktemp(temp_directory_name)
    if data_directory.is_dir():
        shutil.copytree(
            src=str(data_directory),
            dst=str(temp_directory),
            dirs_exist_ok=True,
        )
    yield temp_directory
    shutil.rmtree(str(temp_directory.parent))


def load_environment_variable(env_variable_name: str) -> pathlib.Path:
    """
    General method for loading an environment variable into the
    pytest environment for usage within tests. Requires the
    environment variable name as input and returns a pathlib.Path
    object if resolvable and exists on the local file system

    Raises a FileNotFoundError if unable to find the path provided
    by the environement variable
    """
    dotenv.load_dotenv()
    path_env = os.getenv(env_variable_name, default=None)
    resolve_path = pathlib.Path(path_env).resolve()
    if resolve_path.exists():
        return resolve_path

    path_err_msg = (
        "Unable to resolve environment variable path: "
        f"{str(path_env)}\n"
        f"Check pytest.ini for {env_variable_name}"
    )
    raise FileNotFoundError(path_err_msg)


def chunker(
    iterable: Iterable, length: int, fillvalue: Any = None
) -> Iterable:
    """
    Collect data into fixed-length chunks or blocks
    """
    args = [iter(iterable)] * length
    return itertools.zip_longest(*args, fillvalue=fillvalue)
