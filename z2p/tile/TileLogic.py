#!/usr/bin/env python3

"""
TileLogic:
    - Data structure for holding information on cost and reward
"""

from dataclasses import dataclass


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
