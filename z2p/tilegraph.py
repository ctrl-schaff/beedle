"""
TileGraph:
Converting the raw map data into a set of connected nodes in a graph for
traversal purposes data structure for storing the converted
map data with tile information
    - TileGraph stores a collection of TileData objects
"""

import itertools
from typing import List

from loguru import logger

from .pathprocessor import PathProcessor
from .tilelocations import LocationMap
from .tilemap import TileMap
from .tilenode import TileNode
from .tilesearch import PartialTileMap


class TileGraph:
    """
    Graph object for handling the map node connections
    """

    def __init__(
        self,
        graph_start: tuple,
        graph_end: tuple,
        tile_map: TileMap,
        location_map: LocationMap,
    ):
        self.graph_start = graph_start
        self.graph_end = graph_end
        self._tile_graph = {}

        self._form_tile_graph(tile_map, location_map)

    def _form_tile_graph(self, tile_map: TileMap, location_map: LocationMap):
        """
        Iteratively explores the map and continually updates the topological
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
        """
        map_chunk = self.__find_map_chunks(tile_map, location_map)
        self.__process_bottlenecks(bottlenecks)

        return (topo_graph, map_chunk, bottlenecks)

    def __find_map_chunks(
        self,
        tile_map: TileMap,
        location_map: LocationMap,
        stage_limit: int = None,
    ) -> List[set]:
        """
        Explore the map in chunks given the constraints provided
        by the configuration. Iterates over the map until the
        graph_end specified in the constructor has been marked as
        completed or we reach the iteration limit set by the
        stage_limit value
        """
        if stage_limit is None:
            stage_limit = 100

        map_chunk = []
        completed_keys = set()
        search_inventory = set()
        bottlenecks = {}

        chunk_count = 0
        chunk_pointer = None
        while self.graph_end not in completed_keys:
            logger.info(f"Graph Search Partial Chunk #{chunk_count}")
            chunk_count += 1

            ptile_map = PartialTileMap(
                tile_map, self.graph_start, search_inventory
            )

            ptile_map.find_new_locations(
                tile_map, location_map, completed_keys, search_inventory
            )
            map_chunk.append(ptile_map)

            if chunk_pointer:
                item_bottleneck = set.intersection(
                    ptile_map.cost_collection, chunk_pointer.reward_collection
                )

                bottleneck_coord = location_map.location_item_lookup(
                    item_bottleneck
                )
                bottlenecks[bottleneck_coord[0]] = item_bottleneck

            chunk_pointer = ptile_map

        return map_chunk

    def __process_bottlenecks(self, bottlenecks):
        (bn_iter1, bn_iter2) = itertools.tee(bottlenecks.items(), 2)
        bn_iter2.__next__()
        for bn1, bn2 in itertools.zip_longest(bn_iter1, bn_iter2):
            if bn2 and bn1[0]:
                connection_set = set()
                if topo_graph[bn2[0]][0]:
                    for coord in topo_graph[bn2[0]]:
                        connection_set.add(coord)
                connection_set.add(bn1[0])
                topo_graph[bn2[0]] = tuple(connection_set)

    # def __getitem__(self, index: tuple) -> TileNode:
    #     graph_entry = None
    #     try:
    #         graph_entry = self._tile_graph[index]
    #     except KeyError as gen_err:
    #         raise gen_err
    #     return graph_entry

    # def process_graph(self,
    #                   graph_start: tuple,
    #                   graph_end: tuple,
    #                   map_logic,
    #     (topo_graph, map_chunk, bottlenecks) = self.form_topological_graph(
    #         graph_start, graph_end, map_logic
    #     )
    #     full_node = [graph_start]
    #     for coord in bottlenecks.keys():
    #         full_node.append(coord)
    #     # full_node.append(graph_end)

    #     pathproc = z2p.pathprocessor.PathProcessor(self, map_logic, map_item)
    #     count = 0
    #     trees = []
    #     for node in full_node:
    #         try:
    #             item = bottlenecks[node]
    #             pathproc.global_inventory.update(item)
    #         except KeyError:
    #             pass

    #         (region_keys, tile_paths) = pathproc.initialize_search_space(node)
    #         subtree = pathproc.search_region_space(node,
    #                                                tile_paths,
    #                                                region_keys)
    #         trees.extend(subtree)
    #         print(f'Iteration {count} | {node}')
    #         count += 1
