#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import commodity.path
import osmnx as ox
import networkx as nx
import utilities
import os
import json

# Define and prepare data
bottom_left = [38.954487, -3.958351]
top_right = [39.012350, -3.863268]
project_dir = commodity.path.get_project_dir('.')
graph_file_cache = os.path.join(project_dir, 'src/cache/ciudad-real-graph.graphml')
danger_nodes_file_cache = os.path.join(project_dir, 'src/cache/ciudad-real-danger-nodes.geojson')
amenities_file = os.path.join(project_dir, 'config/amenities_config.json')
survey_cases_config = os.path.join(project_dir, 'config/validation_survey_cases.json')
survey_dir = os.path.join(project_dir, 'data/survey')


def calculate_best_routes():
    best_routes = {}
    with open(survey_cases_config) as json_file:
        survey_cases = json.load(json_file)
    
    for case_id in survey_cases:
        origin = survey_cases[case_id]['origin']
        destiny = survey_cases[case_id]['destiny']

        origin_node = ox.get_nearest_node(G, [origin[1], origin[0]])
        destination_node = ox.get_nearest_node(G, [destiny[1], destiny[0]])

        route = nx.shortest_path(G, origin_node, destination_node, weight='length')
        best_routes[case_id] = utilities.route_to_geojson(G, route)
    
    return best_routes

if __name__ == '__main__':
    with open(amenities_file) as geojson_file:
        amenities = json.load(geojson_file)

    G = utilities.init_graph(bottom_left, top_right, graph_file_cache, amenities)
    utilities.load_danger_points(bottom_left, top_right, danger_nodes_file_cache, amenities)

    best_routes = calculate_best_routes()
    
    with open(danger_nodes_file_cache) as json_file:
        danger_points_data = json.load(json_file)

    for currentpath, folders, files in os.walk(survey_dir):
        for file in files:            
            with open(os.path.join(survey_dir, currentpath, file)) as json_file:
                route = json.load(json_file)

                case_id = route['properties']['case_id']
                result = utilities.routes_operations.compare_routes(best_routes[case_id], route, danger_points_data)

                print(result)
