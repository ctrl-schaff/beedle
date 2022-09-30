"""
Class for handling searching partial "chunks" of 
the TileMap and storing properties related to the
subsequent search
"""

from collections import deque
from typing import Mapping, Tuple, Set

from loguru import logger

from .tilelocations import LocationMap
from .tilemap import TileMap
from .tilenode import TileNode


Coord = Tuple[int, int]
LinkMap = Mapping[TileNode, Coord]


class PartialTileMap:
    def __init__(
        self, tile_map: TileMap, start_coord: Coord, item_inventory: Set[str]
    ):
        self.link_map = {}
        self.partial_map_tiles = self.floodfill(
            tile_map, start_coord, item_inventory
        )

    def floodfill(
        self, tile_map: TileMap, start_coord: tuple, item_inventory: set = None
    ) -> deque:
        """
        Flood fill algorithm to explore entire discoverable region

        Given two double ended queues
            > discover_queue
                > Collection of Coord <Tuple[int, int]> found from search_queue
            > search_queue
                > Collection of tCoord <Tuple[int, int]> accumulated while
                traversing the TileMap
                > Nodes are appended to the end of the queue if the current
                search_node popped from the top are traversable
                    > The TileNode is considered traversible if the traversal
                    cost set is a subset of the inventory passed to the method
                > These TileNodes are added by examining the edges for each
                TileNode in the TileMap

        Returns
            > discover_queue processed from the TileMap
            > link_map generated from filling the TileMap
        """
        if item_inventory is None:
            item_inventory = set()

        search_queue = deque()
        discover_queue = deque()
        search_queue.append(start_coord)

        start_node = tile_map[start_coord]
        self.link_map[start_node] = None

        while len(search_queue) > 0:
            search_coord = search_queue.pop()
            logger.debug(f"Processing {search_coord}")
            discover_queue.append(search_coord)

            tile_node = tile_map[search_coord]
            for edge in tile_node.edges:
                logger.debug(f"Processing {search_coord} edge {edge}")
                if edge not in discover_queue and edge not in search_queue:
                    tcost = set(tile_map[edge].traversal_cost)
                    if tcost.issubset(item_inventory):
                        search_queue.append(edge)
                        self.link_map[tile_map[edge]] = search_coord
        return discover_queue

    def discovered_locations(self, full_location_map: LocationMap) -> set:
        """
        Compares the discovered tiles against the full set
            of key locations and returns the intersection
        """
        full_location_set = full_location_map.location_coordinates
        partial_set = set(self.partial_map_tiles)
        discovered_locations = full_property_set.intersection(partial_set)
        return discovered_locations
