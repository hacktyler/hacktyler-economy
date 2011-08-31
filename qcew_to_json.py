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

def create_obj_for_row(row, root_obj):
    obj = {}

    ownership_code = row['ownership_code']
    industry_code = row['industry_code']

    obj['id'] = '%s-%s' % (ownership_code, industry_code)

    if industry_code == '10':
        if ownership_code == '0':
            obj['name'] = 'Total'
        elif ownership_code == '1':
            obj['name'] = 'Federal Government'
        elif ownership_code == '2':
            obj['name'] = 'State Government'
        elif ownership_code == '3':
            obj['name'] = 'Local Government'
        elif ownership_code == '5':
            obj['name'] = 'Private Industry'
    else:
        obj['name'] = '%s' % industry_names[row['industry_code']]

    obj['data'] = {
        'status': row['annual_status_code'],

        'establishments': _int(row['annual_average_number_of_establishments']),
        'paid_employees': _int(row['annual_average_employment']),
        'annual_payroll': _int(row['annual_total_wages']),
        
        '$area': _int(row['annual_total_wages']),
        
        'str_establishments': add_commas(_int(row['annual_average_number_of_establishments'])),
        'str_paid_employees': add_commas(_int(row['annual_average_employment'])),
        'str_annual_payroll': '$%s' % add_commas(_int(row['annual_total_wages'])),
    }

    if root_obj:
        obj['data']['str_establishments_pct'] = '%.2f%%' % (float(obj['data']['establishments']) / root['data']['establishments'] * 100)
        obj['data']['str_paid_employees_pct'] = '%.2f%%' % (float(obj['data']['paid_employees']) / root['data']['paid_employees'] * 100)
        obj['data']['str_annual_payroll_pct'] = '%.2f%%' % (float(obj['data']['annual_payroll']) / root['data']['annual_payroll'] * 100)

    obj['children'] = []

    return obj

# First row is totals
row = reader.next()

root = create_obj_for_row(row, None)
ownership = None
sector = None
subsector = None
industry_group = None

for row in reader:
    ownership_code = row['ownership_code']
    industry_code = row['industry_code']

    # Skip combined government
    if ownership_code == 4:
        continue
    
    obj = create_obj_for_row(row, root)

    # Total row
    if industry_code == '10':
        if ownership:
            if sector:
                if subsector:
                    if industry_group:
                        subsector['children'].append(industry_group)
                        industry_group = None
                        
                    sector['children'].append(subsector)
                    subsector = None

                ownership['children'].append(sector)
                sector = None

            root['children'].append(ownership)

        ownership = obj
    # TODO: invalid NAICS codes?
    elif industry_code[:2] == '10':
        continue
    elif len(industry_code) == 2 or '-' in industry_code:
        if sector:
            if subsector:
                if industry_group:
                    subsector['children'].append(industry_group)
                    industry_group = None
                    
                sector['children'].append(subsector)
                subsector = None

            ownership['children'].append(sector)

        sector = obj
    elif len(industry_code) == 3:
        if subsector:
            if industry_group:
                subsector['children'].append(industry_group)
                industry_group = None

            sector['children'].append(subsector)

        subsector = obj
    elif len(industry_code) == 4:
        if industry_group:
            subsector['children'].append(industry_group)

        industry_group = obj

if industry_group:
    subsector['children'].append(industry_group)

if subsector:
    sector['children'].append(subsector)

if sector:
    ownership['children'].append(sector)

if ownership:
    root['children'].append(ownership)

# Recursively purge incomplete data
def recurse_purge_incomplete(node):
    if len(node['children']) == 0:
        return

    if any([child['data']['status'] == 'N' for child in node['children']]):
        print 'Dropping children of %s' % node['id']
        node['children'] = []

    for child in node['children']:
        recurse_purge_incomplete(child)

recurse_purge_incomplete(root)

# Recursively assign colors
def recurse_assign_colors(node):
    for child in node['children']:
        if len(child['children']) > 0:
            recurse_assign_colors(child)

    colors = color_generator(len(node['children']))

    for child in node['children']:
        child['data']['$color'] = colors.next()

recurse_assign_colors(root)

with open('data.js', 'w') as f:
    f.write('DATA = %s' % json.dumps(root, indent=4))

