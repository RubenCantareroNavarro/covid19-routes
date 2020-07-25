#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import geopandas as gpd
import osmnx as ox
import networkx as nx
import sys
sys.path.append('../src/')

import utilities

ox.config(log_console=True, use_cache=True)

# define a bounding box in Ciudad Real
bottom_left = [38.954487, -3.958351]
top_right = [39.012350, -3.863268]
north, south, east, west = top_right[0], bottom_left[0], bottom_left[1], top_right[1]

# Route data
origin = (39.001441, -3.924548)
destination = (38.976429, -3.930899)
amenity = "school" # Also is posible about banks, hosìtals, etc.
cf = 5000000

# Create network from that bounding box
G = ox.graph_from_bbox(north, south, east, west, network_type='walk', simplify=True)
origin_node = ox.get_nearest_node(G, origin)
destination_node = ox.get_nearest_node(G, destination)

# Danger route 
danger_route = nx.shortest_path(G, origin_node, destination_node, weight='length')

# Safe route
nodes_near = utilities.nodes_near_amenity(bottom_left, top_right, amenity) #ToMove
utilities.graph_operations.set_weight(G, nodes_near, correction_factor=cf)

# Calculate route
safe_route = nx.shortest_path(G, origin_node, destination_node, weight='weight')

# Show the simplified network with edges colored by length
nodes_near_amenities_ids = [node.id for node in nodes_near]
nc = ['r' if node in nodes_near_amenities_ids else 'w' for node in G.nodes()]
ec = ox.plot.get_edge_colors_by_attr(G, attr='weight', cmap='plasma')

fig, ax = ox.plot_graph_routes(G, routes=[safe_route, danger_route], route_colors=['c', 'r'], route_linewidth=6,
                        node_color=nc, node_edgecolor='k', node_size=20,
                        edge_color=ec, edge_linewidth=3)


