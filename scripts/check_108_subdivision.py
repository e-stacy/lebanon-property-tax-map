#!/usr/bin/env python3
"""
Check the 108-* subdivision structure.
"""

import csv

def check_108_subdivision():
    parcels_108 = []
    with open('data/processed/parcels.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['parcel_id'].startswith('108-') and row['parcel_id'] != '108-14':
                parcels_108.append({
                    'id': row['parcel_id'],
                    'address': row['situs_address'],
                    'class': row['class_code'],
                    'value': float(row['total_value'] or 0),
                    'style': row['nhdra_vns style desc'],
                    'acres': float(row['lot_size_acres'] or 0)
                })

    print(f'108-* parcels (excluding 108-14): {len(parcels_108)}')

    # Group by class
    by_class = {}
    for parcel in parcels_108:
        cls = parcel['class']
        if cls not in by_class:
            by_class[cls] = []
        by_class[cls].append(parcel)

    print('\nBy class:')
    for cls, parcels in by_class.items():
        total_value = sum(p['value'] for p in parcels)
        total_acres = sum(p['acres'] for p in parcels)
        print(f'  Class {cls}: {len(parcels)} parcels, {total_acres:.2f} acres, ${total_value:,.0f} total value')

    print('\nSample parcels:')
    for parcel in parcels_108[:10]:
        print(f'  {parcel["id"]}: {parcel["address"]} - Class {parcel["class"]} - {parcel["acres"]:.2f} acres - ${parcel["value"]:,.0f} - {parcel["style"]}')

if __name__ == '__main__':
    check_108_subdivision()
