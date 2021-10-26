#!/usr/bin/env python3


import z2p.map_data
import z2p.map_tile
import z2p.structure
import z2p.videoprocessor


def test_view_map():

    romfile = z2p.structure.config_file_str("zelda2.nes")
    tilespec = z2p.structure.config_file_str("zelda2tiles.conf")

    map_obj = z2p.map_data.RomMap(romfile)
    maptile = z2p.map_tile.MapTileData(tilespec)

    vz = z2p.videoprocessor.VideoProcessor(map_obj.map_data, maptile)
    vz.view_map_data()
