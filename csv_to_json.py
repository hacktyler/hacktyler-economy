#!/usr/bin/env python

import csv
import json

reader = csv.DictReader(open('BP_2009_00A1/clean.csv'))

data = {}

def create_obj_for_row(row):
    obj = {}

    obj['id'] = row['naics_code']
    obj['name'] = row['naics_label']
    obj['data'] = {
        'establishments': row['establishments'],
        'paid_employees': row['paid_employees'],
        'first_quarter_payroll': row['first_quarter_payroll'],
        'annual_payroll_thousands': row['annual_payroll_thousands'],
        '$area': row['establishments']
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

