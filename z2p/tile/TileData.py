#!/usr/bin/env python3

"""
TileData
Handler for parsing and importing the map specific tile data for key locations and items
"""


class TileData:
    def __init__(self, configFile: str = None):

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

        _UPGRADES = {
            "Heart1": 100,
            "Heart2": 100,
            "Heart3": 100,
            "Heart4": 100,
            "Magic1": 100,
            "Magic2": 100,
            "Magic3": 100,
            "Magic4": 100,
        }

        _MAGIC = {
            "Shield": 10,
            "Jump": 1000,
            "Life": 100,
            "Fairy": 1000,
            "Fire": 10,
            "Reflect": 1000,
            "Spell": 1000,
            "Thunder": 1000,
        }

        _QUEST_ITEMS = {
            "Trophy": 1000,
            "BaguNote": 1000,
            "LifeWater": 1000,
            "LostChild": 1000,
            "MagicalKey": 1000,
        }

        _DUNGEON_ITEMS = {
            "Candle": 100,
            "Hammer": 1000,
            "Gloves": 1000,
            "Raft": 1000,
            "Boots": 1000,
            "Flute": 1000,
            "Cross": 1000,
        }

        _CRYSTALS = {
            "Crystal1": 1000,
            "Crystal2": 1000,
            "Crystal3": 1000,
            "Crystal4": 1000,
            "Crystal5": 1000,
            "Crystal6": 1000,
        }

        self._ITEM_VALUE_LOOKUP = {"|": 0}
        self._ITEM_VALUE_LOOKUP.update(_UPGRADES)
        self._ITEM_VALUE_LOOKUP.update(_MAGIC)
        self._ITEM_VALUE_LOOKUP.update(_QUEST_ITEMS)
        self._ITEM_VALUE_LOOKUP.update(_DUNGEON_ITEMS)
        self._ITEM_VALUE_LOOKUP.update(_CRYSTALS)
