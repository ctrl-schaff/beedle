#!/usr/bin/env python3

"""
Test Methods for exploring path generation for the zelda 2 map
"""


import pytest

import z2p.graph
import z2p.map_item
import z2p.map_data
import z2p.map_logic
import z2p.map_tile
import z2p.pathprocessor
import z2p.structure
import z2p.videoprocessor


def test_path_init():
    """
    Perform region finding and produce all potential paths up to first palace
    Ignores the pathfind method to explore the internal methods to the pathprocessor
    """

    romfile = z2p.structure.config_file_str("zelda2.nes")
    tilespec = z2p.structure.config_file_str("zelda2tiles.conf")
    logicspec = z2p.structure.config_file_str("zelda2logic.conf")
    itemspec = z2p.structure.config_file_str("zelda2items.conf")

    itemdata = z2p.map_item.MapItemData(itemspec)
    tiledata = z2p.map_tile.MapTileData(tilespec)
    logicdata = z2p.map_logic.MapLogicData(logicspec, tiledata)

    map_obj = z2p.map_data.RomMap(romfile)
    graph_obj = z2p.graph.TileGraph(map_obj, logicdata, tiledata)
    path_proc = z2p.pathprocessor.PathProcessor(graph_obj, logicdata, itemdata)

    start_tile = (22, 23)

    (region_keys, tile_paths, new_start_tile) = path_proc._initialize_search_space(
        start_tile,
    )
    breakpoint()

    expected_region_keys = (
        (23, 22),
        (16, 30),
        (2, 6),
        (29, 2),
        (46, 24),
        (55, 16),
        (48, 11),
        (62, 2),
        (62, 34),
    )

    assert set(region_keys) == set(expected_region_keys)
    assert len(tile_paths) == 9
    assert new_start_tile == (62, 2)

    path_proc.search_region_space(tile_paths, region_keys)
    breakpoint()
