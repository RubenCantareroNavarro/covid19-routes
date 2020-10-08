#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-


def compare_routes(route1, route2, danger_points_data):
    route1_danger_points = number_danger_points_in_route(danger_points_data, route1)
    route2_danger_points = number_danger_points_in_route(danger_points_data, route2)

    return [route1_danger_points, route2_danger_points]


def number_danger_points_in_route(danger_points_data, route):
    cont = 0
    danger_points = []
    for feature in danger_points_data['features']:
        danger_points.append(feature['geometry']['coordinates'])

    for point in route['geometry']['coordinates']: 
        if(point in danger_points):
            cont += 1

    return cont