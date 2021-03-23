#!/usr/bin/env python3

"""
PathProcessor:
Implements the floodfill and pathfinding algorithms with desired path combinations
"""

import copy
import operator

import z2p.RomMap as RomMap
from z2p.Tile import TileGraph, TileNode, TilePath

import matplotlib.pyplot as plt
import matplotlib as mpl


class PathProcessor:
    def __init__(self, tileGraph: TileGraph):
        self.tileGraph = tileGraph
        self.keyTile = set()
        for tile in tileGraph._tileParser._graphLogicDict.keys():
            if (
                len(tileGraph[tile].logic.reward) != 1
                or "|" not in tileGraph[tile].logic.reward
            ):
                self.keyTile.add(tile)
        self.globalInventory = set(["|"])

    def pathfind(self, initialStartTile: tuple):
        regionPaths = []

        # Initialize the search space
        (regionStack, linkMap) = self._exploreRegion(initialStartTile)
        regionKeys = set(self.keyTile) & set(regionStack)
        localPaths = self._constructPaths(initialStartTile, regionKeys, linkMap)
        tilePaths = self._formTilePaths(localPaths)

        doneIndex = []
        allPaths = []
        allPaths.extend(tilePaths)

        # Iteratively form path combinations
        # PathProcessor.viewPath(startTilePath, regionKeys)
        while len(tilePaths) > 0:
            startTilePath = tilePaths.pop(0)
            startTile = startTilePath.collection[-1]
            keySubSet = set.difference(regionKeys, startTilePath.keySet)
            (_, linkMap) = self._exploreRegion(startTile)
            localPaths = self._constructPaths(startTile, keySubSet, linkMap)
            localTilePaths = self._formTilePaths(localPaths)

            for localSubPath in localTilePaths:
                copyPath = copy.deepcopy(startTilePath)
                copyPath.concatenate(
                    localSubPath, self.tileGraph._tileParser._ITEM_VALUE_LOOKUP
                )
                tilePaths.append(copyPath)
                allPaths.append(copyPath)

        for tpath in allPaths:
            if self.tileGraph[tpath.pathEnd].background == "Palace":
                regionPaths.append(tpath)
        return (regionStack, regionPaths)

    def _formTilePaths(self, regionPaths: list):
        initialTilePaths = []
        for pcollection in regionPaths:
            basePath = TilePath(
                pcollection,
                self.tileGraph,
                self.tileGraph._tileParser._ITEM_VALUE_LOOKUP,
            )
            initialTilePaths.append(basePath)
        rankSortPaths = self._sortPaths(initialTilePaths)
        return rankSortPaths

    def _exploreRegion(self, startTile: tuple):
        searchStack = [startTile]
        regionStack = []
        linkMap = dict()
        linkMap[startTile] = None

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
                    if tcost.issubset(self.globalInventory):
                        searchStack.append(edgeNode)
                        linkMap[edgeNode] = searchNode
        return (regionStack, linkMap)

    def _constructPaths(self, startTile: tuple, keySet: set, linkMap: dict):
        localPaths = []
        for key in keySet:
            lPath = []
            tilePtr = key
            while tilePtr != startTile:
                lPath.append(tilePtr)
                tilePtr = linkMap[tilePtr]
            lPath.append(startTile)
            lPath.reverse()
            localPaths.append(lPath)
        return localPaths

    def _sortPaths(self, regionPaths: list):
        regionPaths.sort(key=operator.attrgetter("rank"))
        return regionPaths

    @staticmethod
    def viewPath(tPath: TilePath, keySet: set):
        plt.figure()
        (keyY, keyX) = zip(*keySet)
        (pathY, pathX) = zip(*tPath.collection)
        plt.scatter(keyX, keyY)
        plt.scatter(pathX, pathY)
        plt.gca().invert_yaxis()
        plt.show()
