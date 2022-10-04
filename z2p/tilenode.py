#!/usr/bin/env python3

"""
Data Structure for storing constant properties of the map tiles
> identifier <int>
    >  ID used as value to represent the tile in map data structure
> location <tuple>
    > Coordinates storing the (X, Y) pair representing the map
    location entrance
> background <str>
    > ID used to give basic description of what the map tile represents
    (ie. water, mountain, grassland, etc...)
> symbol <str>
    > ID character representing the tile in ascii format for the
    map data structure
> color <str>
    > Value to represent the tile color when plotted
    > Typically stored in a hexadecimal format
> description <str>
    > Short textual desccription to provide any map related details
    about the tile
    (ie. Cave 4, Palace <Name>, Town of <Name>, etc ...)
> traversal_cost <tuple>
    > Collection of string values representing costs required to access
      the tile for connected nodes.
    > No traversal cost requirement is represented by '|'.
    > Multiple costs may be required in which all of them must be present
      in inventory before acquring access
> reward_cost <tuple>
    > Collection of string values representing costs required to attain
    the reward contained on the tile
    No reward cost requirement is represented by '|'.
    Multiple costs may be required in which all of them must be present
    in inventory before acquring access to the reward
> reward <tuple>
    > Collection of string values representing the reward(s) available on
    the designated tile
    No reward is represented by '|'.
    Multiple rewards may be available on the tile
> edges <tuple>
    > Collection of nodes that connect the current TileNode to
    other TileNodes on the may for traversal
"""


import operator
from typing import Tuple

from loguru import logger
import numpy as np


class TileNode:
    def __init__(
        self,
        tile_value: int,
        map_data: np.array,
        location_properties: dict,
        tile_properties: dict,
    ):
        self.identifier = tile_value
        self.location = location_properties["entrance"]

        self.description = location_properties.description

        self.traversal_cost = location_properties["traversal_cost"]
        self.reward_cost = location_properties["reward_cost"]
        self.reward = location_properties["reward"]

        self.background = tile_properties["TYPE"]
        self.symbol = tile_properties["SYMBOL"]
        self.color = tile_properties["COLOR"]

        exit_edge = location_properties["exit"]
        self.edges = self.get_node_edges(map_data, exit_edge)

    def __repr__(self) -> str:
        tile_node_repr = (
            "TileNode(\n"
            f"\ttile_coordinates -> {self.location}\n"
            f"\ttile_value -> {self.identifier}\n"
            f"\tmap_data\n"
            f"\tlocation_properties\n"
            f"\ttile_properties\n"
        )
        return tile_node_repr

    def __str__(self) -> str:
        edge_str = "{" + " ".join(map(str, self.edges)) + "}"
        tile_node_str = (
            f"Tile Coordinates:[{self.location}]\n"
            f"Tile Type:{self.background}\n"
            f"Tile Description:{self.description}\n"
            f"Tile Edges:{edge_str}"
        )
        return tile_node_str

    def get_node_edges(
        self, map_size: Tuple[int, int], exit_edge: Tuple[int, int]
    ) -> tuple:
        """
        Generate all edge values for the TileNode object

        This looks at all adjacent coordinate values and adds them to a list as a collection
        of Tuple[int, int] types

        Additional checks the location properties for an exit value that is different
        than the entrance to indicate a potential non-adjacent node that should be added
        to the edges collection
        """
        adj_edges = self.get_neighbors(self.location)
        map_x_limit, map_y_limit = map_size
        edges = [
            edge
            for edge in adj_edges
            if (
                (edge[0] >= 0 and edge[0] < map_x_limit)
                and (edge[1] >= 0 and edge[1] < map_y_limit)
            )
        ]

        if self.location != exit_edge:
            logger.debug(f"Found additional exit edge {exit_edge} for {self}")
            edges.append(exit_edge)

        return tuple(edges)

    @classmethod
    def get_neighbors(cls, node_position: tuple) -> list:
        """
        Calculates all neighbors in cardinal directions on a
        coordinate plane (left, right, up, down)
        (X, Y) - Coordinate Pair

        (X, Y) + (1, 0) -> (X+1, Y)
        (X, Y) + (0, 1) -> (X, Y+1)
        (X, Y) + (-1, 0) -> (X-1, Y)
        (X, Y) + (0, -1) -> (X, Y-1)

        Output: ((X+1, Y), (X, Y+1), (X-1, Y), (X, Y-1))
        """
        cardinal_directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        return [
            tuple(map(operator.add, node_position, move))
            for move in cardinal_directions
        ]
