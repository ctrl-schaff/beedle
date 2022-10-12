#!/usr/bin/env python3

"""
Test examples using zelda 2 as the data source
for the beedle library
"""

import pprint
import random
import sys

from loguru import logger
import pytest

from beedle import TileGraph, LocationMap, TileMap, TileMapIndexError


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

    property_map = {
        "reward": location_map.location_reward_search,
        "reward_cost": location_map.location_reward_cost_search,
        "traversal_cost": location_map.location_traversal_cost_search,
    }

    for property_name, property_lookup in property_map.items():
        random_item_subset = set(random.sample([*item_bag], 3))

        item_locations = []
        for item in random_item_subset:
            item_lookup_result = property_lookup(item)
            if isinstance(item_lookup_result, list):
                item_locations.extend(item_lookup_result)
            else:
                item_locations.append(item_lookup_result)

        for location in item_locations:
            location_properties = location_map[location]
            found_reward = location_properties.get(property_name, None)
            assert found_reward.intersection(random_item_subset)

        logger.info(
            f"Successful {property_name} lookup {property_lookup.__func__}"
        )


def test_map_generation(z2_map_data, configuration):
    """
    Tests the ability to turn the map data and specified
    configuration into a TileMap data structure
    """
    location_data = configuration.get("locations", None)
    assert location_data

    tile_data = configuration.get("tiles", None)
    assert tile_data
    location_map = LocationMap(location_data)

    tile_map = TileMap(z2_map_data, location_map, tile_data)

    for location, properties in location_map.items():
        location_node = tile_map[location]
        assert location_node.location == location
        assert location_node.location == properties["entrance"]
        assert location_node.description == properties["description"]
        assert location_node.reward == properties["reward"]
        assert location_node.traversal_cost == properties["traversal_cost"]
        assert location_node.reward_cost == properties["reward_cost"]
        if properties["exit"] != properties["entrance"]:
            assert properties["exit"] in location_node.edges

        tile_properties = tile_data[str(location_node.identifier)]
        assert location_node.background == tile_properties["TYPE"]
        assert location_node.symbol == tile_properties["SYMBOL"]
        assert location_node.color == tile_properties["COLOR"]

    all_map_locations = set(tile_map.keys())
    subset_map_locations = set.difference(
        all_map_locations, location_map.entrance_locations
    )
    random_locations = random.sample([*subset_map_locations], 50)
    for location in random_locations:
        location_node = tile_map[location]
        assert location_node.location == location

        assert not location_node.description
        assert not location_node.reward
        assert not location_node.reward_cost

        tile_properties = tile_data[str(location_node.identifier)]
        if tile_properties["WALKABLE"]:
            assert location_node.traversal_cost == set(
                tile_properties["BASE_COST"]
            )
        else:
            assert location_node.traversal_cost == set(["unwalkable"])

        tile_properties = tile_data[str(location_node.identifier)]
        assert location_node.background == tile_properties["TYPE"]
        assert location_node.symbol == tile_properties["SYMBOL"]
        assert location_node.color == tile_properties["COLOR"]

    bounds_dim_x = random.randint(tile_map.map_size_x, sys.maxsize)
    bounds_dim_y = random.randint(tile_map.map_size_y, sys.maxsize)
    bounds_location = (bounds_dim_x, bounds_dim_y)

    with pytest.raises(TileMapIndexError):
        bound_node = tile_map[bounds_location]
        logger.info(bound_node)


def test_graph_generation(z2_map_data, configuration):
    """
    Attempts to generate the graph logic from the zelda 2 map
    """
    location_data = configuration.get("locations", None)
    assert location_data

    tile_data = configuration.get("tiles", None)
    assert tile_data

    location_map = LocationMap(location_data)
    tile_map = TileMap(z2_map_data, location_map, tile_data)

    graph_start = (23, 22)
    graph_end = (69, 43)

    graph_obj = TileGraph(graph_start, graph_end, tile_map, location_map)
    graph_obj.topological_sort(location_map)
