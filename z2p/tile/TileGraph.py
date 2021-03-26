#!/usr/bin/env python3

"""
TileGraph:
Data structure for storing the converted RomMap data with Tile information
    - TileGraph stores a collection of TileData objects created through the TileParser
"""

import z2p.RomMap as RomMap

from z2p.tile.TileParser import TileParser


class TileGraph:
    def __init__(self, romMap: RomMap, keypath: str):
        self.tileMap = []
        self.tileParser = TileParser(keypath, romMap.mapData)
        self._formTileMap(romMap)

    def _formTileMap(self, romMap: RomMap):
        for ri in range(romMap.MAP_SIZE_X):
            tileRow = []
            for ci in range(romMap.MAP_SIZE_Y):
                thisTile = (ri, ci)
                tileID = romMap.mapData[thisTile]
                baseCost = self.tileParser.calcBaseTileCost(tileID)
                tileNode = self.tileParser.createTileNode(
                    thisTile, tileID, baseCost, romMap.mapData
                )
                tileRow.append(tileNode)
            self.tileMap.append(tileRow)

    def __getitem__(self, index: tuple):
        if isinstance(index, tuple):
            return self.tileMap[index[0]][index[1]]
        else:
            return super().__getitem__(index)
