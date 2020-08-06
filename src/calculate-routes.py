#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import geopandas as gpd
import osmnx as ox
import networkx as nx
import sys
import os
import utilities

ox.config(log_console=True, use_cache=True)

# define a bounding box in Ciudad Real
bottom_left = [38.954487, -3.958351]
top_right = [39.012350, -3.863268]
north, south, east, west = top_right[0], bottom_left[0], bottom_left[1], top_right[1]


G = ox.graph_from_bbox(north, south, east, west, network_type='walk', simplify=False)

nodes_near = []
nodes_near_education = utilities.nodes_near_amenity(bottom_left, top_right, "school")
nodes_near_education.extend(utilities.nodes_near_amenity(bottom_left, top_right, "university"))
nodes_near_bank = utilities.nodes_near_amenity(bottom_left, top_right, "bank")

for node in nodes_near_education + nodes_near_bank:
    if node not in nodes_near:
        nodes_near.append(node)

utilities.graph_operations.set_weight(G, nodes_near, correction_factor=5000000)


# Route data
origin = (float(sys.argv[1]), float(sys.argv[2]))
destination = (float(sys.argv[3]), float(sys.argv[4]))

# Calculate osm nodes near origin and destination
origin_node = ox.get_nearest_node(G, origin)
destination_node = ox.get_nearest_node(G, destination)

# Calculate routes
danger_route = nx.shortest_path(G, origin_node, destination_node, weight='length')
safe_route = nx.shortest_path(G, origin_node, destination_node, weight='weight')


# Export geojson routes
file_name_safe_route = 'safe_route.geojson'
file_name_danger_route = 'danger_route.geojson'
dir_route = './data/'

# To changue
utilities.geojson_to_file(dir_route, file_name_safe_route, utilities.route_to_geojson(G, safe_route))
utilities.geojson_to_file(dir_route, file_name_danger_route, utilities.route_to_geojson(G, danger_route))


# Show the simplified network with edges colored by length
nodes_near_education_ids = [node.id for node in nodes_near_education]
nodes_near_bank_ids = [node.id for node in nodes_near_bank]

nc = ['r' if node in nodes_near_education_ids else 'g' if node in nodes_near_bank_ids else 'w' for node in G.nodes()]
ec = ox.plot.get_edge_colors_by_attr(G, attr='weight', cmap='plasma')

fig, ax = ox.plot_graph_routes(G, routes=[safe_route, danger_route], route_colors=['c', 'r'], route_linewidth=6,
                        node_color=nc, node_edgecolor='k', node_size=20,
                        edge_color=ec, edge_linewidth=3)
