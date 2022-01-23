#!/usr/bin/env python3

"""
TileNode:
    Data structure for storing concepts related to the tile properties
"""


from dataclasses import dataclass

import z2p.utility
import z2p.map_logic


@dataclass(init=True, repr=True, frozen=True)
class TileNode:
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
    No traversal cost requirement is represented by "|".
    Multiple costs may be required in which all of them must be present
    in inventory before acquring access
    > reward_cost <tuple>
        > Collection of string values representing costs required to attain
        the reward contained on the tile
        No reward cost requirement is represented by "|".
        Multiple costs may be required in which all of them must be present
        in inventory before acquring access to the reward
    > reward <tuple>
        > Collection of string values representing the reward(s) available on
        the designated tile
        No reward is represented by "|".
        Multiple rewards may be available on the tile
    > edges <tuple>
        > Collection of nodes that connect the current TileNode to
        other TileNodes on the may for traversal
    """
    identifier: int = -1
    location: tuple = ()
    background: str = ""
    symbol: str = ""
    color: str = ""
    description: str = ""
    traversal_cost: tuple = ()
    reward_cost: tuple = ()
    reward: tuple = ()
    edges: tuple = ()

    def __repr__(self) -> str:
        edge_str = "{" + " ".join(map(str, self.edges)) + "}"
        fstr = "\nTILE:[{0:d},{1:d}]\nTYPE:{2:s}\nDESC:{3:s}\nEDGE:{4:s}"
        return fstr.format(*self.location,
                           self.background,
                           self.description,
                           edge_str)


def create_node(
    node_location: tuple, node_id: int, coord_map, logic_table, tile_table
) -> TileNode:
    """
    Using the map logic configuration file, we can take the static position
    data stored in map and create a node in the graph
    """
    logic_entry = logic_table[node_location]
    node_edges = get_node_edges(node_location, coord_map, logic_entry)

    node_obj = TileNode(
        node_id,
        node_location,
        tile_table[node_id]["TYPE"],
        tile_table[node_id]["SYMBOL"],
        tile_table[node_id]["COLOR"],
        logic_entry.description,
        logic_entry.traversal_cost,
        logic_entry.reward_cost,
        logic_entry.reward,
        node_edges,
    )
    return node_obj


def get_node_edges(location: tuple, coord_map, logic_entry) -> tuple:
    """
    Get the adjacent node edges that fit the logic
    """
    adj_edges = z2p.utility.get_neighbors(location)
    (mapx, mapy) = coord_map.map_data.shape
    edges = [
        edge
        for edge in adj_edges
        if ((edge[0] >= 0 and edge[0] < mapx) and
            (edge[1] >= 0 and edge[1] < mapy))
    ]

    if logic_entry.entrance != logic_entry.exit:
        edges.append(logic_entry.exit)
    return tuple(edges)
