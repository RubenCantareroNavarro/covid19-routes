#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import geopandas as gpd
import osmnx as ox
import networkx as nx
import sys
sys.path.append('../../src/')

import utilities
import geojson

ox.config(log_console=True, use_cache=True)


def create_features(nodes_near, danger_level):
    features = []
    for node in nodes_near:
        feature = geojson.Feature(geometry=geojson.Point((node.lon, node.lat)), properties={"id": node.id, "danger" : danger_level})
        features.append(feature)

    return features

# define a bounding box in Ciudad Real
bottom_left = [38.954487, -3.958351]
top_right = [39.012350, -3.863268]

# Safe route
nodes_near_school = utilities.nodes_near_amenity(bottom_left, top_right, "school")
nodes_near_university = utilities.nodes_near_amenity(bottom_left, top_right, "university")
nodes_near_bank = utilities.nodes_near_amenity(bottom_left, top_right, "bank")

features = create_features(nodes_near_school, 10)
features.extend(create_features(nodes_near_university, 5))
features.extend(create_features(nodes_near_bank, 1))

feature_collection = geojson.FeatureCollection(features)

with open('../../../smartcity-viewer/data/danger_points.geojson', 'w') as f:
   geojson.dump(feature_collection, f)

