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
    """
    Represents a subset of the total TileMap explored via
    the floodfill argument

    The item_inventory and configuration determine the total
    subset explorable by the floodfill argument based off the
    traversal_cost requirements for the TileNodes in the TileMap
    """

    def __init__(
        self, tile_map: TileMap, start_coord: Coord, item_inventory: Set[str]
    ):
        self.reward_collection = set()
        self.cost_collection = set()
        self.search_inventory = set()
        self.completed_locations = set()
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
        """
        logger.info(f"Running floodfill algorithm @ {start_coord}")

        if item_inventory is None:
            item_inventory = set()

        search_queue = deque()
        discover_queue = deque()

        search_queue.append(start_coord)
        while len(search_queue) > 0:
            search_coord = search_queue.pop()
            discover_queue.append(search_coord)

            tile_node = tile_map[search_coord]
            for edge in tile_node.edges:
                if edge not in discover_queue and edge not in search_queue:
                    tcost = tile_map[edge].traversal_cost
                    if tcost.issubset(item_inventory):
                        search_queue.append(edge)
        logger.info(f"Generated queue of length {len(discover_queue)}")
        return discover_queue

    def find_completed_locations(
        self,
        tile_map: TileMap,
        location_map: LocationMap,
        completed_locations: set,
        search_inventory: set,
    ) -> None:
        """
        After having performed the floodfill algorithm to complete the
        full set of discoverable TileNodes within the TileMap for this
        subsection, this method finds all locations specified by the
        LocationMap

        It then takes the difference between those locations and the completed
        locations to ensure that all locations discovered are unique to this
        PartialTileMap

        Iterates over the unique locations for this PartialTileMap:
            > Updates the reward_collection property with all unique
            locations reward values
            > Updates the cost_collection property with all unique
            locations cost values
            > Checks if the reward_cost is met to update the search_inventory
            with any rewards that were discovered in the unique_location
            > Checks if the total_cost has been met by the search_inventory
            in order to mark the location as having been completed
        """
        discovered_locations = self.discovered_locations(location_map)
        unique_locations = discovered_locations.difference(completed_locations)

        for location in unique_locations:
            unique_node = tile_map[location]

            reward_collection = unique_node.reward
            reward_cost = unique_node.reward_cost
            traversal_cost = unique_node.traversal_cost
            total_cost = reward_cost | traversal_cost

            self.reward_collection.update(reward_collection)
            self.cost_collection.update(total_cost)

            if reward_cost.issubset(search_inventory):
                self.search_inventory.update(reward_collection)

            if total_cost.issubset(search_inventory):
                self.completed_locations.add(location)

    def discovered_locations(self, location_map: LocationMap) -> set:
        """
        Compares the discovered tiles against the full set
        of key locations and returns the intersection
        """
        full_location_set = location_map.entrance_locations
        partial_set = set(self.partial_map_tiles)
        discovered_locations = full_location_set.intersection(partial_set)
        return discovered_locations
