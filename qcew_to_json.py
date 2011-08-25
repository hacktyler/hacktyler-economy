#!/usr/bin/env python

import colorsys
import csv
import json
import random
import sys

reader = csv.reader(open('qcew/industry_codes.csv'))

industry_names = {}
for row in reader:
    industry_names[row[0]] = row[1]

reader = csv.DictReader(open('qcew/qcew_smith.csv'))

data = {}

def _int(s):
    try:
        return int(s)
    except ValueError:
        return 0

def color_generator(n):
    for h in range(0, 360, 360 / n):
        h = float(h) / 360
        s = (90 + 10 * random.random()) / 200 
        l = (30 + 70 * random.random()) / 200

        rgb = colorsys.hls_to_rgb(h, l, s)
        rgb = map(lambda n: n * 255, rgb)

        yield '#%02x%02x%02x' % tuple(rgb)

def splitthousands(s, sep=','):  
    if len(s) <= 3: return s  
    return splitthousands(s[:-3], sep) + sep + s[-3:]

def add_commas(n):
    return splitthousands(str(n), ',')

def create_obj_for_row(row, root_obj, color):
    obj = {}

    obj['id'] = row['industry_code']
    obj['name'] = '%s (%s)' % (industry_names[row['industry_code']], row['industry_code'])
    obj['data'] = {
        'establishments': _int(row['annual_average_number_of_establishments']),
        'paid_employees': _int(row['annual_average_employment']),
        'annual_payroll': _int(row['annual_total_wages']),
        
        '$area': _int(row['annual_average_number_of_establishments']),
        
        'str_establishments': add_commas(_int(row['annual_average_number_of_establishments'])),
        'str_paid_employees': add_commas(_int(row['annual_average_employment'])),
        'str_annual_payroll': '$%s' % add_commas(_int(row['annual_total_wages'])),
    }

    if root_obj:
        obj['data']['str_establishments_pct'] = '%.2f%%' % (float(obj['data']['establishments']) / root['data']['establishments'] * 100),
        obj['data']['str_paid_employees_pct'] = '%.2f%%' % (float(obj['data']['paid_employees']) / root['data']['paid_employees'] * 100),
        obj['data']['str_annual_payroll_pct'] = '%.2f%%' % (float(obj['data']['annual_payroll']) / root['data']['annual_payroll'] * 100),

    if color:
        obj['data']['$color'] = color

    obj['children'] = []

    return obj

# First row is totals
row = reader.next()

#colors = color_generator(360)

root = create_obj_for_row(row, None, None)
groups = {
    'federal_gov': {},
    'state_gov': {},
    'local_gov': {},
    'private': {}
}

for g in groups:
    groups[g] = {
        'sectors': {},
        'subsectors': {},
        'industry_groups': {},
        'industries': {}
    }

for row in reader:
    obj = create_obj_for_row(row, root, None)

    if row['ownership_code'] == '1':
        ownership = 'federal_gov'
    elif row['ownership_code'] == '2':
        ownership = 'state_gov']
    elif row['ownership_code'] == '3':
        ownership = 'local_gov']
    elif row['ownership_code'] == '5':
        ownership = 'private'
    else:
        continue

    industry_code = obj['id']

    # Deal with odd-ball two sector groupings
    if '-' in industry_code:
        groups[ownership]['sectors'][industry_code] = obj
    # Skip national industry divisions
    if len(industry_code) == 6:
        continue
    elif len(industry_code) == 5:
        groups[ownership]['industries'][industry_code] = obj
    elif len(industry_code) == 4:
        groups[ownership]['industry_groups'][industry_code] = obj
    elif len(industry_code) == 3:
        groups[ownership]['subsectors'][industry_code] = obj
    elif len(industry_code) == 2:
        groups[ownership]['sectors'][industry_code] = obj

for subsector in subsectors.values():
    sector_code = subsector['id'][:2]

    # Handle sectors that are grouped
    if sector_code in ['31', '32', '33']:
        sector_code = '31-33'
    elif sector_code in ['44', '45']:
        sector_code = '44-45'
    elif sector_code in ['48', '49']:
        sector_code = '48-49'

    sectors[sector_code]['children'].append(subsector)

for sector in sectors.values():
    root['children'].append(sector)

with open('data.js', 'w') as f:
    f.write('DATA = %s' % json.dumps(root, indent=4))

