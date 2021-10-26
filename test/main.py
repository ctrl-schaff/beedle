#!/usr/bin/env python3

"""
Driver script for z2p processing
"""


import argparse

import z2p.graph
import z2p.itemdata
import z2p.map_data
import z2p.maplogic
import z2p.maptile
import z2p.pathprocessor
import z2p.structure

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--romfile", dest="romfile", type=str, required=True)
    ap.add_argument("-l", "--logicfile", dest="logicfile", type=str, required=True)
    ap.add_argument("-t", "--tilefile", dest="tilefile", type=str, required=True)
    ap.add_argument("-i", "--itemfile", dest="itemfile", type=str, required=True)

    ap.add_argument(
        "-v",
        "--videoBase",
        dest="videoBase",
        type=str,
        required=False,
        default="pathExplore",
    )

    args = ap.parse_args()

    romfile = z2p.structure.config_file_str("zelda2.nes")
    tilespec = z2p.structure.config_file_str("zelda2tiles.conf")
    logicspec = z2p.structure.config_file_str("zelda2logic.conf")
    itemspec = z2p.structure.config_file_str("zelda2items.conf")

    itemdata = z2p.itemdata.ItemData(itemspec)
    logicdata = z2p.maplogic.LogicData(logicspec)
    tiledata = z2p.maptile.MapTileData(tilespec)

    map_obj = z2p.map_data.RomMap(romfile)
    graph_obj = z2p.graph.TileGraph(map_obj, logicdata, tiledata)
    path_proc = z2p.pathprocessor.PathProcessor(graph_obj)

    init_start_tile = (22, 23)
    path_proc.pathfind(init_start_tile)

    vz = z2p.videoprocessor.VideoProcessor(
        md.mapData, tg.tileParser.tileData.TILE_COLOR
    )
    vz = z2p.videoprocessor.VideoProcessor(
        md.mapData, tg.tileParser.tileData.TILE_COLOR, 10
    )

    for ind, (region_set, region_tile_paths) in enumerate(
        zip(pg.regionData, pg.pathData)
    ):
        VIDEONAME = "{0:s}{1:d}.mp4".format(args.videoBase, ind)
        vz.animateSearch(region_set, region_tile_paths, VIDEONAME)
