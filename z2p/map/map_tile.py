#!/usr/bin/env python3

"""
File import class for handling the map tile specifications
"""

import z2p.utility


class MapTileData:
    """
    MapTileData
    Wrapper class for importing the map tile specifications
    Handler for parsing and importing the map specific tile
    data for key locations and items
    """

    def __init__(self, tile_file: str):
        tile_data = z2p.utility.load_json_data(tile_file)
        mapkey = "maptiles"
        self.tile_lookup = tile_data[mapkey]

    def get_tile_property_collection(self, tile_property: str) -> tuple:
        """
        Get all values for a specific property for the entire tile collection
        """
        try:
            tile_property_collection = [
                tile_entry[tile_property]
                for tile_entry in self.tile_lookup.values()
            ]
        except Exception as excp:
            raise excp

        return tuple(tile_property_collection)

    def __getitem__(self, index: int):
        try:
            tile_entry = self.tile_lookup[str(index)]
            return tile_entry
        except KeyError as key_err:
            msg = (
                f'Error indexing  map tile lookup table with index {index}\n'
                f'Expected bounds [0, {len(self.tile_lookup)}]'
            )
            print(msg)
            raise key_err

    def __iter__(self):
        for entry in self.tile_lookup.values():
            yield entry
