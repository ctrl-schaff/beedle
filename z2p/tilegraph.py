"""
TileGraph:
Converting the raw map data into a set of connected nodes in a graph for
traversal purposes data structure for storing the converted
map data with tile information
    - TileGraph stores a collection of TileData objects
"""

import itertools

from loguru import logger
import networkx as nx
import matplotlib.pyplot as plt

from .pathprocessor import PathProcessor
from .tilemap import TileMap
from .tilenode import TileNode
from .tilesearch import PartialTileMap


class TileGraph:
    """
    Graph object for handling the map node connections
    """

    def __init__(
        self,
        graph_start: tuple,
        graph_end: tuple,
        map_data: TileMap,
        location_map: LocationMap,
        tile_table,
    ):
        self.graph_start = graph_start
        self.graph_end = graph_end
        self._tile_graph = dict()

        self._form_tile_graph(map_data, location_map, tile_table)

    def _form_tile_graph(
        self, map_data: TileMap, map_item: LocationMap, tile_table
    ):
        """
        Iteratively explores the map and continually updates the topological
        graph formed from the logic tiles.
        Process:
            > Explore the entire possible region with a given inventory
            > Using the maplogic object, extract the import 'key' tiles
              from the entire possible region
            > Iterate over those found keys and see if the criteria is met
              to obtain the reward
            > If the reward cost is met, update the inventory and add the
              tile to the completed / visited keys set to avoid further
              duplicate processing
            > If the traversal cost is met, update the connections associated
              with that 'key' tile
        End Criteria:
            > Add the graph_end tile point to the completed_keys set
        """
        graph_stages = self.chunks()
        bottlenecks = self.process_stages(map_logic, graph_stages)

        (bn_iter1, bn_iter2) = itertools.tee(bottlenecks.items(), 2)
        bn_iter2.__next__()
        for bn1, bn2 in itertools.zip_longest(bn_iter1, bn_iter2):
            if bn2 and bn1[0]:
                connection_set = set()
                if topo_graph[bn2[0]][0]:
                    for coord in topo_graph[bn2[0]]:
                        connection_set.add(coord)
                connection_set.add(bn1[0])
                topo_graph[bn2[0]] = tuple(connection_set)
        return (topo_graph, graph_stages, bottlenecks)

    def _find_map_chunks(self, stage_limit: int):
        """
        Explore the map in chunks given the constraints provided
        by the configuration. Iterates over the map until the
        graph_end specified in the constructor has been marked as
        completed or we reach the iteration limit set by the
        stage_limit value
        """
        graph_stages = []
        completed_keys = set()
        search_inventory = set()

        stage_count = 0
        while self.graph_end not in completed_keys:
            logger.info("Graph Search Stage #{stage_count} ")
            stage_count += 1

            ptile_map = PartialTileMap(
                tile_map, self.graph_start, search_inventory
            )

            discovered_locations = ptile_map.discovered_locations(location_map)
            stage_locations = discovered_locations.difference(completed_keys)

            graph_stages.append(stage_locations)
            for loc in stage_locations:
                rcost = set([*map_data[loc].reward_cost])
                tcost = set([*map_data[loc].traversal_cost])
                total_cost = rcost | tcost

                self._tile_graph[loc] = map_logic.reward_lookup(total_cost)

                if rcost.issubset(search_inventory):
                    for reward_item in self._tile_graph[loc].reward:
                        search_inventory.add(reward_item)

                if total_cost.issubset(search_inventory):
                    completed_keys.add(loc)

            graph_stages[stage_key].intersection_update(completed_keys)
            path_proc.global_inventory.update(interim_inventory)
        return graph_stages

    # def process_graph(self,
    #                   graph_start: tuple,
    #                   graph_end: tuple,
    #                   map_logic,
    #                   map_item):
    #     (topo_graph, graph_stages, bottlenecks) = self.form_topological_graph(
    #         graph_start, graph_end, map_logic, map_item
    #     )
    #     full_node = [graph_start]
    #     for coord in bottlenecks.keys():
    #         full_node.append(coord)
    #     # full_node.append(graph_end)

    #     pathproc = z2p.pathprocessor.PathProcessor(self, map_logic, map_item)
    #     count = 0
    #     trees = []
    #     for node in full_node:
    #         try:
    #             item = bottlenecks[node]
    #             pathproc.global_inventory.update(item)
    #         except KeyError:
    #             pass

    #         (region_keys, tile_paths) = pathproc.initialize_search_space(node)
    #         subtree = pathproc.search_region_space(node,
    #                                                tile_paths,
    #                                                region_keys)
    #         trees.extend(subtree)
    #         print(f'Iteration {count} | {node}')
    #         count += 1

    def process_stages(self, map_logic, graph_stages: dict) -> dict:
        """
        Debugging method for visualizing bottlenecks in the topological
        graph formation
        """
        bottlenecks = dict()
        stage_cmp = []
        for stage_lvl, coord_collection in graph_stages.items():
            stage_cmp.append(coord_collection)
            # print(f'{stage_lvl}')
            # for coord in coord_collection:
            #     msg = (f'{coord} | '
            #            f'{self._tile_graph[coord].traversal_cost} | '
            #            f'{self._tile_graph[coord].reward_cost} | '
            #            f'{self._tile_graph[coord].reward}')
            #     print(msg)

            if len(stage_cmp) == 2:
                prev_stage_rewards = set()
                for crd in stage_cmp[0]:
                    for rew in self._tile_graph[crd].reward:
                        prev_stage_rewards.add(rew)

                curr_stage_costs = set()
                for crd in stage_cmp[1]:
                    for t_cost in self._tile_graph[crd].traversal_cost:
                        curr_stage_costs.add(t_cost)

                    for r_cost in self._tile_graph[crd].reward_cost:
                        curr_stage_costs.add(r_cost)

                bottleneck_item = set.intersection(
                    curr_stage_costs, prev_stage_rewards
                )

                bottleneck_coord = map_logic.reward_lookup(bottleneck_item)
                bottlenecks[bottleneck_coord[0]] = bottleneck_item
                stage_cmp.pop(0)
        return bottlenecks

    def form_network_graph(
        self, topological_graph: dict, graph_end: tuple, map_logic
    ):
        """
        Takes the calculated topological graph and visualizes the graph network
        """
        topo_network_graph = nx.DiGraph()
        node_traversal = [graph_end]
        while node_traversal:
            parent_node = node_traversal.pop()
            if parent_node is not None:
                plabel = map_logic[parent_node].description
                topo_network_graph.add_node(plabel, pos=parent_node)

                child_nodes = topological_graph[parent_node]
                if child_nodes[0] is not None:
                    child_labels = [
                        map_logic[cnode].description for cnode in child_nodes
                    ]
                    for cnode, clabel in zip(child_nodes, child_labels):
                        topo_network_graph.add_edge(plabel, clabel)
                        node_traversal.append(cnode)

        plt.figure()
        node_position = nx.get_node_attributes(topo_network_graph, "pos")
        nx.draw_networkx(topo_network_graph, node_position)
        net_ax = plt.gca()
        net_ax.invert_yaxis()
        plt.grid()
        plt.show()

    # def __getitem__(self, index: tuple) -> TileNode:
    #     graph_entry = None
    #     try:
    #         graph_entry = self._tile_graph[index]
    #     except KeyError as gen_err:
    #         raise gen_err
    #     return graph_entry
