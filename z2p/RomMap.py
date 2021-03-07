#!/usr/bin/env python3

"""
RomMap:
Handles the importation of the rom map data  
"""

import os
import sys

import numpy as np

import z2p.utility as util


class RomMap:
    def __init__(self, rompath: str):

        self.SUB_MAP_SIZE_X = 75
        self.SUB_MAP_SIZE_Y = 65
        self.MAP_SIZE_X = 2 * self.SUB_MAP_SIZE_X
        self.MAP_SIZE_Y = 2 * self.SUB_MAP_SIZE_Y
        self.MAP_BOUNDARY = {
            "WEST_HYRULE": (int("506C", 16), int("538C", 16)),
            "DEATH_MOUNTAIN": (int("665C", 16), int("6942", 16)),
            "EAST_HYRULE": (int("9056", 16), int("936F", 16)),
            "MAZE_ISLAND": (int("A65C", 16), int("A942", 16)),
        }

        self._subMapData = []
        self.mapData = np.zeros(
            [2 * self.SUB_MAP_SIZE_X, 2 * self.SUB_MAP_SIZE_Y], dtype=np.int
        )
        self.tileMap = []

        if os.path.isfile(rompath) and os.path.exists(rompath):
            self.romdata = os.path.abspath(rompath)
        else:
            sys.exit("Invalid rom file path{0:s}".format(os.path.abspath(rompath)))

        self._extractMapData()
        self._formMapData()

    def _extractMapData(self):
        with open(self.romdata, "rb+") as romfile:
            for mapbound in self.MAP_BOUNDARY.values():
                romfile.seek(mapbound[0])
                numMapBytes = (mapbound[1] - mapbound[0]) + 1
                mapByteChunk = romfile.read(numMapBytes).hex()

                subMap = []
                self._formSubMapData(subMap, mapByteChunk)
                self._formWaterBarrier(subMap)

                self._subMapData.append(
                    np.resize(
                        np.array(subMap), (self.SUB_MAP_SIZE_X, self.SUB_MAP_SIZE_Y)
                    )
                )

    def _formSubMapData(self, subMap: list, mapByteChunk: str):
        for byte in util.chunker(mapByteChunk, 2, fillvalue="0"):
            subMap += (int(byte[0], 16) + 1) * [int(byte[1], 16)]

    # Vertical water barrier to separate sub maps
    def _formWaterBarrier(self, subMap: list):
        for index in range(self.SUB_MAP_SIZE_Y, len(subMap), self.SUB_MAP_SIZE_Y):
            subMap.insert(index - 1, 12)

    def _formMapData(self):

        # Cleanup the Death Mountain and Maze Island Segments
        self._subMapData[1][:, 28:] = 12
        self._subMapData[1][60:, :] = 12
        self._subMapData[3][:, :28] = 12
        self._subMapData[3][59:, :] = 12

        # Form total map
        self.mapData[:, :] = np.hstack(
            (
                np.vstack((self._subMapData[0], self._subMapData[1])),
                np.vstack((self._subMapData[2], self._subMapData[3])),
            )
        )
