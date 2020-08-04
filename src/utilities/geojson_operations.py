#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import geopandas as gpd
import osmnx as ox
import networkx as nx
import sys
import utilities
import geojson

ox.config(log_console=True, use_cache=True)


# define a bounding box in Ciudad Real
bottom_left = [38.954487, -3.958351]
top_right = [39.012350, -3.863268]

def geojson_to_file(file_dir, file_name, data):
    with open(file_dir + file_name, 'w') as f:
        geojson.dump(data, f)

def create_features(nodes_near, danger_level):
    features = []
    for node in nodes_near:
        feature = geojson.Feature(geometry=geojson.Point((node.lon, node.lat)), properties={"id": node.id, "danger" : danger_level})
        features.append(feature)

    return features

def export_danger_points(file_dir, file_name):
    nodes_near_school = utilities.nodes_near_amenity(bottom_left, top_right, "school")
    nodes_near_university = utilities.nodes_near_amenity(bottom_left, top_right, "university")
    nodes_near_bank = utilities.nodes_near_amenity(bottom_left, top_right, "bank")

    features = create_features(nodes_near_school, 10)
    features.extend(create_features(nodes_near_university, 5))
    features.extend(create_features(nodes_near_bank, 1))

    feature_collection = geojson.FeatureCollection(features)

    geojson_to_file(file_dir, file_name, feature_collection)
    

def export_route(file_dir, file_name, G, route):
    nodes_coord = []
    for node_id in route:
        nodes_coord.append([G.nodes[node_id]['x'], G.nodes[node_id]['y']])

    line_string = geojson.LineString(nodes_coord)
    feature = geojson.Feature(geometry=line_string)

    geojson_to_file(file_dir, file_name, feature)


