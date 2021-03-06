#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import networkx as nx
import osmnx as ox
import os
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

def set_weight(G, bottom_left, top_right, amenities):
    for node1, node2, d, data in G.edges(keys=True, data=True):
        weight = G[node1][node2][d]["length"]
        G[node1][node2][d]["weight"] = weight
        G[node2][node1][d]["weight"] = weight

    for amenity in amenities.keys():
        nodes_near_amenity = (utilities.nodes_near_amenity(bottom_left, top_right, amenity, amenities[amenity]['radius']))
        nodes_near_amenity_ids = [node.id for node in nodes_near_amenity]
       
        for node1, node2, d, data in G.edges(keys=True, data=True):
            weight = G[node1][node2][d]["length"]

            if node1 in nodes_near_amenity_ids or node2 in nodes_near_amenity_ids:
                weight = weight * amenities[amenity]['correction_factor']
                G[node1][node2][d]["weight"] = weight
                G[node2][node1][d]["weight"] = weight # ¿Clean?

def init_graph(bottom_left, top_right, graph_file_cache, amenities):
    if os.path.isfile(graph_file_cache):
        print("The graph exits. Loading...")
        G = ox.io.load_graphml(graph_file_cache)
    else:
        north, south, east, west = top_right[0], bottom_left[0], bottom_left[1], top_right[1]
        G = ox.graph_from_bbox(north, south, east, west, network_type='walk', simplify=False)
        utilities.graph_operations.set_weight(G, bottom_left, top_right, amenities)
        ox.save_graphml(G, graph_file_cache) #SOLVE: por defecto pone el atributo weight como cadena, cuando debe ser un float.
    
    return G