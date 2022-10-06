#!/usr/bin/env python3

"""
Test examples using zelda 2 as the data source
for the z2p library
"""

import pprint
import random

from loguru import logger

from z2p import TileGraph, LocationMap


def test_location_map(configuration):
    """
    Test the ability to translate the configuration
    field <locations> parsed as a json structure into
    a LocationMap data structure
    """
    location_data = configuration.get("locations", None)
    assert location_data
    location_map = LocationMap(location_data)

    for location, properties in location_map.items():
        assert isinstance(location, tuple)
        assert isinstance(properties, dict)
        item_msg = (
            f"Location:{location}\n"
            f"Properties:{pprint.pformat(properties, sort_dicts=True)}"
        )
        logger.debug(item_msg)

    assert isinstance(location_map.entrance_locations, set)
    assert len(location_map.entrance_locations) > 0
    for entrance in random.sample([*location_map.entrance_locations], k=3):
        assert isinstance(entrance, tuple)

    item_bag = set()
    for entrance in location_map.entrance_locations:
        entrance_properties = location_map[entrance]
        assert isinstance(entrance_properties, dict)
        item_bag.update(entrance_properties["reward"])
        item_bag.update(entrance_properties["reward_cost"])
        item_bag.update(entrance_properties["traversal_cost"])

    random_item_subset = set(random.sample([*item_bag], 3))
    item_locations = location_map.location_item_search(random_item_subset)
    for location in item_locations:
        location_properties = location_map[location]
        found_reward = location_properties["reward"]
        assert found_reward.intersection(random_item_subset)


def test_map_generation(configuration):
    """
    Tests the ability to turn the map data and specified
    configuration into a TileMap data structure
    """
    assert False


def test_graph_generation(z2_map_data, configuration):
    """
    Attempts to generate the graph logic from the zelda 2 map
    """
    location_data = configuration.get("locations", None)
    location_map = LocationMap(location_data)

    graph_start = (23, 22)
    graph_end = (69, 43)

    graph_obj = TileGraph(graph_start, graph_end, z2_map_data, location_map)

    item_data = configuration.get("items", None)
    tile_data = configuration.get("tiles", None)
