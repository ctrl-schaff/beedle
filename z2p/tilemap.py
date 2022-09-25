'''
TileMap:
Converting the raw map data into a dictionary of connected nodes 
storing the converted map data with tile information
    - TileMap stores a collection of Node objects
Maps (xcoord, ycoord) -> TileNode

'''

from collections import UserDict
import itertools
from typing import (List,
                    Tuple)

from loguru import logger
import numpy as np

from .exceptions import TileMapIndexError
from .tilelocations import LocationMap
from .tilenode import TileNode


class TileMap(UserDict):
    '''
    Graph object for handling the map node connections
    '''

    def __init__(self,
                 map_data: np.array,
                 location_table: List[dict],
                 tile_table: dict):
        self.map_size_x, self.map_size_y = map_data.size()
        _tile_map = self._form_tile_map(map_data,
                                        location_table,
                                        tile_table)
        super().__init__(_tile_map)
        
    def __repr__(self) -> str:
        map_data_repr = f'[{self.map_size_x, self.map_size_y}]'
        tilemap_repr = ('TileMap(\n'
                        f'\tmap_data -> {map_data_repr}\n'
                        f'\tlocation_table\n'
                        f'\ttile_table\n')
        return tilemap_repr

    def __str__(self) -> str:
        map_data_repr = f'[{self.map_size_x, self.map_size_y}]'
        tilemap_str = f'TileMap Instance {map_data_repr} {id(self)}\n'
        return tilemap_str

    def _form_tile_map(self,
                       map_data: np.array,
                       location_table: List[dict],
                       tile_table) -> dict:
        '''
        Iterates over the coordinates of the map based off dimensions and
        creates a graph with the associated map logic for
        transforming (X, Y) -> TileNode()
        '''
        tile_map = {}
        location_map = LocationMap(location_table)
        map_dim_x, map_dim_y = map_data.size()
        map_traversal = itertools.product(range(map_dim_x), range(map_dim_y))
        for (row_index, col_index) in map_traversal:
            tile_coord = (row_index, col_index)
            tile_node = TileNode(tile_coord,
                                 map_data,
                                 location_map,
                                 tile_table)
            tile_map[tile_coord] = tile_node
            logger.debug(f'Added {tile_node} to {self}@{tile_coord}')
        return tile_map

    def __setitem__(self, key: Tuple[int, int], value: TileNode):
        '''
        Updates the tilemap instance with a key value pair representing
        a location on the map with a TileNode object
        '''
        if isinstance(key, tuple) and isinstance(value, TileNode):
            if (key[0] > 0 and key[0] <= self.map_size_x and
                    key[1] > 0 and key[1] <= self.map_size_y):
                self.data[key] = value
            else:
                logger.error(f'Invalid coordinate key {key} for {self}')
                raise TileMapIndexError(self, key, value)
        else:
            logger.error(f'Invalid input to {self}')
            raise TileMapIndexError(self, key, value)
