"""
TileGraph:
Converting the raw map data into a set of connected nodes in a graph for
traversal purposes data structure for storing the converted
map data with tile information
    - TileGraph stores a collection of TileData objects
"""

from collections import OrderedDict
import itertools
from typing import List, Set, Tuple

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
        self._tile_graph = {}
        self.bottlenecks = self.__translate_map_data(tile_map, location_map)

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

        bottlenecks = OrderedDict()

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
                self.add_node(location)

            node_vertices = itertools.permutations(
                partial_tile_map.completed_locations, 2
            )
            for vertex in node_vertices:
                self.update_node_edge(vertex[0], vertex[1])

            bottleneck_subset = self.__find_bottleneck(
                partial_tile_map,
                previous_partial_tile_map,
                location_map,
            )
            bottlenecks.update(bottleneck_subset)
            previous_partial_tile_map = partial_tile_map
        return bottlenecks

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
    ) -> dict:
        """
        Compares two sequentially created PartialTileMap(s) and compares the
        stored cost items found from the current PartialTileMap with the stored
        reward items found from the previous PartialTileMap. The itersection of
        these two sets are the "bottleneck" items that prevented the previous
        PartialTileMap from exploring further

        These items and locations need to be joined across PartialTileMaps
        on the graph to ensure that logically connected locations share an edge

        It also stores the bottleneck as a dictionary with the
        following key-value pair structure
            > key: reward_location Tuple[int, int]
            > value: cost_location Set[Tuple[int, int]]
        """
        bottleneck_subset = {}
        if prev_partial_map:
            item_bottleneck = set.intersection(
                current_partial_map.cost_collection,
                prev_partial_map.reward_collection,
            )
            logger.info(f"Found item bottleneck {item_bottleneck}")

            for item in item_bottleneck:
                reward_location = location_map.location_reward_search(item)
                cost_location = location_map.location_cost_search(item)
                bottleneck_subset[reward_location] = set(cost_location)

                bottleneck_locations = location_map.location_search(item)
                node_vertices = itertools.permutations(bottleneck_locations, 2)
                for vertex in node_vertices:
                    self.update_node_edge(vertex[0], vertex[1])
        return bottleneck_subset

    def add_node(self, node: Tuple[int, int]) -> None:
        """
        Attempts to add a new node to the graph
        If the node already exists, then no action is performed
        """
        if node not in self._tile_graph:
            self._tile_graph[node] = set()
            logger.info(f"Added new node {node} to graph")
        else:
            logger.info(
                f"Node {node} -> {self._tile_graph[node]} exists in graph"
            )

    def update_node_edge(
        self, node: Tuple[int, int], connected_node: Tuple[int, int]
    ) -> None:
        """
        Attempts to create an edge on the graph by adding connecting two nodes
        together (represented by adding the node to the dictionary value set

        If the node doesn't exist, then we create the node by adding the edge
        """
        if node not in self._tile_graph:
            self.add_node(node)

        self._tile_graph[node].add(connected_node)
        logger.info(f"Update node {node} -> {self._tile_graph[node]}")

    def get_node(self, node: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """
        Attempts to access the a node in the graph based off the key
        value Tuple[int, int] and returns the connected nodes
        """
        connected_nodes = None
        if node not in self._tile_graph:
            logger.info(f"Unable to find node {node} in the graph")
            connected_nodes = set()
        else:
            connected_nodes = self._tile_graph[node]
            logger.info(f"Found connected nodes {node} -> {connected_nodes}")
        return connected_nodes

    def topological_sort(
        self, location_map: LocationMap
    ) -> List[Tuple[int, int]]:
        """
        Returns a topological sorted list of locations to fully
        process the 2D map in logical order
        """
        starting_connection = {self.graph_start: None}
        topo_sort = [starting_connection]
        for reward_location, cost_locations in self.bottlenecks.items():
            logger.info(f"Graph Sort Length #{len(topo_sort)}")
            logger.info(
                f"Current node {reward_location}\n{location_map[reward_location]}"
            )
            connection = {reward_location: cost_locations}
            topo_sort.append(connection)
        logger.info(topo_sort)
        return topo_sort
