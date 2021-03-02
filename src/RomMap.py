#!/usr/bin/env python3

"""
RomMap:
Handles the importation of the rom map data  
"""

import os
import sys

import numpy as np

import Tile
import utility
import Visualization

class RomMap():
    def __init__(self, rompath, keypath):
        
        self.MAP_SIZE_X = 75        
        self.MAP_SIZE_Y = 65 
        self.MAP_BOUNDARY = { 
            'WEST_HYRULE':(int("506C", 16), int('538C', 16)),
            'DEATH_MOUNTAIN':(int("665C", 16), int('6942', 16)),    
            'EAST_HYRULE':(int("9056", 16), int('936F', 16)),
            'MAZE_ISLAND':(int("A65C", 16), int('A942', 16))  
        } 

        self._subMapData = []
        self.mapData = np.zeros([2*self.MAP_SIZE_X, 2*self.MAP_SIZE_Y], dtype=np.int)
        self.tileMap = []

        if os.path.isfile(rompath) and os.path.exists(rompath):
            self.romdata = os.path.abspath(rompath) 
        else:
            sys.exit("Invalid rom file path{0:s}".format(os.path.abspath(rompath)))

        self._tileProcessor = Tile.TileProcessor(keypath)
        self._extractMapData()

        self._formatMapData()
        self._formTileMap()


    def _extractMapData(self):
        with open(self.romdata, 'rb+') as romfile:
            for mapbound in self.MAP_BOUNDARY.values():
                romfile.seek(mapbound[0])
                numMapBytes = (mapbound[1] - mapbound[0]) + 1
                mapByteChunk = romfile.read(numMapBytes).hex()

                subMap = []
                for byte in utility.chunker(mapByteChunk, 2, fillvalue='0'):
                    subMap += (int(byte[0], 16) + 1) * [int(byte[1], 16)]

                # Vertical water barrier to separate sub maps
                for index in range(self.MAP_SIZE_Y, len(subMap), self.MAP_SIZE_Y):
                    subMap.insert(index-1, 12)

                self._subMapData.append(np.resize(np.array(subMap), 
                    (self.MAP_SIZE_X, self.MAP_SIZE_Y)))

    def _formatMapData(self):

        # Cleanup the Death Mountain and Maze Island Segments 
        self._subMapData[1][:,28:] = 12
        self._subMapData[1][60:,:] = 12
        self._subMapData[3][:,:28] = 12
        self._subMapData[3][59:,:] = 12  
        
        # Form total map 
        self.mapData[:, :] = np.hstack((
            np.vstack((self._subMapData[0], self._subMapData[1])), 
            np.vstack((self._subMapData[2], self._subMapData[3]))))

    def _formTileMap(self):
        for ri in range(self.MAP_SIZE_X):   
            tileRow = []
            for ci in range(self.MAP_SIZE_Y):
                thisLocation = (ri, ci)
                valid_edges = self.adjTileCheck(thisLocation)
                tileRow.append(self._tileProcessor.tileLookup(thisLocation, 
                    self.mapData[thisLocation], valid_edges))
            self.tileMap.append(tileRow)

    def adjTileCheck(self, location:tuple):
        adj_pos = utility.getNeighbors(location)
        adj_val = [self.mapData[pos] for pos in adj_pos] 

        valid_edges = {} 
        for pos, val in zip(adj_pos, adj_val):
            if (pos[0] >= 0 and pos[0] < 2*self.MAP_SIZE_X) and \
                (pos[1] >= 0 and pos[1] < 2*self.MAP_SIZE_Y):
                valid_edges[pos] = val 
        return valid_edges
