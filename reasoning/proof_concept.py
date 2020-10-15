#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import clips
import re
import json
import os
import commodity.path
from scone_client import SconeClient

level = {"Zero" : 0, "Low" : 3, "Medium" : 6, "High" : 10}
amenity_types = ["school"]
amenities = {}

project_dir = commodity.path.get_project_dir('.')
amenities_config_file =  os.path.join(project_dir, 'config/amenities_config_temp.json')
clips_file = os.path.join(project_dir, 'reasoning/clips/schools_proof_concept.clp')


def occupations_from_facts(ocupation_facts):
    occupations = {}

    for ocupation_fact in ocupation_facts:
        occupation_type, ocupation_level = re.split(r'[()]', str(ocupation_fact))[1:-2]
        occupations[occupation_type] = ocupation_level.split()[1]

    return occupations
 
def estimate_danger(amenity_type, occupation_level):
    occupation_types = parse_scone_sentence(scone.query("(list-rel {{is occupied by}} {{{0}}})".format(amenity_type)))

    transmission_risk_levels = {}
    vulnerability_levels = {}

    for occupation_type in occupation_types:
        query = "(the-x-of-y {{measure magnitude}} (the-x-of-y {{COVID-19 vulnerability level}} {{{0}}}))".format(occupation_type)
        response = parse_scone_sentence(scone.query(query))
        vulnerability_levels[occupation_type] = float(response[0])

        query = "(the-x-of-y {{measure magnitude}} (the-x-of-y {{transmission risk level}} {{{0}}}))".format(occupation_type)
        response = parse_scone_sentence(scone.query(query))
        transmission_risk_levels[occupation_type] = float(response[0])

    if occupation_level == 'ZERO':
        return max(vulnerability_levels.values())
    else:
        return max(vulnerability_levels.values()) * max(transmission_risk_levels.values()) * level[occupation_level]

def parse_scone_sentence(sentence):
    return re.findall(r'{(.*?)}', sentence)

if __name__ == "__main__":
    scone = SconeClient(host='localhost', port=6517)  # default params
    env = clips.Environment()
    env.load(clips_file)
    env.reset()

    # env.assert_string('(context (day-of-week Sunday))')
    env.assert_string('(context (day-of-week Friday) (is-class-period YES) (is-public-holiday NO) (time-hour 14) (time-minutes 16))')
    env.run()

    ocupation_facts = [fact for fact in env.facts() if "ocupation" in str(fact)]

    occupations = occupations_from_facts(ocupation_facts)
    print(occupations)


    for amenity_type in amenity_types:
        ocupation_level = occupations["{}-ocupation ".format(amenity_type)]
        danger = estimate_danger(amenity_type, ocupation_level)
        print("Amenity-type: {}\t Danger:{}".format(amenity_type, danger))

        amenities[amenity_type] = {"correction_factor": danger *100,
                                    "danger_level": danger,
                                    "radius": 50}

        with open(amenities_config_file, 'w') as outfile:
            json.dump(amenities, outfile, indent = 4)

    