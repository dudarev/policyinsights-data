import csv
import json
import os

from slugify import slugify


CENSUS_2010_FILE = '~/data/census/2010/DEC_10_DP_DPDP1.csv'
JSON_FILE = 'locations.json'


CONTENT_TEMPLATE = """# {name}

FIPS_code: {FIPS_code}
population: {population}
population_K12: {population_K12}
population_K12_percent: {population_K12_percent:.2f}
population_children: {population_children}
population_children_percent: {population_children_percent:.2f}
population_seniors: {population_seniors}
population_seniors_percent: {population_seniors_percent:.2f}
"""

data = []

with open(os.path.expanduser(CENSUS_2010_FILE), encoding='latin1') as f:
    csv_read = csv.reader(f)
    next(csv_read)
    pk = 1
    for line in csv_read:
        obj = {
            "model": "locations.location",
            "pk": pk,
        }
        pk += 1
        FIPS_code = line[1]
        name = line[2]
        slug = slugify(name, ok='_', lower=False)
        population = {
            'total': line[3],
            'under_5': line[5],
            '5_9': line[7],
            '10_14': line[9],
            '15_19': line[11],
            '60_64': line[29],
            '65_69': line[31],
            '70_74': line[33],
            '75_79': line[35],
            '80_84': line[37],
            '85_and_over': line[39],
        }
        for k, v in population.items():
            population[k] = int(v)
        population_K12 = population['5_9'] + population['10_14'] + population['15_19']
        population_children = population_K12 + population['under_5']
        population_seniors = population['60_64'] + population['65_69'] + population['70_74'] + \
            population['75_79'] + population['80_84'] + population['85_and_over']
        fields = {
            "slug": slug,
            "fips_code": FIPS_code,
            "content": CONTENT_TEMPLATE.format(
                name=name,
                FIPS_code=FIPS_code,
                population=population['total'], population_K12=population_K12,
                population_K12_percent=population_K12 / population['total'] * 100,
                population_children=population_children,
                population_children_percent=population_children / population['total'] * 100,
                population_seniors=population_seniors,
                population_seniors_percent=population_seniors / population['total'] * 100
            ),
        }
        obj.update({'fields': fields})
        data.append(obj)
        print(name)
        print('slug: {}'.format(slug))
        print('FIPS_code: {}'.format(FIPS_code))
        print('population: {}'.format(population['total']))
        print('population_K12: {}'.format(population_K12))
        print('population_K12_percent: {0:.2f}'.format(population_K12 / population['total'] * 100))
        print('population_children: {}'.format(population_children))
        print('population_children_percent: {0:.2f}'.format(
            population_children / population['total'] * 100))
        print('population_seniors: {}'.format(population_seniors))
        print('population_seniors_percent: {0:.2f}'.format(
            population_seniors / population['total'] * 100))
        print(40 * '-')


with open(JSON_FILE, 'w') as f:
    json.dump(data, f, indent=2)
