#!/usr/bin/env python3
# -*- coding: utf-8; mode: python3; -*-

import clips
import re


def occupations_from_facts(ocupancy_facts):
    occupations = {}

    for ocupancy_fact in ocupancy_facts:
        ocupancy_type, ocupancy_level = re.split(r'[()]', str(ocupancy_fact))[1:-2]
        occupations[ocupancy_type] = ocupancy_level.split()[1]

    return occupations



if __name__ == "__main__":
    env = clips.Environment()
    env.load('schools_proof_concept.clp')
    env.reset()

    env.assert_string('(context (day-of-week Sunday))')
    env.run()

    ocupancy_facts = [fact for fact in env.facts() if "ocupation" in str(fact)]

    occupations = occupations_from_facts(ocupancy_facts)
    print(occupations)
