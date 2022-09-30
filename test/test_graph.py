#!/usr/bin/env python3

"""
Test Methods for exploring the graph generation from map data
"""


from z2p import TileGraph


def test_graph_generation(z2_map_data, configuration):
    """
    Attempts to generate the graph logic from the zelda 2 map
    """

    item_data = configuration.get("items", None)
    tile_data = configuration.get("tiles", None)
    location_data = configuration.get("locations", None)

    graph_obj = TileGraph(z2_map_data, location_data, tile_data)
    # graph_start = (23, 22)
    # graph_end = (69, 43)
    # path_proc = graph_obj.process_graph(graph_start,
    #                                     graph_end,
    #                                     logicdata,
    #                                     itemdata)
