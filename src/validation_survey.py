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
import argparse
from geopy.distance import geodesic

ox.config(use_cache=True, log_console=False)

parser = argparse.ArgumentParser()
parser.add_argument("survey_results_case_dir", help="Directory where respondents' routes are stored for all cases")
parser.add_argument("case_id", help="case_id of the case to be processed")
parser.add_argument("results_dir", help="Directory to store processed results")
args = parser.parse_args()
case_id = args.case_id
results_dir = os.path.join(args.results_dir, 'results')
survey_results_case_dir = os.path.join(args.survey_results_case_dir, case_id)

# Define and prepare data
bottom_left = [38.954487, -3.958351]
top_right = [39.012350, -3.863268]
project_dir = commodity.path.get_project_dir('.')
graph_file_cache = os.path.join(project_dir, 'src/cache/ciudad-real-graph_{}.graphml'.format(case_id))
danger_nodes_file_cache = os.path.join(project_dir, 'src/cache/ciudad-real-danger-nodes_{}.geojson'.format(case_id))
amenities_file = os.path.join(project_dir, 'config/amenities_{}_config.json'.format(case_id))
survey_cases_config = os.path.join(project_dir, 'config/validation_survey_cases.json')



def calculate_system_route():
    system_routes = {}
    with open(survey_cases_config) as json_file:
        survey_cases = json.load(json_file)
    
    origin = survey_cases[case_id]['origin']
    destiny = survey_cases[case_id]['destiny']

    origin_node = ox.get_nearest_node(G, [origin[1], origin[0]])
    destination_node = ox.get_nearest_node(G, [destiny[1], destiny[0]])

    route = nx.shortest_path(G, origin_node, destination_node, weight='weight')
    system_routes["safest"] = {}
    system_routes["safest"]["route_nodes"] = route
    system_routes["safest"]["route_coordinates"] = utilities.route_to_geojson(G, route)
    system_routes["safest"]["route_length"] = utilities.routes_operations.route_length(G, route)
    system_routes["safest"]["route_weight"] = utilities.routes_operations.route_weight(G, route)
    system_routes["safest"]["number_danger_points"] = utilities.routes_operations.number_danger_points_in_route(danger_points_data, system_routes["safest"]["route_coordinates"])


    route = nx.shortest_path(G, origin_node, destination_node, weight='length')
    system_routes["shortest"] = {}
    system_routes["shortest"]["route_nodes"] = route
    system_routes["shortest"]["route_coordinates"] = utilities.route_to_geojson(G, route)
    system_routes["shortest"]["route_length"] = utilities.routes_operations.route_length(G, route)
    system_routes["shortest"]["route_weight"] = utilities.routes_operations.route_weight(G, route)
    system_routes["shortest"]["number_danger_points"] = utilities.routes_operations.number_danger_points_in_route(danger_points_data, system_routes["shortest"]["route_coordinates"])
    return system_routes

if __name__ == '__main__':
    with open(amenities_file) as geojson_file:
        amenities = json.load(geojson_file)

    utilities.load_danger_points(bottom_left, top_right, danger_nodes_file_cache, amenities)
    with open(danger_nodes_file_cache) as json_file:
        danger_points_data = json.load(json_file)

    G = utilities.init_graph(bottom_left, top_right, graph_file_cache, amenities)
    system_routes = calculate_system_route()

    csv_data = []
    for currentpath, folders, files in os.walk(survey_results_case_dir):
        for file in files:            
            with open(os.path.join(survey_results_case_dir, currentpath, file)) as json_file:
                route = json.load(json_file)
                case_id = route['properties']['case_id']
                case_last_point = system_routes["safest"]["route_coordinates"]['geometry']['coordinates'][-1]
                current_last_point = route['geometry']['coordinates'][-1]
                distance_ends = geodesic([case_last_point[1], case_last_point[0]], [current_last_point[1], current_last_point[0]]).meters

                survey_number_danger_points = utilities.routes_operations.number_danger_points_in_route(danger_points_data, route)
                survey_route_nodes = utilities.routes_operations.coordinates_to_graph_nodes(G, route)
                survey_route_length = utilities.routes_operations.route_length(G, survey_route_nodes)
                survey_route_weight = utilities.routes_operations.route_weight(G, survey_route_nodes)

                print([file, case_id, [survey_number_danger_points, survey_route_length], [system_routes["safest"]["number_danger_points"], system_routes["safest"]["route_length"]]])

                csv_data.append({
                    'file_name': file, 
                    'case_id': case_id, 
                    'knowledge_city_level': route['properties']['knowledge_city_level'], 
                    'age':  route['properties']['age'], 
                    'gender': route['properties']['gender'], 
                    'comments': route['properties']['comments'], 
                    'survey_number_danger_points': survey_number_danger_points, 
                    'survey_route_length': survey_route_length, 
                    'survey_route_weight': survey_route_weight, 
                    'safest_number_danger_points': system_routes["safest"]["number_danger_points"], 
                    'safest_route_length': system_routes["safest"]["route_length"],
                    'safest_route_weight': system_routes["safest"]["route_weight"],
                    'shortest_number_danger_points': system_routes["shortest"]["number_danger_points"], 
                    'shortest_route_length': system_routes["shortest"]["route_length"],
                    'shortest_route_weight': system_routes["shortest"]["route_weight"],
                    'distance_ends (m)': distance_ends,
                    'valid': distance_ends < 200
                })
        
    if not os.path.exists(results_dir):
        try:
            os.makedirs(os.path.join(results_dir, 'summaries'))
            os.makedirs(os.path.join(results_dir, 'system_routes'))
        except OSError:
            print ("Creation of the directory %s failed" % file_path)

    with open(os.path.join(results_dir, 'summaries' , case_id + '_validation_survey_summary.csv'), mode='w') as csv_file:
        fieldnames = ['file_name', 'case_id', 'knowledge_city_level', 'age', 'gender', 'comments', 'survey_number_danger_points', 'survey_route_length', 'survey_route_weight', 'safest_number_danger_points', 'safest_route_length', 'safest_route_weight', 'shortest_number_danger_points', 'shortest_route_length', 'shortest_route_weight', 'distance_ends (m)', 'valid']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(csv_data)
        

    utilities.geojson_to_file(os.path.join(results_dir, 'system_routes', case_id + '_safest_route.geojson'),  utilities.route_to_geojson(G, system_routes["safest"]["route_nodes"])) 
    utilities.geojson_to_file(os.path.join(results_dir, 'system_routes', case_id + '_shortest_route.geojson'),  utilities.route_to_geojson(G, system_routes["shortest"]["route_nodes"])) 