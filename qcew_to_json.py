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
    obj['name'] = industry_names[row['industry_code']]
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
sectors = {}
subsectors = {}
industry_groups = {}
industries = {}

for row in reader:
    obj = create_obj_for_row(row, root, None)

    # Deal with odd-ball two sector groupings
    if '-' in obj['id']:
        sectors.append(obj)
    # Skip national industry divisions
    if len(obj['id']) == 6:
        continue
    elif len(obj['id']) == 5:
        industries.append(obj)
    elif len(obj['id']) == 4:
        industry_groups.append(obj)
    elif len(obj['id']) == 3:
        subsectors.append(obj)
    elif len(obj['id']) == 2:
        sectors.append(obj)

with open('data.js', 'w') as f:
    f.write('DATA = %s' % json.dumps(root))

