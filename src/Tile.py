#!/usr/bin/env python3

"""
Tile:
Handles the properties associated with map tiles
    - Internal TileData data structure stores concepts related to the tile edges
    and also the game logic for traversing certain tiles 
    - TileProcessor is the class that manipulates the TileData and parses a lot of the 
    game logic 
    - RomMap stores a collection of TileData objects created through the TileProcessor
"""

import os
import shlex
import sys
import typing

class TileData(typing.NamedTuple):
    location: tuple
    background: str 
    edge: frozenset
    traversalCost: frozenset
    rewardCost: frozenset
    reward: frozenset
    identifier: int
    symbol: str
    color: str
    description: str
    
    def __repr__(self) -> str:
        tcost_str = '{' + ' '.join(map(str, self.traversalCost)) + '}'
        rcost_str = '{' + ' '.join(map(str, self.rewardCost)) + '}'
        reward_str = '{' + ' '.join(map(str, self.reward)) + '}'
        edge_str = '{' + ' '.join(map(str, self.edge)) + '}'
        fstr = "\nTILE:[{0:d},{1:d}]\nTYPE:{2:s}\nTRAVERSE COST:{3:s}\nREWARD COST:{4:s}\nREWARD:{5:s}\nEDGE:{6:s}\n"
        return fstr.format(*self.location, self.background,
            tcost_str, rcost_str, reward_str, edge_str)

class TileProcessor:
    def __init__(self, keypath:str):
        self.TILE_SYMBOL = ('T', 'C', 'P', 'B',
            'D', 'G', 'F', 'S', 'Y', 'R', 'V', 'M',
            'W', 'E', 'O', 'A', '*')

        self.TILE_TYPE = ('Town', 'Cave', 'Palace', 'Bridge', 'Desert',
            'Grassland', 'Forest', 'Swamp', 'Graveyard', 'Road', 'Volcanic',
            'Mountain', 'Ocean', 'Water', 'Boulder', 'Monster', 'PATH')

        self.TILE_COLOR = ('#747474', '#000000', '#efefef', '#f0bc3c',
            '#fabcb0', '#80D010', '#009400', '#386138', '#fcfcfc', '#ffbc3c',
            '#c84c0c', '#634536', '#3cbcfc', '#85d5ff', '#dc7e4f', '#237849',
            )

        _UPGRADES = ("Heart1", "Heart2", "Heart3", "Heart4", \
            "Magic1", "Magic2", "Magic3", "Magic4") 

        _MAGIC = ("Shield", "Jump", "Life", "Fairy", \
            "Fire", "Reflect", "Spell", "Thunder") 

        _QUEST_ITEMS = ("Trophy", "BaguNote", "LifeWater", "LostChild", "MagicalKey")
    
        _DUNGEON_ITEMS = ("Candle", "Hammer", "Glove", "Raft", \
            "Boots", "Flute", "Cross")

        _CRYSTALS = ("Crystal1", "Crystal2", "Crystal3", \
            "Crystal4", "Crystal5", "Crystal6")

        self._ITEM_VALUE_LOOKUP = ['|']
        self._ITEM_VALUE_LOOKUP.extend(_UPGRADES) 
        self._ITEM_VALUE_LOOKUP.extend(_MAGIC)
        self._ITEM_VALUE_LOOKUP.extend(_QUEST_ITEMS) 
        self._ITEM_VALUE_LOOKUP.extend(_DUNGEON_ITEMS) 
        self._ITEM_VALUE_LOOKUP.extend(_CRYSTALS) 
        self._ITEM_VALUE_LOOKUP = frozenset(self._ITEM_VALUE_LOOKUP)

        self._graphLogicDict = {}

        if os.path.isfile(keypath) and os.path.exists(keypath):
            self._importGraphLogicData(os.path.abspath(keypath))
        else:
            sys.exit("Invalid rom file path{0:s}".format(os.path.abspath(keypath)))

    def _importGraphLogicData(self, keyfile:str):
        with open(keyfile, 'r') as kf:
            for line in kf:
                graphLogicList = shlex.split(line.strip('\n'))    
                self._parseEdgeLogicLine(graphLogicList)
    
    def _parseEdgeLogicLine(self, edgeLogic:list):
        tileKey = (int(edgeLogic[2]), int(edgeLogic[1])) 
        
        # Check if additional edge exists due to game logic
        if edgeLogic[1] == edgeLogic[5] and edgeLogic[2] == edgeLogic[6]:
            tileEdge = None
        else:
            tileEdge = (int(edgeLogic[6]), int(edgeLogic[5]))
        
        # Parse edge reward
        tileRewardsLogic = edgeLogic[4].split('>')
        tileRewardCost = tileRewardsLogic[0].split('+')
        tileRewardItems = tileRewardsLogic[1].split('+')
            
        # Parse edge traversal cost
        tileTraversalCost = edgeLogic[3].split('+')
        
        tileParseResults = (edgeLogic[0], tileKey, tileTraversalCost, \
            tileRewardCost, tileRewardItems, tileEdge)
        self._graphLogicDict[tileKey] = tileParseResults 

    def tileLookup(self, tile_loc:tuple, tid:int, tile_edge:dict):
        edges = [edge for edge, val in tile_edge.items() 
            if self.TILE_SYMBOL[val] not in ('W', 'M')]

        try:
            edgeLogic = self._graphLogicDict[tile_loc]
        except KeyError as ke:
            edgeLogic = ('Generic Tile', tile_loc, ['|'], ['|'], ['|'], None)

        baseTraversalCost = self._calcBaseTileCost(tid)
        if baseTraversalCost is not None:
            edgeLogic[2].append(baseTraversalCost)

        tileDescription = edgeLogic[0]
        tileTraversalCost = edgeLogic[2] 
        tileRewardCost = edgeLogic[3]
        tileReward = edgeLogic[4]
        tileLogicEdge = edgeLogic[5]

        if tileLogicEdge is not None:
            edges.append(tileLogicEdge)
        
        return TileData(tile_loc, \
            self.TILE_TYPE[tid], \
            frozenset(edges), \
            frozenset(tileTraversalCost), \
            frozenset(tileRewardCost), \
            frozenset(tileReward), \
            tid, \
            self.TILE_SYMBOL[tid], \
            self.TILE_COLOR[tid], \
            tileDescription)

    def _calcBaseTileCost(self, tid:int):
        tileCost = None
        if self.TILE_SYMBOL[tid] == 'O':
            tileCost = 'Hammer'
        elif self.TILE_SYMBOL[tid] == 'E':
            tileCost = 'Boots'
        elif self.TILE_SYMBOL[tid] == 'A':
            tileCost = 'Flute'
        return tileCost
