"""
Collection of test fixtures

group fixtures
> caplog
> temporary_data_storage

zelda2 fixtures
> zelda2_map
> zelda2_configuration
"""
# pylint: disable=W0621 (redefined-outer-scope)

import json
import pathlib
import shutil

from loguru import logger
import numpy as np
import pytest

from _pytest.logging import LogCaptureFixture


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    handler_id = logger.add(caplog.handler, format="{message}")
    yield caplog
    logger.remove(handler_id)


@pytest.fixture(scope="session")
def zelda2_map(temporary_data_storage) -> np.array:
    """
    Loads the zelda2 map data
    """
    map_name = "zelda2map.dat"
    map_path = (temporary_data_storage / map_name).resolve().absolute()
    with open(str(map_path), "r", encoding="utf-8") as map_handle:
        map_data = np.array(
            [[int(entry) for entry in row.split()] for row in map_handle]
        )
        return map_data


@pytest.fixture(scope="session")
def zelda2_configuration(temporary_data_storage) -> dict:
    """
    Fixture for loading the zelda 2 config file
    provided in the pytest.ini [env] section
    """
    config_name = "zelda2.json"
    config_path = (temporary_data_storage / config_name).resolve().absolute()
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as config_handle:
            config_data = json.load(config_handle)
        return config_data
    else:
        raise FileNotFoundError(f"Unable to load {config_path}")


@pytest.fixture(scope="session")
def temporary_data_storage(tmp_path_factory, request):
    """
    Builds a session level test structure to avoid potentially modifying
    repository test data

    > Takes the session level items discovered as tests and iterates over
      them
    > Each test item will have the following:
        > test_location
        > test_node
        > test_name
    > We search for a potential hardcoded data directory relative to the
      discovered test to add to our collection of test data directories
    > Takes these discovered directories and copies all the corresponding
      test data into a temporary location for usage during the tests
    > Fixture yields the temporary directory structure to each test that
      calls it so the test can utilize any potential data it requires
      without modifying the stored test data within the repository
    > Cleans up the temporary directory after the test session has completed
    """
    test_data_directory_name = "testdata"
    module_root_path = request.config.rootpath

    test_data_locations = set()
    for test_function in request.session.items:
        test_location, test_node, test_name = test_function.location
        logger.info(
            f"Discovered {test_name}@{test_location} given node #{test_node}"
        )

        test_location_path = pathlib.Path(test_location)
        test_data_path = (
            module_root_path
            / test_location_path.parent
            / test_data_directory_name
        )
        test_data_locations.add(test_data_path)

    temp_directory_name = "merchant"
    temp_directory = tmp_path_factory.mktemp(temp_directory_name)
    for data_directory in test_data_locations:
        if data_directory.is_dir():
            shutil.copytree(
                src=str(data_directory),
                dst=str(temp_directory),
                dirs_exist_ok=True,
            )
            logger.info(f"Copied {data_directory} -> {temp_directory}")

    yield temp_directory
    shutil.rmtree(str(temp_directory))
