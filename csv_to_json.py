#!/usr/bin/env python

import colorsys
import csv
import json
import random

reader = csv.DictReader(open('BP_2009_00A1/clean.csv'))

data = {}

def _int(s):
    try:
        return int(s)
    except ValueError:
        return 0

def generate_color():
    for h in range(0, 360, 360 / 20):
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

def create_obj_for_row(row):
    obj = {}

    obj['id'] = row['naics_code']
    obj['name'] = row['naics_label']
    obj['data'] = {
        'establishments': _int(row['establishments']),
        'paid_employees': _int(row['paid_employees']),
        'first_quarter_payroll': _int(row['first_quarter_payroll']),
        'annual_payroll': _int(row['annual_payroll_thousands']) * 1000,
        
        '$area': _int(row['establishments']),
        
        'str_establishments': add_commas(_int(row['establishments'])),
        'str_paid_employees': add_commas(_int(row['paid_employees'])),
        'str_first_quarter_payroll': add_commas(_int(row['first_quarter_payroll'])),
        'str_annual_payroll': '$%s' % add_commas(_int(row['annual_payroll_thousands']) * 1000)
    }
    obj['children'] = []

    return obj

# First row is totals
row = reader.next()

root = create_obj_for_row(row)

colors = generate_color()

for row in reader:
    obj = create_obj_for_row(row)
    obj['data']['$color'] = colors.next()

    obj['data']['str_establishments_pct'] = '%.2f%%' % (float(obj['data']['establishments']) / root['data']['establishments'] * 100),
    obj['data']['str_paid_employees_pct'] = '%.2f%%' % (float(obj['data']['paid_employees']) / root['data']['paid_employees'] * 100),
    obj['data']['str_first_quarter_payroll_pct'] = '%.2f%%' % (float(obj['data']['first_quarter_payroll']) / root['data']['first_quarter_payroll'] * 100),
    obj['data']['str_annual_payroll_pct'] = '%.2f%%' % (float(obj['data']['annual_payroll']) / root['data']['annual_payroll'] * 100),

    root['children'].append(obj)

with open('data.js', 'w') as f:
    f.write('DATA = %s' % json.dumps(root))

