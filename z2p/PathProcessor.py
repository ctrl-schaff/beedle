#!/usr/bin/env python3

"""
PathProcessor:
Implements the floodfill and pathfinding algorithms with desired path combinations
"""

import copy
import operator

import matplotlib.pyplot as plt
import matplotlib as mpl

import z2p.RomMap as RomMap
from z2p.tile.TileGraph import TileGraph
from z2p.tile.TileNode import TileNode
from z2p.tile.TilePath import TilePath


class PathProcessor:
    def __init__(self, tileGraph: TileGraph):
        self.tileGraph = tileGraph
        self.keyTile = set()
        for tile in tileGraph.tileParser.graphLogicDict.keys():
            if (
                len(tileGraph[tile].logic.reward) != 1
                or "|" not in tileGraph[tile].logic.reward
            ):
                self.keyTile.add(tile)
        self.globalInventory = set(["|"])

    def pathfind(self, startTile: tuple):
        self.regionData = []
        self.pathData = []
        for pregion in range(2):
            (regionKeys, tilePaths, startTile) = self._initializeSearchSpace(startTile)
            self._searchRegionSpace(tilePaths, regionKeys)

    def _initializeSearchSpace(self, initialStartTile: tuple):
        (regionStack, linkMap) = self._exploreRegion(initialStartTile)
        regionKeys = set(self.keyTile) & set(regionStack)
        localPaths = self._constructPaths(initialStartTile, regionKeys, linkMap)
        tilePaths = self._formTilePaths(localPaths)

        self.linkMaps = {initialStartTile: linkMap}
        endTile = (None, None)
        for keyTile in regionKeys:
            (_, linkMap) = self._exploreRegion(keyTile)
            self.linkMaps[keyTile] = linkMap

            if self.tileGraph[keyTile].background == "Palace":
                newStartTile = keyTile

        self.regionData.append(regionStack)

        return (regionKeys, tilePaths, newStartTile)

    def _searchRegionSpace(self, tilePaths: list, regionKeys: set):
        allPaths = []
        regionPaths = []
        while len(tilePaths) > 0:
            startTilePath = tilePaths.pop(0)
            startTile = startTilePath.collection[-1]
            keySubSet = set.difference(regionKeys, startTilePath.keySet)
            localPaths = self._constructPaths(
                startTile, keySubSet, self.linkMaps[startTile]
            )
            localTilePaths = self._formTilePaths(localPaths)

            for localSubPath in localTilePaths:
                copyPath = copy.deepcopy(startTilePath)
                copyPath.concatenate(
                    localSubPath, self.tileGraph.tileParser.lookupTable
                )
                tilePaths.append(copyPath)
                allPaths.append(copyPath)

        for tpath in allPaths:
            if self.tileGraph[tpath.pathEnd].background == "Palace":
                regionPaths.append(tpath)

        self.pathData.append(self._sortPaths(regionPaths))
        self.globalInventory.update(regionPaths[0].inventory)

    def _formTilePaths(self, regionPaths: list):
        initialTilePaths = []
        for pcollection in regionPaths:
            basePath = TilePath(
                pcollection,
                self.tileGraph,
                self.tileGraph.tileParser.lookupTable,
            )
            initialTilePaths.append(basePath)
        return initialTilePaths

    def _exploreRegion(self, startTile: tuple):
        searchStack = [startTile]
        localStack = []
        linkMap = dict()
        linkMap[startTile] = None

        while len(searchStack) > 0:
            searchNode = searchStack.pop(0)
            tileNode = self.tileGraph[searchNode]
            localStack.append(searchNode)
            for edgeNode in tileNode.edges:
                if (
                    edgeNode not in localStack
                    and edgeNode not in searchStack
                    and edgeNode not in linkMap
                ):
                    tcost = self.tileGraph[edgeNode].logic.traversalCost
                    if tcost.issubset(self.globalInventory):
                        searchStack.append(edgeNode)
                        linkMap[edgeNode] = searchNode

        return (localStack, linkMap)

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
        regionPaths.sort(key=operator.attrgetter("rank"), reverse=True)
        return regionPaths
