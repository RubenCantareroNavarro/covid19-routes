#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-
import osmnx as ox

def number_danger_points_in_route(danger_points_data, route):
    cont = 0
    danger_points = []
    last_point = []

    for feature in danger_points_data['features']:
        danger_at_point = float(feature['properties']['danger'])
        if(danger_at_point > 1):
            danger_points.append(feature['geometry']['coordinates'])

    for point in route['geometry']['coordinates']: 
        if last_point == point:
            continue

        if(point in danger_points):
            cont += 1

        last_point = point

    return cont

def route_length(G, route):
    return sum([G[route[i]][route[i+1]][0]['length'] for i in range(len(route)-1)])

def route_weight(G, route):
    return sum([G[route[i]][route[i+1]][0]['weight'] for i in range(len(route)-1)])

def coordinates_to_graph_nodes(G, route):
    route_nodes = []
    last_point = []

    for point in route['geometry']['coordinates']:
        #If possible that the user make the mistake putiing the same point in the visualizer
        if last_point == point: 
            continue

        route_nodes.append(ox.get_nearest_node(G, [point[1], point[0]]))
        last_point = point

    return route_nodes
