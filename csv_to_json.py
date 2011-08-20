#!/usr/bin/env python

import csv
import json

reader = csv.DictReader(open('BP_2009_00A1/clean.csv'))

data = {}

def _int(s):
    try:
        return int(s)
    except ValueError:
        return 0

def create_obj_for_row(row):
    obj = {}

    obj['id'] = row['naics_code']
    obj['name'] = row['naics_label']
    obj['data'] = {
        'establishments': _int(row['establishments']),
        'paid_employees': _int(row['paid_employees']),
        'first_quarter_payroll': _int(row['first_quarter_payroll']),
        'annual_payroll_thousands': _int(row['annual_payroll_thousands']),
        '$area': _int(row['establishments'])
    }
    obj['children'] = []

    return obj

# First row is totals
row = reader.next()

root = create_obj_for_row(row)

for row in reader:
    root['children'].append(create_obj_for_row(row))

with open('data.js', 'w') as f:
    f.write('DATA = %s' % json.dumps(root))

