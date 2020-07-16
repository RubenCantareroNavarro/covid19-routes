#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import geopandas as gpd
import osmnx as ox

ox.config(log_console=True, use_cache=True)


# define a bounding box in Ciudad Real
# north, south, east, west = 37.79, 37.78, -122.41, -122.43
north, south, east, west = 39.012350, 38.954487, -3.958351, -3.863268

# 39.012350, -3.958351
# 38.954487, -3.863268

# create network from that bounding box
G = ox.graph_from_bbox(north, south, east, west, network_type='walk', simplify=True)

# save street network as GraphML file to work with later in OSMnx or networkx or gephi
ox.save_graphml(G, filepath='../data/ciudadreal-walk.graphml')

# Print attributes of nodes
for node_id in G.nodes():
    print(G.nodes[node_id])

# print(G.edges(keys=True, data=True))

for edge int G.edges():
    

# show the simplified network with edges colored by length
ec = ox.plot.get_edge_colors_by_attr(G, attr='length', cmap='plasma_r')
fig, ax = ox.plot_graph(G, node_color='w', node_edgecolor='k', node_size=50,
                        edge_color=ec, edge_linewidth=3)

