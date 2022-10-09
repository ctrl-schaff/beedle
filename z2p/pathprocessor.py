"""
PathProcessor:
Implements the floodfill and pathfinding algorithms with desired path
combinations
"""

import treelib

import z2p.tilepath


class PathProcessor:
    """
    Class for handling the main pathfind algorithm
    """

    def __init__(self, tile_graph, map_logic, map_item):
        self.global_inventory = set(["|"])
        self.link_maps = {}
        self.region_data = []
        self.path_data = []

        self.tile_graph = tile_graph

        self.key_tile = map_logic.logic_tile
        self.map_item = map_item

    def initialize_search_space(self, initial_start_tile: tuple):
        """
        1) Performs a flood-fill of the region given the initialize starting
        tile and returns a region stack and link map for the corresponding
        2) Does a set intersection between the known key tiles from the logic
        and the region tiles to determine what region keys exists in the
        explorable region
        3) Using the A* algorithm and the calculated link maps from the
        flood-fill, we can calculate a path to all local region keys from
        the initial_start_tile
        """

        region_stack = self.explore_region(initial_start_tile)
        self.region_data.append(region_stack)

        region_keys = set(self.key_tile) & set(region_stack)

        initial_start_node = self.tile_graph[initial_start_tile]
        localpaths = self.construct_paths(initial_start_node, region_keys)
        tile_paths = self.form_tile_paths(localpaths)

        for key_tile in region_keys:
            self.explore_region(key_tile)

        return (region_keys, tile_paths)

    def search_region_space(self, tile_paths: list, region_keys: set):
        """
        Expands on the initial collection of paths to explore all potential
        combinations possible

        Takes the subset of already
        """

        subtrees = []
        for node in region_keys:
            path_start = self.tile_graph[node]
            localpaths = self.construct_paths(path_start, region_keys)
            local_tile_paths = self.form_tile_paths(localpaths)
            pathtree = treelib.Tree()
            pathtree.create_node(identifier=path_start)
            for local_subpath in local_tile_paths:
                tag_str = (
                    f"{local_subpath.path_start.description} -> "
                    f"{local_subpath.path_end.description}"
                )
                pathtree.create_node(
                    tag=tag_str,
                    identifier=local_subpath.path_end,
                    parent=local_subpath.path_start,
                    data=local_subpath,
                )
                tile_paths.append(local_subpath)
            subtrees.append(pathtree)
        return subtrees

    def form_tile_paths(self, region_paths: list):
        """
        Wrapper around the TilePath class given a list of accumulated
        region paths
        """
        tile_paths = []
        for pcollection in region_paths:
            base_path = z2p.tilepath.TilePath(pcollection, self.map_item)
            tile_paths.append(base_path)
        return tile_paths

    def construct_paths(self, start_node, key_set: set):
        """
        Main path formation algorithm associated with A*
        """
        localpaths = []
        start_coord = start_node.location
        link_map = self.link_maps[start_coord]
        for key in key_set:
            lpath = []
            tile_ptr = key
            while tile_ptr != start_coord:
                lpath.append(self.tile_graph[tile_ptr])
                tile_ptr = link_map[self.tile_graph[tile_ptr]]
            lpath.append(start_node)
            lpath.reverse()
            if lpath[0] != lpath[-1]:
                localpaths.append(lpath)
        return localpaths
