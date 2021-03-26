#!/usr/bin/env python3

"""
Miscellaneous utilities
"""

import itertools
import operator

import numpy as np
import matplotlib.pyplot as plt

import z2p.tile.TilePath as TilePath


def getNeighbors(node: tuple):
    return [
        tuple(map(operator.add, node, move))
        for move in ((1, 0), (-1, 0), (0, 1), (0, -1))
    ]


def manhattanDistance(node1: tuple, node2: tuple):
    return np.abs(node1[0] - node2[0]) + np.abs(node1[1] - node2[1])


# Collect data into fixed-length chunks or blocks
def chunker(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def viewPath(tPath: TilePath, keySet: set):
    plt.figure()
    (keyY, keyX) = zip(*keySet)
    (pathY, pathX) = zip(*tPath.collection)
    plt.scatter(keyX, keyY)
    plt.scatter(pathX, pathY)
    plt.gca().invert_yaxis()
    plt.show()
