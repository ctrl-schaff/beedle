#!/usr/bin/env python3

"""
TilePath:
Collection of TileNodes representing a path

Output result from path processor

"""


class TilePath:
    """
    Class sequence for representing a collection of tiles derived from
    one location on the map to another
    """

    def __init__(self, pathData: list, itemdata):
        self.collection = pathData
        self.path_start = self.collection[0]
        self.path_end = self.collection[-1]
        self.itemdata = itemdata

        self.inventory = set(["|"])
        self.key_data = set([self.path_start, self.path_end])

        self.__update_inventory()

    def __update_inventory(self):
        for key_tile in self.key_data:
            reward_cost = set(key_tile.reward_cost)
            if reward_cost.issubset(self.inventory):
                for rewarditem in key_tile.reward:
                    self.inventory.add(rewarditem)

    def __iadd__(self, other_path):
        if self.path_end == other_path.path_start:
            other_path.collection.pop(0)
            self.collection.extend(other_path.collection)
            self.path_end = self.collection[-1]

            self.inventory.update(other_path.inventory)
            self.key_data.update(other_path.key_data)
        return self

    def __repr__(self) -> str:
        path_view = [self.collection[0], self.collection[-1]]
        col_str = "{" + " ".join(map(str, path_view)) + "}"
        fstr = "\nSCORE:{0:d}\nLENGTH:{1:d}\nCOLLECTION:{2:s}"
        return fstr.format(col_str)
