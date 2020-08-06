#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import geopandas as gpd
import osmnx as ox
import networkx as nx
import sys
import utilities
import geojson

ox.config(log_console=True, use_cache=True)

def geojson_to_file(file_dir, file_name, data):
    with open(file_dir + file_name, 'w') as f:
        geojson.dump(data, f)

def create_features(nodes_near, danger_level, amenity_near):
    features = []
    for node in nodes_near:
        feature = geojson.Feature(geometry=geojson.Point((node.lon, node.lat)), properties={"osm_id": node.id, "danger" : danger_level, "amenity_near" : amenity_near})
        features.append(feature)

    return features

def geojson_danger_points(bottom_left, top_right):
    features = []
    for amenity in utilities.amenities:
        nodes_near_amenity = (utilities.nodes_near_amenity(bottom_left, top_right, amenity['type'], amenity['radius']))
        features.extend(create_features(nodes_near_amenity, amenity['danger_level'], amenity['type']))

    feature_collection = geojson.FeatureCollection(features)

    return feature_collection
    

def route_to_geojson(G, route):
    nodes_coord = []
    for node_id in route:
        nodes_coord.append([G.nodes[node_id]['x'], G.nodes[node_id]['y']])

    line_string = geojson.LineString(nodes_coord)
    feature = geojson.Feature(geometry=line_string)

    return feature


