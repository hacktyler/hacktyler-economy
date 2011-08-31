#!/usr/bin/env python

import json

data = open('data.js', 'r').read()
data = data[6:]

root = json.loads(data)

def recurse_test_totals(node):
    if len(node['children']) == 0:
        return

    expected_establishments = node['data']['establishments']
    sum_establishments = sum([child['data']['establishments'] for child in node['children']])

    if expected_establishments != sum_establishments:
        print '%s: %s != %s' % (node['id'], expected_establishments, sum_establishments)

    for child in node['children']:
        recurse_test_totals(child)

recurse_test_totals(root)

