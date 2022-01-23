#!/usr/bin/env python3

"""
RomMap:
Handles the importation of the rom map data
"""

import os
import sys

import numpy as np

import z2p.utility


class RomMap:

    SUB_MAP_SIZE_X = 75
    SUB_MAP_SIZE_Y = 65
    MAP_SIZE_X = 2 * SUB_MAP_SIZE_X
    MAP_SIZE_Y = 2 * SUB_MAP_SIZE_Y

    def __init__(self, rompath: str):

        self.map_boundary = {
            "WEST_HYRULE": (int("506C", 16), int("538C", 16)),
            "DEATH_MOUNTAIN": (int("665C", 16), int("6942", 16)),
            "EAST_HYRULE": (int("9056", 16), int("936F", 16)),
            "MAZE_ISLAND": (int("A65C", 16), int("A942", 16)),
        }

        self._sub_map_data = []
        self.map_data = np.zeros(
            [2 * self.SUB_MAP_SIZE_X, 2 * self.SUB_MAP_SIZE_Y], dtype=np.int
        )
        if os.path.isfile(rompath) and os.path.exists(rompath):
            self.romdata = os.path.abspath(rompath)
        else:
            sys.exit(f"Invalid rom file path {os.path.abspath(rompath)}")

        self._extract_map_data()
        self._form_map_data()

        # Transpose the map to ensure you can index with
        # (X, Y) rather than (Y, X)
        self.map_data = self.map_data.T
        (self.MAP_SIZE_X, self.MAP_SIZE_Y) = self.map_data.shape

    def _extract_map_data(self):
        with open(self.romdata, "rb+") as romfile:
            for mapbound in self.map_boundary.values():
                romfile.seek(mapbound[0])
                num_map_bytes = (mapbound[1] - mapbound[0]) + 1
                map_byte_chunk = romfile.read(num_map_bytes).hex()

                sub_map = []
                for byte in z2p.utility.chunker(
                        map_byte_chunk, 2, fillvalue="0"
                ):
                    sub_map += (int(byte[0], 16) + 1) * [int(byte[1], 16)]

                self._form_water_barrier(sub_map)

                self._sub_map_data.append(
                    np.resize(
                        np.array(sub_map),
                        (self.SUB_MAP_SIZE_X, self.SUB_MAP_SIZE_Y)
                    )
                )

    def _form_water_barrier(self, sub_map: list):
        """
        Vertical water barrier to separate sub maps
        """
        for index in range(self.SUB_MAP_SIZE_Y,
                           len(sub_map),
                           self.SUB_MAP_SIZE_Y
                           ):
            sub_map.insert(index - 1, 12)

    def _form_map_data(self):
        # Cleanup the Death Mountain and Maze Island Segments
        self._sub_map_data[1][:, 28:] = 12
        self._sub_map_data[1][60:, :] = 12
        self._sub_map_data[3][:, :28] = 12
        self._sub_map_data[3][59:, :] = 12

        # Form total map
        self.map_data[:, :] = np.hstack(
            (
                np.vstack((self._sub_map_data[0], self._sub_map_data[1])),
                np.vstack((self._sub_map_data[2], self._sub_map_data[3])),
            )
        )

    def __getitem__(self, map_coord: tuple):
        try:
            map_id = self.map_data[map_coord]
        except IndexError as ind_err:
            print(ind_err)
            print(f"Error indexing the map with coordinate {map_coord}")
            map_id = -1
        return map_id
