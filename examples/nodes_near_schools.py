#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-
import sys
sys.path.append('../src/')

import utilities

bottom_left = [38.954487, -3.958351]
top_right = [39.012350, -3.863268]
amenity = "school"

result = utilities.nodes_near_amenity(bottom_left, top_right, amenity)
print(result) 