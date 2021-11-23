#!/usr/bin/env python3

"""
TileGraph:
Converting the raw map data into a set of connected nodes in a graph for traversal purposes
Data structure for storing the converted Map data with Tile information
    - TileGraph stores a collection of TileData objects
"""

import itertools

import z2p.node
import z2p.pathprocessor
import z2p.utility


class TileGraph:
    """
    Graph object for handling the map node connections
    """

    def __init__(self, map_data, logic_table, tile_table):
        self._tile_graph = dict()
        self._form_tile_graph(map_data, logic_table, tile_table)

    def _form_tile_graph(self, map_data, logic_table, tile_table) -> None:
        """
        Iterates over the coordinates of the map based off dimensions and creates a graph
        with the associated map logic for transforming (X, Y) -> TileNode()
        """
        map_dim_product = (range(map_data.MAP_SIZE_X), range(map_data.MAP_SIZE_Y))
        for (row_index, col_index) in itertools.product(
            map_dim_product[0], map_dim_product[1]
        ):
            tile_coord = (row_index, col_index)
            tile_id = map_data[tile_coord]
            tile_node = z2p.node.create_node(
                tile_coord, tile_id, map_data, logic_table, tile_table
            )
            self._tile_graph[tile_coord] = tile_node

    def form_topological_graph(self,
                               graph_start: tuple,
                               graph_end: tuple,
                               map_logic,
                               map_item):
        """
        Iteratively explores the map and continually updates the topological
        graph formed from the logic tiles.
        Process:
            > Explore the entire possible region with a given inventory
            > Using the maplogic object, extract the import "key" tiles
              from the entire possible region
            > Iterate over those found keys and see if the criteria is met
              to obtain the reward
            > If the reward cost is met, update the inventory and add the
              tile to the completed / visited keys set to avoid further
              duplicate processing
            > If the traversal cost is met, update the connections associated
              with that "key" tile
        End Criteria:
            > Add the graph_end tile point to the completed_keys set
        """
        path_proc = z2p.pathprocessor.PathProcessor(self, map_logic, map_item)
        topo_graph = dict()
        completed_keys = set()

        while graph_end not in completed_keys:
            interim_inventory = set()
            region_stack, _ = path_proc.explore_region(graph_start)

            region_keys = set(path_proc.key_tile) & set(region_stack)
            for rkey in region_keys.difference(completed_keys):
                rcost = set([*self._tile_graph[rkey].reward_cost])
                tcost = set([*self._tile_graph[rkey].traversal_cost])

                item_set = rcost | tcost
                # topo_graph[rkey] = item_set
                topo_graph[rkey] = map_logic.reward_lookup(item_set)

                if rcost.issubset(path_proc.global_inventory):
                    for reward_item in self._tile_graph[rkey].reward:
                        interim_inventory.add(reward_item)

                if (rcost.issubset(path_proc.global_inventory) and
                        tcost.issubset(path_proc.global_inventory)):
                    completed_keys.add(rkey)
                
            path_proc.global_inventory.update(interim_inventory)
        breakpoint()
        return topo_graph

    def __getitem__(self, index: tuple):
        graph_entry = z2p.node.TileNode()
        try:
            graph_entry = self._tile_graph[index]
        except KeyError as gen_err:
            raise gen_err
        return graph_entry
