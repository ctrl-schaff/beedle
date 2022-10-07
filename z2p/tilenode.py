#!/usr/bin/env python3

"""
Data Structure for storing constant properties of the map tiles
> identifier <int>
    > ID used as value to represent the tile in map data structure
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
    > Short textual description to provide any map related details
      about the tile
      (ie. Cave 4, Palace <Name>, Town of <Name>, etc ...)
> traversal_cost <tuple>
    > Collection of string values representing costs required to access
      the tile for connected nodes.
    > No traversal cost requirement is represented by '|'.
    > Multiple costs may be required in which all of them must be present
      in inventory before acquiring access
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


class TileNode:
    def __init__(
        self,
        tile_location: Tuple[int, int],
        tile_value: int,
        map_size: Tuple[int, int],
        location_properties: dict,
        tile_properties: dict,
    ):
        self.identifier = tile_value
        self.location = tile_location

        self.description = location_properties.get("description", None)
        self.traversal_cost = location_properties.get("traversal_cost", None)
        self.reward_cost = location_properties.get("reward_cost", None)
        self.reward = location_properties.get("reward", None)

        self.background = tile_properties["TYPE"]
        self.symbol = tile_properties["SYMBOL"]
        self.color = tile_properties["COLOR"]

        exit_edge = location_properties.get("exit", tile_location)
        self.edges = self.__get_node_edges(map_size, exit_edge)

    def __repr__(self) -> str:
        edge_repr = "{" + " ".join(map(str, self.edges)) + "}"
        tile_node_repr = (
            "TileNode\n"
            "{\n"
            f"\tlocation: {self.location}\n"
            f"\ttile_value:  {self.identifier}\n"
            f"\tdescription: {self.description}\n"
            f"\ttraversal_cost: {self.traversal_cost}\n"
            f"\treward_cost: {self.reward_cost}\n"
            f"\treward: {self.reward}\n"
            f"\tbackground: {self.background}\n"
            f"\tsymbol: {self.symbol}\n"
            f"\tcolor: {self.color}\n"
            f"\tedges: {edge_repr}\n"
            "}\n"
        )
        return tile_node_repr

    def __str__(self) -> str:
        edge_str = "{" + " ".join(map(str, self.edges)) + "}"
        tile_node_str = (
            f"TileNode {id(self)}\n"
            "{\n"
            f"\tTile Coordinates: [{self.location}]\n"
            f"\tTile Type: {self.background}:{self.identifier}\n"
            f"\tTile Description: {self.description}\n"
            f"\tTile Edges: {edge_str}\n"
            "}\n"
        )
        return tile_node_str

    def __get_node_edges(
        self, map_size: Tuple[int, int], exit_edge: Tuple[int, int]
    ) -> tuple:
        """
        Generate all edge values for the TileNode object

        This looks at all adjacent coordinate values and adds them to a list
        as a collection of Tuple[int, int] types

        Additional checks the location properties for an exit value that is
        different than the entrance to indicate a potential non-adjacent node
        that should be added to the edges collection
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
