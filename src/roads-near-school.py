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

for node in result.nodes:
    print(node)


