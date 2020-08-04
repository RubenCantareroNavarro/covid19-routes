#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import networkx as nx
import utilities

def dijkstra(graph, start, end):
    distances = {}
    predecessors = {}
    to_assess = graph.nodes

    for node in graph.nodes:
        distances[node] = float('inf')
        predecessors[node] = None

    sp_set = []
    distances[start] = 0

    while len(sp_set) < len(to_assess):
        still_in = {node: distances[node]\
                    for node in [node for node in\
                    to_assess if node not in sp_set]}

        closest = min(still_in, key = distances.get)

        sp_set.append(closest)

        for node in graph[closest]:
            if distances[node] > distances[closest] +\
                    graph[closest][node]['weight']:

                distances[node] = distances[closest] +\
                    graph[closest][node]['weight']

                predecessors[node] = closest

    path = [end]
    while start not in path:
        path.append(predecessors[path[-1]])

    return path[::-1], distances[end]

def set_weight(G, nodes_near, correction_factor=1):
    nodes_near_amenities_ids = [node.id for node in nodes_near]

    for node1, node2, d, data in G.edges(keys=True, data=True):
        weight = G[node1][node2][d]["length"]

        if node1 in nodes_near_amenities_ids or node2 in nodes_near_amenities_ids:
            weight = weight * correction_factor

                
        G[node1][node2][d]["weight"] = weight
        G[node2][node1][d]["weight"] = weight # ¿Clean?