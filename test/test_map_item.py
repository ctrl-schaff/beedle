#!/usr/bin/env python3

"""
Test methods for the map item data list
"""


import pytest

import z2p.map_item
import z2p.structure


def zelda2_item_truth():
    """
    Provides truth data for what the import data
    from the zelda2items.conf file should contain
    """
    itemlist = {
        "|": 0,
        "Heart1": 100,
        "Heart2": 100,
        "Heart3": 100,
        "Heart4": 100,
        "Magic1": 100,
        "Magic2": 100,
        "Magic3": 100,
        "Magic4": 100,
        "Shield": 10,
        "Jump": 1000,
        "Life": 100,
        "Fairy": 1000,
        "Fire": 10,
        "Reflect": 1000,
        "Spell": 1000,
        "Thunder": 1000,
        "Trophy": 1000,
        "BaguNote": 1000,
        "LifeWater": 1000,
        "LostChild": 1000,
        "MagicalKey": 1000,
        "Candle": 100,
        "Hammer": 1000,
        "Gloves": 1000,
        "Raft": 1000,
        "Boots": 1000,
        "Flute": 1000,
        "Cross": 1000,
        "Crystal1": 1000,
        "Crystal2": 1000,
        "Crystal3": 1000,
        "Crystal4": 1000,
        "Crystal5": 1000,
        "Crystal6": 1000,
    }
    return itemlist


def test_itemdata_import():
    """
    Test initial tile data import and compare against all values from
    the known truth values
    """
    itemspec = z2p.structure.config_file_str("zelda2items.conf")
    mapitem = z2p.map_item.MapItemData(itemspec)
    itemlist_truth = zelda2_item_truth()

    for item_name in mapitem.item_lookup.keys():
        assert item_name in itemlist_truth.keys()
        assert mapitem.item_lookup[item_name] == itemlist_truth[item_name]
        assert mapitem[item_name] == itemlist_truth[item_name]
