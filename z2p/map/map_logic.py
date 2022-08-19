#!/usr/bin/env python3

"""
TileLogic:
    - Data structure for holding information on cost and reward
"""


from dataclasses import dataclass

import z2p.utility
import z2p.graph


@dataclass(init=True, repr=True, frozen=True)
class LogicData:
    """
    Data class for handling the map logic typing. Manipulated
    by the MapLogic class as a container / processor for the
    data strcture
    """

    description: str
    entrance: tuple
    exit: tuple
    traversal_cost: tuple
    reward_cost: tuple
    reward: tuple

    def __repr__(self) -> str:
        tcost_str = "%s" % (self.traversal_cost,)
        rcost_str = "%s" % (self.reward_cost,)
        reward_str = "%s" % (self.reward,)
        fstr = "\nTRAVERSE COST:{0:s}\nREWARD COST:{1:s}\nREWARD:{2:s}"
        return fstr.format(tcost_str, rcost_str, reward_str)


class MapLogicData:
    """
    MapLogic
    Wrapper class for importing the map logic for specific tile attributes.
    This includes non-adjacent connected edges, costs, and items
    """

    def __init__(self,
                 logic_file: str,
                 tiledata,
                 mapdata):
        logic_data = z2p.utility.load_json_data(logic_file)
        self.logic_lookup = self._format_lookup_table(logic_data)
        self.tiledata = tiledata
        self.mapdata = mapdata

    @property
    def logic_tile(self) -> set:
        """
        Map logic data property for the corresponding logic tile locations
        """
        logic_tiles = set(self.logic_lookup.keys())
        return logic_tiles

    def default_logic_entry(self, node_location: tuple) -> LogicData:
        """
        Default map tile logic for entries that have no indicated logic
        """
        description = "Default"
        entrance_pair = node_location
        exit_pair = node_location
        node_id = self.mapdata[node_location]

        traversal_cost = self._base_tile_traversal_cost(node_id)
        reward_cost = tuple("|")
        reward = tuple("|")

        return LogicData(description,
                         entrance_pair,
                         exit_pair,
                         traversal_cost,
                         reward_cost,
                         reward
                         )

    def _base_tile_traversal_cost(self, node_id) -> tuple:
        """
        Determine the base traversal cost for a map tile.
        The traversal cost is the requirement to travel to a node
        from an adjacently connected node
        If a tile has an impossible traversal cost, it likely represents
        the edge of the map and will equal "X"
        """
        walk_status = self.tiledata[node_id]["WALKABLE"]
        base_traversal_cost = self.tiledata[node_id]["BASE_COST"]

        if walk_status:
            traversal_cost = tuple([base_traversal_cost])
        else:
            traversal_cost = tuple("X")

        return traversal_cost

    @classmethod
    def _format_lookup_table(cls, raw_logic_data: dict):
        """
        Cleanup the data import so that the dictionary lookup process
        involves passing the coordinate tuple to the MapLogic instance
        mp = MapLogic(<filepath>)
        coord_logic = mp[(X, Y)]
        """
        logic_lookup = dict()
        for entry in raw_logic_data:
            description = str(entry["Description"])
            entrance_pair = (
                int(entry["Entrance X Position"]),
                int(entry["Entrance Y Position"]),
            )
            exit_pair = (int(entry["Exit X Position"]),
                         int(entry["Exit Y Position"]))

            traversal_cost = tuple(entry["Traversal Cost"])
            reward_cost = tuple(entry["Reward Cost"])
            reward = tuple(entry["Reward"])

            logic_lookup[entrance_pair] = LogicData(
                description,
                entrance_pair,
                exit_pair,
                traversal_cost,
                reward_cost,
                reward,
            )
        return logic_lookup

    def __getitem__(self, key_location: tuple):
        """
        Indexing the map logic class requires two arguments for indexing
            node_location: tuple (int, int) (Tile Index Location)
            > logic_entry = logic_table[node_location]
        """
        try:
            logic_entry = self.logic_lookup[key_location]
        except KeyError:
            logic_entry = self.default_logic_entry(key_location)
        return logic_entry

    def reward_lookup(self, search_item: set) -> tuple:
        """
        Provided a reward value to search, will iterate over the
        map_logic and return a the tile value if the reward search
        matches the lookup logic
        """
        if search_item == set(['|']):
            return (None,)

        search_item.discard('|')
        tile_data = []
        for sitem in search_item:
            for tile, logic_entry in self.logic_lookup.items():
                logic_reward = {item for item in logic_entry.reward}
                if sitem in logic_reward:
                    tile_data.append(tile)
        return tuple(tile_data)
