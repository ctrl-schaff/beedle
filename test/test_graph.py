#!/usr/bin/env python3

"""
Test Methods for exploring the graph generation from map data
"""

import functools
import time
import pytest

import z2p.graph
import z2p.map_item
import z2p.map_data
import z2p.map_logic
import z2p.map_tile
import z2p.pathprocessor
import z2p.structure


def measure(func):
    @functools.wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time.time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time.time() * 1000)) - start
            print(f'Test | {func.__name__}')
            print(f'Total execution time: {end_ if end_ > 0 else 0} ms')


def test_process_graph():
    """
    Graph processing algorithm
    """

    romfile = z2p.structure.config_file_str("zelda2.nes")
    tilespec = z2p.structure.config_file_str("zelda2tiles.conf")
    logicspec = z2p.structure.config_file_str("zelda2logic.conf")
    itemspec = z2p.structure.config_file_str("zelda2items.conf")

    map_obj = z2p.map_data.RomMap(romfile)

    tiledata = z2p.map_tile.MapTileData(tilespec)
    logicdata = z2p.map_logic.MapLogicData(logicspec, tiledata, map_obj)
    itemdata = z2p.map_item.MapItemData(itemspec)

    graph_obj = z2p.graph.TileGraph(map_obj, logicdata, tiledata)
    graph_start = (23, 22)
    graph_end = (69, 43)
    path_proc = graph_obj.process_graph(graph_start,
                                        graph_end,
                                        logicdata,
                                        itemdata)

    # breakpoint()
    # vz = z2p.videoprocessor.VideoProcessor(
    #     map_obj.mapData, tilespec.tileParser.tileData.TILE_COLOR
    # )
    # vz = z2p.videoprocessor.VideoProcessor(map_obj.mapData,
    #                                        tilespec,
    #                                        10)

    # for ind, (region_set, region_tile_paths) in enumerate(
    #     zip(path_proc.regionData, path_proc.pathData)
    # ):
    #     VIDEONAME = "{0:s}{1:d}.mp4".format('z2p_path', ind)
    #     vz.animateSearch(region_set, region_tile_paths, VIDEONAME)
