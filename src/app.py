#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*- 

from datetime import datetime
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS
import geopandas as gpd
import osmnx as ox
import networkx as nx
import commodity.path
import utilities
import os
import json

ox.config(log_console=True, use_cache=True)
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = '*'

# Define and prepare data for Ciudad Real
project_dir = commodity.path.get_project_dir('.')
bottom_left = [38.954487, -3.958351]
top_right = [39.012350, -3.863268]
graph_file_cache = os.path.join(project_dir, 'src/cache/ciudad-real-graph.graphml')
danger_nodes_file_cache = os.path.join(project_dir, 'src/cache/ciudad-real-danger-nodes.geojson')
survey_directory = os.path.join(project_dir, "data/survey/")
amenities_file = os.path.join(project_dir, 'config/amenities_config.json')
survey_config_file = os.path.join(project_dir, 'config/validation_survey_cases.json')

@app.route('/covid19-routes/api/v1.0/ciudad-real/route/', methods=['GET'])
def get_route():
    # Route data
    route_type = request.args.get('route_type')
    origin = (request.args.get('origin_lat', type=float), request.args.get('origin_lon', type=float))
    destination = (request.args.get('destination_lat', type=float), request.args.get('destination_lon', type=float))

    # Calculate osm nodes near origin and destination
    origin_node = ox.get_nearest_node(G, origin)
    destination_node = ox.get_nearest_node(G, destination)

    if route_type == 'safe':
        route = nx.shortest_path(G, origin_node, destination_node, weight='weight')
    elif route_type == 'danger':
        route = nx.shortest_path(G, origin_node, destination_node, weight='length')
    else:
        abort(404)

    return utilities.route_to_geojson(G, route)

@app.route('/covid19-routes/api/v1.0/ciudad-real/danger-points/', methods=['GET'])
def get_danger_points():
    return utilities.load_danger_points(bottom_left, top_right, danger_nodes_file_cache, amenities)

@app.route('/covid19-routes/api/v1.0/ciudad-real/survey/', methods=['POST'])
def add_message():
    content = request.get_json()
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y_%H:%M:%S")
    file_name = "{}_{}.geojson".format(content["properties"]["case_id"], timestampStr)

    if not os.path.exists(survey_directory):
        try:
            os.makedirs(survey_directory)
        except OSError:
            print ("Creation of the directory %s failed" % survey_directory)
  
    with open(survey_directory + file_name, 'w') as outfile:
        json.dump(content, outfile)

    return jsonify(None)

@app.route('/covid19-routes/api/v1.0/ciudad-real/survey/get-cases/', methods=['GET'])
def get_cases():
    with open(survey_config_file) as f:
        data = json.load(f)
        return data

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    with open(amenities_file) as geojson_file:
        amenities = json.load(geojson_file)

    G = utilities.init_graph(bottom_left, top_right, graph_file_cache, amenities)
    utilities.load_danger_points(bottom_left, top_right, danger_nodes_file_cache, amenities)
    app.run(debug=True, host='127.0.0.1', port=5001)


# curl -i "http://127.0.0.1:5001/covid19-routes/api/v1.0/ciudad-real/?route_type=danger&origin_lat=39.001441&origin_lon=-3.924548&destination_lat=38.976429&destination_lon=-3.930899"