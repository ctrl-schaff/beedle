#!/usr/bin/env python3

"""
Test Methods for exploring the graph generation from map data
"""


import z2p.graph
import z2p.map_item
import z2p.map_data
import z2p.map_logic
import z2p.map_tile
import z2p.pathprocessor
import z2p.structure

from z2p import TileGraph




def test_graph_generation():
    '''
    Attempts to generate the graph logic
    from the zelda 2 map 
    '''
    
    romfile = z2p.structure.config_file_str("zelda2.nes")
    tilespec = z2p.structure.config_file_str("zelda2tiles.conf")
    logicspec = z2p.structure.config_file_str("zelda2logic.conf")
    itemspec = z2p.structure.config_file_str("zelda2items.conf")

    map_obj = z2p.map_data.RomMap(romfile)

    tiledata = z2p.map_tile.MapTileData(tilespec)
    logicdata = z2p.map_logic.MapLogicData(logicspec, tiledata, map_obj)
    itemdata = z2p.map_item.MapItemData(itemspec)

    graph_obj = z2p.graph.TileGraph(map_obj, logicdata, tiledata)
    graph_start = (23, 22)
    graph_end = (69, 43)
    path_proc = graph_obj.process_graph(graph_start,
                                        graph_end,
                                        logicdata,
                                        itemdata)
