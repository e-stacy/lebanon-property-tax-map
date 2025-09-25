#!/usr/bin/env python3
"""
Check for condo parcels on Mountain View Drive.
"""

import csv

def check_mountain_view_condos():
    mountain_view_condos = []
    with open('data/processed/parcels.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['class_code'] == '102V' and 'MOUNTAIN VIEW' in row['situs_address']:
                mountain_view_condos.append({
                    'id': row['parcel_id'],
                    'address': row['situs_address'],
                    'value': float(row['total_value'] or 0)
                })

    print(f'Mountain View Drive condos: {len(mountain_view_condos)}')
    for condo in mountain_view_condos[:10]:
        print(f'  {condo["id"]}: {condo["address"]} - ${condo["value"]:,.0f}')
    if len(mountain_view_condos) > 10:
        print(f'  ... and {len(mountain_view_condos) - 10} more')

if __name__ == '__main__':
    check_mountain_view_condos()
