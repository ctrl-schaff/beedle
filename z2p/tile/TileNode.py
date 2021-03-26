#!/usr/bin/env python3

"""
TileNode:
    Data structure for storing concepts related to the tile properties
"""

from dataclasses import dataclass
import z2p.tile.TileLogic as TileLogic


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
