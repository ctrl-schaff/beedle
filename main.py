#!/usr/bin/env python3

import os
import sys

from z2p import RomMap, TileGraph, PathProcessor, VideoProcessor
import z2p

if __name__ == "__main__":

    dataDir = "./data/"
    dataDir = os.path.abspath(dataDir)
    if os.path.isdir(dataDir) and os.path.exists(dataDir):
        romfile = dataDir + "/zelda2.nes"
        keyfile = dataDir + "/key2.dat"
    else:
        exitstr = "Exiting: Unable to locate files\nROM {0:s}\nLOGIC {1:s}"
        sys.exit(exitstr.format(romfile, keyfile))

    md = RomMap(romfile)
    tg = TileGraph(md, keyfile)
    pg = PathProcessor((22, 23), tg)
    (regionSet, regionPaths) = pg.pathfind()

    vz = VideoProcessor(md.mapData, tg._tileParser.TILE_COLOR)
    vz.animateSearch(regionSet, regionPaths)
