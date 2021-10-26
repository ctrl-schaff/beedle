#!/usr/bin/env python3

"""
Test Methods for exploring the graph generation from map data
"""


import itertools
import pdb
import pytest

import z2p.graph
import z2p.map_item
import z2p.map_data
import z2p.map_logic
import z2p.map_tile
import z2p.pathprocessor
import z2p.structure


def test_graph_generation():
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

    graph_obj = z2p.graph.TileGraph(map_obj, logicdata, tiledata)


def test_graph_indexing():
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

    graph_obj = z2p.graph.TileGraph(map_obj, logicdata, tiledata)

    map_dim_product = (range(map_obj.MAP_SIZE_X), range(map_obj.MAP_SIZE_Y))
    for (row_index, col_index) in itertools.product(
        map_dim_product[0], map_dim_product[1]
    ):
        tile_coord = (row_index, col_index)
        tile_node = graph_obj[tile_coord]
        assert tile_coord == tile_node.location
