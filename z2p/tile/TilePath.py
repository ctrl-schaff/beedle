#!/usr/bin/env python3

"""
TilePath:

"""

import z2p.tile.TileGraph as TileGraph


class TilePath:
    def __init__(self, pathData: list, tGraph: TileGraph, lookupTable: dict):
        self.collection = pathData
        self.pathStart = self.collection[0]
        self.pathEnd = self.collection[-1]

        self.inventory = set(["|"])
        self.keySet = set([self.pathStart, self.pathEnd])

        self._updateInventory(tGraph, lookupTable)
        self._calcRank(lookupTable)

    def concatenate(self, tPath, lookupTable: dict):
        if self.pathEnd == tPath.pathStart:
            tPath.collection.pop(0)
            self.collection.extend(tPath.collection)
            self.pathEnd = self.collection[-1]

            self.inventory.update(tPath.inventory)
            self.keySet.update(tPath.keySet)

            self._calcRank(lookupTable)

    def _updateInventory(self, tGraph: TileGraph, lookupTable: dict):
        for keyTile in self.keySet:
            rewardCost = set([rC for rC in tGraph[keyTile].logic.rewardCost])
            if rewardCost.issubset(self.inventory):
                for rewarditem in tGraph[keyTile].logic.reward:
                    self.inventory.add(rewarditem)

    def _calcRank(self, lookupTable: dict):
        score = 0
        for item in self.inventory:
            score += lookupTable[item]
        self.rank = [score, len(self.collection)]

    def __repr__(self) -> str:
        col_str = "{" + " ".join(map(str, self.collection)) + "}"
        fstr = "\nSCORE:{0:d}\nLENGTH:{1:d}\nCOLLECTION:{2:s}"
        return fstr.format(self.rank[0], self.rank[1], col_str)
