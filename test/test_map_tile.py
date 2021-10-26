#!/usr/bin/env python3

"""
Test methods for the map item data list
"""


import pytest

import z2p.map_tile
import z2p.structure


def zelda2_tile_truth():
    """
    Provides truth data for what the import data
    from the zelda2items.conf file should contain
    """
    tilelist = {
        "0": {
            "TYPE": "Town",
            "SYMBOL": "T",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#747474",
        },
        "1": {
            "TYPE": "Cave",
            "SYMBOL": "C",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#000000",
        },
        "2": {
            "TYPE": "Palace",
            "SYMBOL": "P",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#efefef",
        },
        "3": {
            "TYPE": "Bridge",
            "SYMBOL": "B",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#f0bc3c",
        },
        "4": {
            "TYPE": "Desert",
            "SYMBOL": "D",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#fabcb0",
        },
        "5": {
            "TYPE": "Grassland",
            "SYMBOL": "G",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#80D010",
        },
        "6": {
            "TYPE": "Forest",
            "SYMBOL": "F",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#009400",
        },
        "7": {
            "TYPE": "Swamp",
            "SYMBOL": "S",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#386138",
        },
        "8": {
            "TYPE": "Graveyard",
            "SYMBOL": "Y",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#fcfcfc",
        },
        "9": {
            "TYPE": "Road",
            "SYMBOL": "R",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#ffbc3c",
        },
        "10": {
            "TYPE": "Volcanic",
            "SYMBOL": "V",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#c84c0c",
        },
        "11": {
            "TYPE": "Mountain",
            "SYMBOL": "M",
            "BASE_COST": "|",
            "WALKABLE": False,
            "COLOR": "#634536",
        },
        "12": {
            "TYPE": "Ocean",
            "SYMBOL": "W",
            "BASE_COST": "|",
            "WALKABLE": False,
            "COLOR": "#3cbcfc",
        },
        "13": {
            "TYPE": "Water",
            "SYMBOL": "E",
            "BASE_COST": "Boots",
            "WALKABLE": True,
            "COLOR": "#85d5ff",
        },
        "14": {
            "TYPE": "Boulder",
            "SYMBOL": "O",
            "BASE_COST": "Hammer",
            "WALKABLE": True,
            "COLOR": "#dc7e4f",
        },
        "15": {
            "TYPE": "Monster",
            "SYMBOL": "A",
            "BASE_COST": "Flute",
            "WALKABLE": True,
            "COLOR": "#ff6def",
        },
        "16": {
            "TYPE": "Fill",
            "SYMBOL": "*",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#ccfdff",
        },
        "17": {
            "TYPE": "Path",
            "SYMBOL": "^",
            "BASE_COST": "|",
            "WALKABLE": True,
            "COLOR": "#f31616",
        },
    }

    return tilelist


def test_itemdata_import():
    """
    Test initial tile data import and compare against all values from
    the known truth values
    """
    tilespec = z2p.structure.config_file_str("zelda2tiles.conf")
    tiledata = z2p.map_tile.MapTileData(tilespec)
    tilelist_truth = zelda2_tile_truth()

    for tile_entry in tiledata.tile_lookup.keys():
        assert tile_entry in tilelist_truth.keys()
        assert tiledata.tile_lookup[tile_entry] == tilelist_truth[tile_entry]
        assert tiledata[tile_entry] == tilelist_truth[tile_entry]
