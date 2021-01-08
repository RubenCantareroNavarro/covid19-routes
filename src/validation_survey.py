#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import commodity.path
import osmnx as ox
import networkx as nx
import utilities
import os
import json
import csv
import sys
from geopy.distance import geodesic

ox.config(use_cache=True, log_console=False)

# Define and prepare data
bottom_left = [38.954487, -3.958351]
top_right = [39.012350, -3.863268]
project_dir = commodity.path.get_project_dir('.')
graph_file_cache = os.path.join(project_dir, 'src/cache/ciudad-real-graph_case-010.graphml')
danger_nodes_file_cache = os.path.join(project_dir, 'src/cache/ciudad-real-danger-nodes_case-010.geojson')
amenities_file = os.path.join(project_dir, 'config/amenities_case-010_config.json')
survey_cases_config = os.path.join(project_dir, 'config/validation_survey_cases.json')
survey_dir = sys.argv[1]


def calculate_best_routes():
    best_routes = {}
    with open(survey_cases_config) as json_file:
        survey_cases = json.load(json_file)
    
    for case_id in survey_cases:
        origin = survey_cases[case_id]['origin']
        destiny = survey_cases[case_id]['destiny']

        origin_node = ox.get_nearest_node(G, [origin[1], origin[0]])
        destination_node = ox.get_nearest_node(G, [destiny[1], destiny[0]])

        # ToDo: lenght? or weight?
        route = nx.shortest_path(G, origin_node, destination_node, weight='weight')
        best_routes[case_id] = {}
        best_routes[case_id]["route_nodes"] = route
        best_routes[case_id]["route_coordinates"] = utilities.route_to_geojson(G, route)
        best_routes[case_id]["route_length"] = utilities.routes_operations.route_cost(G, route)
        best_routes[case_id]["number_danger_points"] = utilities.routes_operations.number_danger_points_in_route(danger_points_data, best_routes[case_id]["route_coordinates"])
    
    return best_routes

if __name__ == '__main__':
    with open(amenities_file) as geojson_file:
        amenities = json.load(geojson_file)

    utilities.load_danger_points(bottom_left, top_right, danger_nodes_file_cache, amenities)
    with open(danger_nodes_file_cache) as json_file:
        danger_points_data = json.load(json_file)

    G = utilities.init_graph(bottom_left, top_right, graph_file_cache, amenities)
    best_routes = calculate_best_routes()

    csv_data = []
    for currentpath, folders, files in os.walk(survey_dir):
        for file in files:            
            with open(os.path.join(survey_dir, currentpath, file)) as json_file:
                route = json.load(json_file)
                case_id = route['properties']['case_id']
                case_last_point = best_routes[case_id]["route_coordinates"]['geometry']['coordinates'][-1]
                current_last_point = route['geometry']['coordinates'][-1]
                distance_ends = geodesic([case_last_point[1], case_last_point[0]], [current_last_point[1], current_last_point[0]]).meters

                survey_number_danger_points = utilities.routes_operations.number_danger_points_in_route(danger_points_data, route)
                survey_route_nodes = utilities.routes_operations.coordinates_to_graph_nodes(G, route)
                survey_route_length = utilities.routes_operations.route_cost(G, survey_route_nodes)

                print([file, case_id, [survey_number_danger_points, survey_route_length], [best_routes[case_id]["number_danger_points"], best_routes[case_id]["route_length"]]])

                csv_data.append({
                    'file_name': file, 
                    'case_id': case_id, 
                    'knowledge_city_level': route['properties']['knowledge_city_level'], 
                    'age':  route['properties']['age'], 
                    'gender': route['properties']['gender'], 
                    'comments': route['properties']['comments'], 
                    'survey_number_danger_points': survey_number_danger_points, 
                    'survey_route_length': survey_route_length, 
                    'best_number_danger_points': best_routes[case_id]["number_danger_points"], 
                    'best_route_length': best_routes[case_id]["route_length"],
                    'distance_ends (m)': distance_ends,
                    'valid': distance_ends < 200
                })
            
    with open(os.path.join(survey_dir, 'validation_survey_summary.csv'), mode='w') as csv_file:
        fieldnames = ['file_name', 'case_id', 'knowledge_city_level', 'age', 'gender', 'comments', 'survey_number_danger_points', 'survey_route_length', 'best_number_danger_points', 'best_route_length', 'distance_ends (m)', 'valid']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(csv_data)


