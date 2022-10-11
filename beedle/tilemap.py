"""
TileMap:
Converting the raw map data into a dictionary of connected nodes
storing the converted map data with tile information
    - TileMap stores a collection of Node objects
Maps (xcoord, ycoord) -> TileNode
"""

from collections import UserDict
import itertools
from typing import Any, Tuple

from loguru import logger
import numpy as np

from .exceptions import TileMapIndexError
from .tilelocations import LocationMap
from .tilenode import TileNode


class TileMap(UserDict):
    """
    Dictionary representing the 2D tile map
    key -> Tuple[int, int] representing tile coordinate
    value -> TileNode object with properties and information
             specific to the tile based off the configuration
    """

    def __init__(
        self, map_data: np.array, location_map: LocationMap, tile_table: dict
    ):
        map_dim = map_data.shape
        self.map_size_x = map_dim[0]
        self.map_size_y = map_dim[1]

        _tile_map = self._form_tile_map(map_data, location_map, tile_table)
        super().__init__(_tile_map)

    def __str__(self) -> str:
        map_data_repr = f"[{self.map_size_x, self.map_size_y}]"
        tilemap_str = f"TileMap Instance {map_data_repr} {id(self)}\n"
        return tilemap_str

    def _form_tile_map(
        self, map_data: np.array, location_map: LocationMap, tile_table
    ) -> dict:
        """
        Iterates over the coordinates of the map based off dimensions and
        creates a graph with the associated map logic for
        transforming (X, Y) -> TileNode()
        """
        tile_map = {}
        map_axis_x = range(self.map_size_x)
        map_axis_y = range(self.map_size_y)
        map_traversal = itertools.product(map_axis_x, map_axis_y)
        for (row_index, col_index) in map_traversal:
            tile_coord = (row_index, col_index)
            tile_value = map_data[tile_coord]
            location_properties = location_map[tile_coord]
            tile_properties = tile_table[str(tile_value)]

            tile_node = TileNode(
                tile_coord,
                tile_value,
                map_data.shape,
                location_properties,
                tile_properties,
            )

            tile_map[tile_coord] = tile_node
            logger.debug(f"Added new TileNode@{self}+{tile_node}")
        return tile_map

    def __missing__(self, key: Any):
        """
        Any missing key values should raise a TileMapIndexError
        """
        logger.error(f"{self} Unable to access key {key}")
        raise TileMapIndexError(self, key, None)

    def __setitem__(self, key: Tuple[int, int], value: TileNode):
        """
        Updates the tilemap instance with a key value pair representing
        a location on the map with a TileNode object
        """
        if isinstance(key, tuple) and isinstance(value, TileNode):
            if (
                key[0] >= 0
                and key[0] < self.map_size_x
                and key[1] >= 0
                and key[1] < self.map_size_y
            ):
                self.data[key] = value
            else:
                logger.error(f"Invalid coordinate key {key} for {self}")
                raise TileMapIndexError(self, key, value)
        else:
            logger.error(f"Invalid input to {self}")
            raise TileMapIndexError(self, key, value)
