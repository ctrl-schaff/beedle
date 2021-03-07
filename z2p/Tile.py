#!/usr/bin/env python3

"""
Tile:
Handles the map tile data and associated properties
    - Internal TileNode data structure stores concepts related to the tile edges
    - TileNode has the TileLogic data structures for determining games rewards and costs
    - TileParser is the class that manipulates the TileNode and stores game logic 
    - TileGraph stores a collection of TileData objects created through the TileParser
"""

from dataclasses import dataclass
import os
import shlex
import sys

import numpy as np

import z2p.RomMap as RomMap
import z2p.utility as util


@dataclass
class TileLogic:
    traversalCost: frozenset = frozenset(["|"])
    rewardCost: frozenset = frozenset(["|"])
    reward: frozenset = frozenset(["|"])

    def __repr__(self) -> str:
        tcost_str = "{" + " ".join(map(str, self.traversalCost)) + "}"
        rcost_str = "{" + " ".join(map(str, self.rewardCost)) + "}"
        reward_str = "{" + " ".join(map(str, self.reward)) + "}"
        fstr = "\nTRAVERSE COST:{0:s}\nREWARD COST:{1:s}\nREWARD:{2:s}"
        return fstr.format(tcost_str, rcost_str, reward_str)


@dataclass
class TileNode:
    identifier: int
    location: tuple
    background: str
    symbol: str
    color: str
    description: str
    logic: TileLogic
    edges: frozenset

    def __repr__(self) -> str:
        edge_str = "{" + " ".join(map(str, self.edges)) + "}"
        fstr = "\nTILE:[{0:d},{1:d}]\nTYPE:{2:s}\nDESC:{3:s}\nEDGE:{4:s}"
        return fstr.format(*self.location, self.background, self.description, edge_str)


class TileGraph(list):
    def __init__(self, romMap: RomMap, keypath: str):
        self.tileMap = []
        self._tileParser = TileParser(keypath, romMap.mapData)
        self._formTileMap(romMap)

    def _formTileMap(self, romMap: RomMap):
        for ri in range(romMap.MAP_SIZE_X):
            tileRow = []
            for ci in range(romMap.MAP_SIZE_Y):
                thisTile = (ri, ci)
                tileID = romMap.mapData[thisTile]
                baseCost = self._tileParser._calcBaseTileCost(tileID)
                tileNode = self._tileParser.createTileNode(
                    thisTile, tileID, baseCost, romMap.mapData
                )
                tileRow.append(tileNode)
            self.tileMap.append(tileRow)

    def __getitem__(self, index: tuple):
        if isinstance(index, tuple):
            return self.tileMap[index[0]][index[1]]
        else:
            return super().__getitem__(index)


class TileParser:
    def __init__(self, keypath: str, mapdata: np.array):
        self.TILE_SYMBOL = (
            "T",
            "C",
            "P",
            "B",
            "D",
            "G",
            "F",
            "S",
            "Y",
            "R",
            "V",
            "M",
            "W",
            "E",
            "O",
            "A",
            "*",
            "^",
        )

        self.TILE_TYPE = (
            "Town",
            "Cave",
            "Palace",
            "Bridge",
            "Desert",
            "Grassland",
            "Forest",
            "Swamp",
            "Graveyard",
            "Road",
            "Volcanic",
            "Mountain",
            "Ocean",
            "Water",
            "Boulder",
            "Monster",
            "FILL",
            "PATH",
        )

        self.TILE_COLOR = (
            "#747474",
            "#000000",
            "#efefef",
            "#f0bc3c",
            "#fabcb0",
            "#80D010",
            "#009400",
            "#386138",
            "#fcfcfc",
            "#ffbc3c",
            "#c84c0c",
            "#634536",
            "#3cbcfc",
            "#85d5ff",
            "#dc7e4f",
            "#ff6def",
            "#ccfdff",
            "#f31616",
        )

        _UPGRADES = (
            "Heart1",
            "Heart2",
            "Heart3",
            "Heart4",
            "Magic1",
            "Magic2",
            "Magic3",
            "Magic4",
        )

        _MAGIC = (
            "Shield",
            "Jump",
            "Life",
            "Fairy",
            "Fire",
            "Reflect",
            "Spell",
            "Thunder",
        )

        _QUEST_ITEMS = ("Trophy", "BaguNote", "LifeWater", "LostChild", "MagicalKey")

        _DUNGEON_ITEMS = (
            "Candle",
            "Hammer",
            "Glove",
            "Raft",
            "Boots",
            "Flute",
            "Cross",
        )

        _CRYSTALS = (
            "Crystal1",
            "Crystal2",
            "Crystal3",
            "Crystal4",
            "Crystal5",
            "Crystal6",
        )

        self._ITEM_VALUE_LOOKUP = ["|"]
        self._ITEM_VALUE_LOOKUP.extend(_UPGRADES)
        self._ITEM_VALUE_LOOKUP.extend(_MAGIC)
        self._ITEM_VALUE_LOOKUP.extend(_QUEST_ITEMS)
        self._ITEM_VALUE_LOOKUP.extend(_DUNGEON_ITEMS)
        self._ITEM_VALUE_LOOKUP.extend(_CRYSTALS)
        self._ITEM_VALUE_LOOKUP = frozenset(self._ITEM_VALUE_LOOKUP)

        self._graphLogicDict = {}

        if os.path.isfile(keypath) and os.path.exists(keypath):
            self._importGraphLogicData(os.path.abspath(keypath), mapdata)
        else:
            sys.exit("Invalid rom file path{0:s}".format(os.path.abspath(keypath)))

    def createTileNode(self, tile_loc: tuple, tid: int, baseCost: str, mapdata: RomMap):

        baseTraversalCost = self._calcBaseTileCost(tid)
        (desc, logicData, logicEdge) = self._graphLogicDict.get(
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
            self.TILE_TYPE[tid],
            self.TILE_SYMBOL[tid],
            self.TILE_COLOR[tid],
            desc,
            logicData,
            frozenset(tileEdges),
        )

    def _formTileEdges(self, location: tuple, logicEdge: tuple, mapdata: np.array):

        adjEdges = util.getNeighbors(location)
        (mapx, mapy) = mapdata.shape
        edges = [
            edge
            for edge in adjEdges
            if (edge[0] >= 0 and edge[0] < mapx)
            and (edge[1] >= 0 and edge[1] < mapy)
            and self.TILE_SYMBOL[mapdata[edge]] not in ("W", "M")
        ]

        if logicEdge not in edges and logicEdge is not None:
            edges.append(logicEdge)
        return edges

    def _importGraphLogicData(self, keyfile: str, mapdata: np.array):
        with open(keyfile, "r") as kf:
            for line in kf:
                graphLogicList = shlex.split(line.strip("\n"))
                self._parseEdgeLogic(graphLogicList, mapdata)

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

        baseCost = self._calcBaseTileCost(mapdata[tileKey])
        if baseCost not in traversalCost:
            traversalCost.append(baseCost)

        description = edgeLogic[0]
        logicData = TileLogic(
            frozenset(traversalCost), frozenset(rewardCost), frozenset(rewardItems)
        )
        self._graphLogicDict[tileKey] = (description, logicData, logicEdge)

    def _calcBaseTileCost(self, tid: int):
        tileCost = "|"
        if self.TILE_SYMBOL[tid] == "O":
            tileCost = "Hammer"
        elif self.TILE_SYMBOL[tid] == "E":
            tileCost = "Boots"
        elif self.TILE_SYMBOL[tid] == "A":
            tileCost = "Flute"
        return tileCost
