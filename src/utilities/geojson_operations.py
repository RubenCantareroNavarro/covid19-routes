#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import geopandas as gpd
import osmnx as ox
import networkx as nx
import os
import sys
import utilities
import geojson

ox.config(log_console=True, use_cache=True)

def geojson_to_file(file_name, data):
    with open(file_name, 'w') as f:
        geojson.dump(data, f, indent = 4)

def create_features(nodes_near, danger_level, amenity_near):
    features = []
    for node in nodes_near:
        # The decimal precision in osmnx is seven. By default, the geojson library uses precision 6
        feature = geojson.Feature(geometry=geojson.Point((node.lon, node.lat), precision=7), properties={"osm_id": node.id, "danger" : danger_level, "amenity_near" : amenity_near})
        features.append(feature)

    return features

def geojson_danger_points(bottom_left, top_right, amenities):
    features = []
    for amenity in amenities.keys():
        nodes_near_amenity = (utilities.nodes_near_amenity(bottom_left, top_right, amenity, amenities[amenity]['radius']))
        features.extend(create_features(nodes_near_amenity, amenities[amenity]['danger_level'], amenity))

    feature_collection = geojson.FeatureCollection(features)

    return feature_collection

def load_danger_points(bottom_left, top_right, danger_nodes_file_cache, amenities):
    if not os.path.isfile(danger_nodes_file_cache):
        data = utilities.geojson_danger_points(bottom_left, top_right, amenities)
        utilities.geojson_to_file(danger_nodes_file_cache, data)

    with open(danger_nodes_file_cache) as geojson_file:
        return geojson.load(geojson_file)

def route_to_geojson(G, route):
    nodes_coord = []
    for node_id in route:
        nodes_coord.append([G.nodes[node_id]['x'], G.nodes[node_id]['y']])

    line_string = geojson.LineString(nodes_coord, precision=7)
    feature = geojson.Feature(geometry=line_string)

    return feature


