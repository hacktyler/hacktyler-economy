#!/usr/bin/env python

"""
Validates that all "steps" in the hierarchy sum correctly.

Some private industry groups (ownership == 5) genuinely
don't sum up to 100% by very small margins.
"""

import json

data = open('assets/data.js', 'r').read()
data = data[6:]

root = json.loads(data)

def recurse_test_totals(node):
    if len(node['children']) == 0:
        return

    for datum in ['establishments', 'paid_employees', 'annual_payroll']:
        expected = node['data'][datum]
        total = sum([child['data'][datum] for child in node['children']])

        if expected != total:
            print '[%s] %s: %s != %s' % (datum.upper(), node['id'], expected, total)

    for child in node['children']:
        recurse_test_totals(child)

recurse_test_totals(root)

