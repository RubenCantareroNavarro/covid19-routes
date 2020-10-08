#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import geopandas as gpd
import osmnx as ox
import networkx as nx
import commodity.path
import os
import json
import sys
sys.path.append(os.path.join(commodity.path.get_project_dir(''), 'src/'))
import utilities

ox.config(log_console=True, use_cache=True)

# define a bounding box in Ciudad Real
bottom_left = [38.954487, -3.958351]
top_right = [39.012350, -3.863268]
graph_file_cache = sys.argv[5]
danger_nodes_file_cache = sys.argv[6]
amenities_file = sys.argv[7]

with open(amenities_file) as geojson_file:
   amenities = json.load(geojson_file)

G = utilities.init_graph(bottom_left, top_right, graph_file_cache, amenities)
danger_points = utilities.load_danger_points(bottom_left, top_right, danger_nodes_file_cache, amenities)

danger_nodes = []
for feature in danger_points["features"]:
   danger_nodes.append(feature['properties']['osm_id'])


# Route data
origin = (float(sys.argv[1]), float(sys.argv[2]))
destination = (float(sys.argv[3]), float(sys.argv[4]))

# Calculate osm nodes near origin and destination
origin_node = ox.get_nearest_node(G, origin)
destination_node = ox.get_nearest_node(G, destination)

# Calculate routes
danger_route = nx.shortest_path(G, origin_node, destination_node, weight='length')
safe_route = nx.shortest_path(G, origin_node, destination_node, weight='weight')

# Used to give diferent color to nodes
# nc = ['r' if node in nodes_near_education_ids else 'g' if node in nodes_near_bank_ids else 'w' for node in G.nodes()]
nc = ['r' if node in danger_nodes else 'w' for node in G.nodes()]
ec = ox.plot.get_edge_colors_by_attr(G, attr='weight', cmap='plasma')

fig, ax = ox.plot_graph_routes(G, routes=[safe_route, danger_route], route_colors=['c', 'r'], route_linewidth=6,
                        node_color=nc, node_edgecolor='k', node_size=20,
                        edge_color=ec, edge_linewidth=3)
