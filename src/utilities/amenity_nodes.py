#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import overpy

def nodes_near_amenity(bottom_left, top_right, amenity):
  north, south, east, west = top_right[0], bottom_left[0], bottom_left[1], top_right[1]
  api = overpy.Overpass()
  radius = 50

  query = """[out:json]
              [timeout:800]
              ;
              (
                way
                  ["amenity"="{amenity}"]
                  ({south}, {east}, {north}, {west});
                node
                  ["amenity"="{amenity}"]
                  ({south}, {east}, {north}, {west});
                relation
                  ["amenity"="{amenity}"]
                  ({south}, {east}, {north}, {west});
              )->.amenities;
              node(around.amenities:{radius});
              out geom;""".format(amenity=amenity, north=north, south=south, east=east, west=west, radius=radius)
  result = api.query(query)
  all_nodes_near_amenities = result.nodes

  query = """[out:json]
            [timeout:800]
            ;
            (
              way
                ["amenity"="{amenity}"]
                ({south}, {east}, {north}, {west});
              node
                ["amenity"="{amenity}"]
                ({south}, {east}, {north}, {west});
              relation
                ["amenity"="{amenity}"]
                ({south}, {east}, {north}, {west});
            )->.amenities;
            way
              ["highway"]
              (around.amenities:{radius});
            node(w)->.nodes;
            (
              .nodes;
            );
            out geom;""".format(amenity=amenity,north=north, south=south, east=east, west=west, radius=radius)
  result = api.query(query)


  nodes_from_roads_near_amenities_ids = [node.id for node in result.nodes]
  final_nodes = []
  for node in all_nodes_near_amenities:
      if node.id in nodes_from_roads_near_amenities_ids:
          final_nodes.append(node)

  return(final_nodes)

