#!/usr/bin/env python3

"""
"""


import itertools
import pytest

import z2p.graph
import z2p.map_item
import z2p.map_data
import z2p.map_logic
import z2p.map_tile
import z2p.pathprocessor
import z2p.structure


def test_node_generation():
    """
    Perform region finding and produce all potential paths up to first palace
    """

    romfile = z2p.structure.config_file_str("zelda2.nes")
    tilespec = z2p.structure.config_file_str("zelda2tiles.conf")
    logicspec = z2p.structure.config_file_str("zelda2logic.conf")
    itemspec = z2p.structure.config_file_str("zelda2items.conf")

    map_obj = z2p.map_data.RomMap(romfile)

    tiledata = z2p.map_tile.MapTileData(tilespec)
    logicdata = z2p.map_logic.MapLogicData(logicspec, tiledata)

    tile_graph = dict()
    map_dim_x = range(map_obj.MAP_SIZE_X)
    map_dim_y = range(map_obj.MAP_SIZE_Y)
    for (row_index, col_index) in itertools.product(map_dim_x, map_dim_y):
        tile_coord = (row_index, col_index)
        tile_id = map_obj.map_data[tile_coord]
        tile_node = z2p.node.create_node(
            tile_coord, tile_id, map_obj, logicdata, tiledata
        )
        tile_graph[tile_coord] = tile_node
