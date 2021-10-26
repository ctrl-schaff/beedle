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
        self._form_topological_graph()

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

    def _form_topological_graph(self, graph_start: tuple, graph_end: tuple):
        inventory = set()
        full_map_coordinates = set()
        current_goal = None
        while (graph_end not in full_map_coordinates):
            

        

    def __getitem__(self, index: tuple):
        graph_entry = z2p.node.TileNode()
        try:
            graph_entry = self._tile_graph[index]
        except KeyError as gen_err:
            raise gen_err
        return graph_entry
