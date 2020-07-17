#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import overpy
api = overpy.Overpass()

result = api.query("""[out:json]
[timeout:800]
;
(
  way
    ["amenity"="school"]
    (38.950398154493,-3.956880569458,39.00764626424,-3.8663291931152);
  node
    ["amenity"="school"]
    (38.950398154493,-3.956880569458,39.00764626424,-3.8663291931152);
  relation
    ["amenity"="school"]
    (38.950398154493,-3.956880569458,39.00764626424,-3.8663291931152);
)->.schools;
node(around.schools:50);
out geom;""")

all_nodes_schools = result.nodes

result = api.query("""[out:json]
[timeout:800]
;
(
  way
    ["amenity"="school"]
    (38.950398154493,-3.956880569458,39.00764626424,-3.8663291931152);
  node
    ["amenity"="school"]
    (38.950398154493,-3.956880569458,39.00764626424,-3.8663291931152);
  relation
    ["amenity"="school"]
    (38.950398154493,-3.956880569458,39.00764626424,-3.8663291931152);
)->.schools;
way
  ["highway"]
  (around.schools:20);
node(w)->.nodes;
(
  .nodes;
);
out geom;""")

# nodes_from_roads_near_schools = result.nodes

nodes_from_roads_near_schools_ids = [node.id for node in result.nodes]


final_nodes = []
for node in all_nodes_schools:
    if node.id in nodes_from_roads_near_schools_ids:
        final_nodes.append(node)

print(final_nodes)