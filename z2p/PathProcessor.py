#!/usr/bin/env python3


"""
PathProcessor:
Implements the floodfill and pathfinding algorithms while desired path combinations
"""

import copy

import z2p.RomMap as RomMap
from z2p.Tile import TileGraph


class PathProcessor:
    def __init__(self, startTile: tuple, tileGraph: TileGraph):
        self._startTile = startTile
        self.tileGraph = tileGraph
        self.keyTile = tileGraph._tileParser._graphLogicDict.keys()

        self.inventory = set("|")
        self.pathData = []

    def pathfind(self):
        regionKeys = []
        regionPaths = []

        regionStack, linkMap = self._exploreRegion()
        for key_pos in self.keyTile:
            if key_pos in regionStack:
                localPath = self._constructPath(key_pos, linkMap)
                regionPaths.append(localPath)
        regionPaths.pop(0)
        return (regionStack, regionPaths)

    def _exploreRegion(self):
        searchStack = [self._startTile]
        regionStack = []
        linkMap = dict()
        linkMap[self._startTile] = None

        while len(searchStack) > 0:
            searchNode = searchStack.pop(0)
            tileNode = self.tileGraph[searchNode]
            regionStack.append(searchNode)
            for edgeNode in tileNode.edges:
                if (
                    edgeNode not in regionStack
                    and edgeNode not in searchStack
                    and edgeNode not in linkMap
                ):
                    tcost = self.tileGraph[edgeNode].logic.traversalCost
                    if tcost.issubset(self.inventory):
                        searchStack.append(edgeNode)
                        linkMap[edgeNode] = searchNode
        return (regionStack, linkMap)

    def _constructPath(self, keyPos: tuple, linkMap: dict):
        localPath = []
        tilePtr = keyPos
        while tilePtr != self._startTile:
            localPath.append(tilePtr)
            tilePtr = linkMap[tilePtr]
        localPath.append(self._startTile)
        localPath.reverse()
        return localPath
