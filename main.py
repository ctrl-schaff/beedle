#!/usr/bin/env python3

"""
Driver script for z2p processing
"""

import argparse
import os

from structure import DATA_DIR
from structure import CONFIG_DIR

import z2p.RomMap as RomMap
import z2p.PathProcessor as PathProcessor
import z2p.VideoProcessor as VideoProcessor
from z2p.tile.TileGraph import TileGraph

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--romfile", dest="romfile", type=str, required=True)
    ap.add_argument("-l", "--logicfile", dest="logicfile", type=str, required=True)

    ap.add_argument(
        "-v",
        "--videoBase",
        dest="videoBase",
        type=str,
        required=False,
        default="pathExplore",
    )

    args = ap.parse_args()

    romfile = os.path.join(DATA_DIR, args.romfile)
    logicfile = os.path.join(DATA_DIR, args.logicfile)

    md = RomMap(romfile)
    tg = TileGraph(md, logicfile)
    pg = PathProcessor(tg)

    initStartTile = (22, 23)
    pg.pathfind(initStartTile)

    vz = VideoProcessor(md.mapData, tg.tileParser.tileData.TILE_COLOR)
    vz = VideoProcessor(md.mapData, tg.tileParser.tileData.TILE_COLOR, 10)

    for ind, (regionSet, regionTilePaths) in enumerate(zip(pg.regionData, pg.pathData)):
        videoName = "{0:s}{1:d}.mp4".format(args.videoBase, ind)
        vz.animateSearch(regionSet, regionTilePaths, videoName)
