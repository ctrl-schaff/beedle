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

import numpy as np

from .tilelocations import LocationMap


class TileNode:
    def __init__(
        self,
        node_location: tuple,
        map_data: np.array,
        location_map: LocationMap,
        tile_table: dict,
    ):
        node_id = map_data[node_location]
        self.identifier = node_id
        self.location = node_location

        self.background = tile_table[node_id]["TYPE"]
        self.symbol = tile_table[node_id]["SYMBOL"]
        self.color = tile_table[node_id]["COLOR"]

        logic_entry = location_map[self.location]
        self.description = logic_entry.description
        self.traversal_cost = logic_entry.traversal_cost
        self.reward_cost = logic_entry.reward_cost
        self.reward = logic_entry.reward

        self.edges = self.get_node_edges(map_data, logic_entry)

    def __repr__(self) -> str:
        edge_str = "{" + " ".join(map(str, self.edges)) + "}"
        fstr = "\nTILE:[{0:d},{1:d}]\nTYPE:{2:s}\nDESC:{3:s}\nEDGE:{4:s}"
        return fstr.format(*self.location, self.background, self.description, edge_str)

    def get_node_edges(self, map_data: np.array, location: dict) -> tuple:
        """
        Get the adjacent node edges that fit the logic
        """
        adj_edges = self.get_neighbors(self.location)
        (mapx, mapy) = map_data.map_data.shape
        edges = [
            edge
            for edge in adj_edges
            if ((edge[0] >= 0 and edge[0] < mapx) and (edge[1] >= 0 and edge[1] < mapy))
        ]

        if location["entrance"] != location["exit"]:
            location_exit = tuple(location["exit"])
            edges.append(location_exit)

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
