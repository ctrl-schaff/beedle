"""
TileGraph:
Converting the raw map data into a set of connected nodes in a graph for
traversal purposes data structure for storing the converted
map data with tile information
    - TileGraph stores a collection of TileData objects
"""

import itertools
from typing import Set, Tuple

from loguru import logger

from .tilelocations import LocationMap
from .tilemap import TileMap
from .tilesearch import PartialTileMap


class TileGraph:
    """
    Graph object for handling the map node connections
    """

    def __init__(
        self,
        graph_start: Tuple[int, int],
        graph_end: Tuple[int, int],
        tile_map: TileMap,
        location_map: LocationMap,
    ):
        self.graph_start = graph_start
        self.graph_end = graph_end
        self._tile_graph = self.__translate_map_data(tile_map, location_map)

    def __translate_map_data(
        self, tile_map: TileMap, location_map: LocationMap
    ) -> dict:
        """
        Iteratively explores the map and continually updates the
        graph formed from the logic tiles.

        Process:
            > Explore the entire possible region with a given inventory
            > Using the maplogic object, extract the import 'key' tiles
              from the entire possible region
            > Iterate over those found keys and see if the criteria is met
              to obtain the reward
            > If the reward cost is met, update the inventory and add the
              tile to the completed / visited keys set to avoid further
              duplicate processing
            > If the traversal cost is met, update the connections associated
              with that 'key' tile
        End Criteria:
            > Add the graph_end tile point to the completed_keys set

        Explore the map in chunks given the constraints provided
        by the configuration. Iterates over the map until the
        graph_end specified in the constructor has been marked as
        completed or we reach the iteration limit set by the
        stage_limit value
        """
        logger.info("Transforming TileMap {tile_map} into TileGraph")
        tilegraph = {}
        global_completed_locations = set()
        global_item_inventory = set()

        previous_partial_tile_map = None

        chunk_count = 0
        while self.graph_end not in global_completed_locations:
            logger.info(f"Graph Search Chunk #{chunk_count}")
            chunk_count += 1

            partial_tile_map = self.__create_partial_map(
                tile_map,
                location_map,
                global_item_inventory,
                global_completed_locations,
            )

            for location in partial_tile_map.completed_locations:
                if not tilegraph.get(location, None):
                    tilegraph[location] = set()

            node_vertices = itertools.permutations(
                partial_tile_map.completed_locations, 2
            )
            for vertex in node_vertices:
                tilegraph[vertex[0]].add(vertex[1])

            self.__find_bottleneck(
                partial_tile_map,
                previous_partial_tile_map,
                location_map,
                tilegraph,
            )
            previous_partial_tile_map = partial_tile_map
        return tilegraph

    def __create_partial_map(
        self,
        tile_map: TileMap,
        location_map: LocationMap,
        global_item_inventory: Set[str],
        global_completed_locations: Set[Tuple[int, int]],
    ) -> PartialTileMap:
        """
        Creates an instance of a PartialTileMap and attempts to find all
        completed locations within the explorable region generated by
        the object
        """

        ptile_map = PartialTileMap(
            tile_map, self.graph_start, global_item_inventory
        )

        ptile_map.find_completed_locations(
            tile_map,
            location_map,
            global_completed_locations,
            global_item_inventory,
        )
        global_item_inventory.update(ptile_map.search_inventory)
        global_completed_locations.update(ptile_map.completed_locations)
        return ptile_map

    def __find_bottleneck(
        self,
        current_partial_map: PartialTileMap,
        prev_partial_map: PartialTileMap,
        location_map: LocationMap,
        tilegraph: dict,
    ):
        """
        Compares two sequentially created PartialTileMap(s) and compares the
        stored cost items found from the current PartialTileMap with the stored
        reward items found from the previous PartialTileMap. The itersection of
        these two sets are the "bottleneck" items that prevented the previous
        PartialTileMap from exploring further

        These items and locations need to be joined across PartialTileMaps
        on the graph to ensure that logically connected locations share an edge
        """
        if prev_partial_map:
            item_bottleneck = set.intersection(
                current_partial_map.cost_collection,
                prev_partial_map.reward_collection,
            )
            logger.info(f"Found item bottleneck {item_bottleneck}")

            for item in item_bottleneck:
                bottleneck_locations = []
                bottleneck_locations.extend(
                    location_map.location_reward_search(item)
                )
                bottleneck_locations.extend(
                    location_map.location_cost_search(item)
                )
                node_vertices = itertools.permutations(bottleneck_locations, 2)
                for vertex in node_vertices:
                    tilegraph[vertex[0]].add(vertex[1])
