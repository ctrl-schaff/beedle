#!/usr/bin/env python3

"""
TileParser:
Manipulates TileNode data and formats the game logic
"""

import os
import shlex

import numpy as np

import z2p.RomMap as RomMap
import z2p.utility as util

from z2p.tile.TileData import TileData
from z2p.tile.TileNode import TileNode
from z2p.tile.TileLogic import TileLogic


class TileParser:
    def __init__(self, keypath: str, mapdata: np.array):
        self.tileData = TileData()
        self.graphLogicDict = {}
        self.lookupTable = self.tileData._ITEM_VALUE_LOOKUP

        if os.path.isfile(keypath) and os.path.exists(keypath):
            self._importGraphLogicData(os.path.abspath(keypath), mapdata)
        else:
            sys.exit("Invalid rom file path{0:s}".format(os.path.abspath(keypath)))

    def createTileNode(self, tile_loc: tuple, tid: int, baseCost: str, mapdata: RomMap):
        baseTraversalCost = self.calcBaseTileCost(tid)
        (desc, logicData, logicEdge) = self.graphLogicDict.get(
            tile_loc,
            (
                "Generic Tile",
                TileLogic(traversalCost=frozenset([baseTraversalCost])),
                None,
            ),
        )
        tileEdges = self._formTileEdges(tile_loc, logicEdge, mapdata)

        return TileNode(
            tid,
            tile_loc,
            self.tileData.TILE_TYPE[tid],
            self.tileData.TILE_SYMBOL[tid],
            self.tileData.TILE_COLOR[tid],
            desc,
            logicData,
            frozenset(tileEdges),
        )

    def calcBaseTileCost(self, tid: int):
        tileCost = "|"
        if self.tileData.TILE_SYMBOL[tid] == "O":
            tileCost = "Hammer"
        elif self.tileData.TILE_SYMBOL[tid] == "E":
            tileCost = "Boots"
        elif self.tileData.TILE_SYMBOL[tid] == "A":
            tileCost = "Flute"
        return tileCost

    def _formTileEdges(self, location: tuple, logicEdge: tuple, mapdata: np.array):
        adjEdges = util.getNeighbors(location)
        (mapx, mapy) = mapdata.shape
        edges = [
            edge
            for edge in adjEdges
            if (edge[0] >= 0 and edge[0] < mapx)
            and (edge[1] >= 0 and edge[1] < mapy)
            and self.tileData.TILE_SYMBOL[mapdata[edge]] not in ("W", "M")
        ]

        if logicEdge not in edges and logicEdge is not None:
            edges.append(logicEdge)
        return edges

    def _importGraphLogicData(self, keyfile: str, mapdata: np.array):
        with open(keyfile, "r") as kf:
            for line in kf:
                graphLogicList = shlex.split(line.strip("\n"))
                self._parseEdgeLogic(graphLogicList, mapdata)
        self.graphKeys = self.graphLogicDict.keys()

    def _parseEdgeLogic(self, edgeLogic: list, mapdata: np.array):
        # Check if additional edge exists due to game logic
        if edgeLogic[1] == edgeLogic[5] and edgeLogic[2] == edgeLogic[6]:
            logicEdge = None
        else:
            logicEdge = (int(edgeLogic[6]), int(edgeLogic[5]))

        # Parse edge reward
        rewardsLogic = edgeLogic[4].split(">")
        rewardCost = rewardsLogic[0].split("+")
        rewardItems = rewardsLogic[1].split("+")

        # Parse edge traversal cost
        tileKey = (int(edgeLogic[2]), int(edgeLogic[1]))
        traversalCost = edgeLogic[3].split("+")

        baseCost = self.calcBaseTileCost(mapdata[tileKey])
        if baseCost not in traversalCost:
            traversalCost.append(baseCost)

        description = edgeLogic[0]
        logicData = TileLogic(
            frozenset(traversalCost), frozenset(rewardCost), frozenset(rewardItems)
        )
        self.graphLogicDict[tileKey] = (description, logicData, logicEdge)
