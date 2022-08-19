#!/usr/bin/env python3 

"""
Cython flood fill algorithm
Flood fill algorithm to explore entire possible region discoverable
Given two stacks (using lists)
    > local_stack
        Collection of search_nodes popped from the search_stack
    > search_stack
        Collection of tiles accumulated while traversing the graph.
        Nodes are appended to the end of this stack if the current
        search_node popped from the top are traversable (the global
        inventory passes the traversal cost)
        These nodes are added by examining the edges for each node
        in the graph
"""


cpdef (list, dict) explore_region(tile_graph,
                                  global_inventory: set,
                                  start_coord: tuple):
    cdef list search_stack = [start_coord]
    cdef list local_stack = []
    cdef dict link_map = dict()

    # self.link_maps[start_coord] = link_map
    link_map[self.tile_graph[start_coord]] = None

    while len(search_stack) > 0:
        search_coord = search_stack.pop(0)
        local_stack.append(search_coord)

        tile_node = self.tile_graph[search_coord]
        for edge_coord in tile_node.edges:
            if (edge_coord not in local_stack and
                    edge_coord not in search_stack):
                tcost = set(self.tile_graph[edge_coord].traversal_cost)
                if tcost.issubset(self.global_inventory):
                    search_stack.append(edge_coord)
                    link_map[self.tile_graph[edge_coord]] = search_coord
    return local_stack
