"""
TileGraph:
Converting the raw map data into a set of connected nodes in a graph for
traversal purposes data structure for storing the converted
map data with tile information
    - TileGraph stores a collection of TileData objects
"""

import itertools
import networkx as nx
import matplotlib.pyplot as plt

from .pathprocessor import PathProcessor
from .tilemap import TileMap
from .tilenode import TileNode
from .tilesearch import floodfill


class TileGraph:
    """
    Graph object for handling the map node connections
    """

    def __init__(
        self,
        graph_start: tuple,
        graph_end: tuple,
        map_data: TileMap,
        logic_table,
        LocationMap,
    ):
        self.graph_start = graph_start
        self.graph_end = graph_end
        self._tile_graph = dict()

        self._form_tile_graph(map_data, logic_table, tile_table)

    def _form_tile_graph(self, map_logic, map_item, tile_table):
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
        path_proc = z2p.pathprocessor.PathProcessor(self, map_logic, map_item)
        topo_graph = {}
        completed_keys = set()
        stages = {}

        stage_count = 0
        while graph_end not in completed_keys:
            interim_inventory = set()
            region_stack = path_proc.explore_region(graph_start)

            region_keys = set(path_proc.key_tile) & set(region_stack)
            stage_key = f"Stage {stage_count}"
            stage_count += 1
            stages[stage_key] = region_keys.difference(completed_keys)

            for rkey in region_keys.difference(completed_keys):
                rcost = set([*self._tile_graph[rkey].reward_cost])
                tcost = set([*self._tile_graph[rkey].traversal_cost])

                item_set = rcost | tcost
                topo_graph[rkey] = map_logic.reward_lookup(item_set)

                if rcost.issubset(path_proc.global_inventory):
                    for reward_item in self._tile_graph[rkey].reward:
                        interim_inventory.add(reward_item)

                if rcost.issubset(path_proc.global_inventory) and tcost.issubset(
                    path_proc.global_inventory
                ):
                    completed_keys.add(rkey)

            stages[stage_key].intersection_update(completed_keys)
            path_proc.global_inventory.update(interim_inventory)

        bottlenecks = self.process_stages(map_logic, stages)

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
        return (topo_graph, stages, bottlenecks)

    # def process_graph(self,
    #                   graph_start: tuple,
    #                   graph_end: tuple,
    #                   map_logic,
    #                   map_item):
    #     (topo_graph, stages, bottlenecks) = self.form_topological_graph(
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

    def process_stages(self, map_logic, stages: dict) -> dict:
        """
        Debugging method for visualizing bottlenecks in the topological
        graph formation
        """
        bottlenecks = dict()
        stage_cmp = []
        for stage_lvl, coord_collection in stages.items():
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

                bottleneck_item = set.intersection(curr_stage_costs, prev_stage_rewards)

                try:
                    bottleneck_item.remove("|")
                except KeyError:
                    pass

                bottleneck_coord = map_logic.reward_lookup(bottleneck_item)
                bottlenecks[bottleneck_coord[0]] = bottleneck_item
                stage_cmp.pop(0)
        return bottlenecks

    def form_network_graph(self, topological_graph: dict, graph_end: tuple, map_logic):
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
