#!/usr/bin/env python3

"""
Test methods for the map tile logic
    > Logic in this case indicates anything associated with a map 
    that would not be immediately obvious from looking at a static 
    image of the map
    > This includes things like cave / transportation points, traversal 
    requirements, item data, etc ...
"""

import pytest

import z2p.structure
import z2p.map_logic
import z2p.map_tile


def test_tilelogic_import():
    """
    Test initial tile data import and compare against all values from
    the known truth values
    """
    logicspec = z2p.structure.config_file_str("zelda2logic.conf")
    tilespec = z2p.structure.config_file_str("zelda2tiles.conf")

    tile_data = z2p.map_tile.MapTileData(tilespec)
    maplogic_collection = z2p.map_logic.MapLogicData(logicspec, tile_data)
