#!/usr/bin/env python3
"""
Debug parcel ID creation and extraction
"""

import csv
import pandas as pd

def debug_parcel_extraction():
    print("=== DEBUGGING PARCEL ID CREATION ===")

    # Read the NHDRA CSV and find parcel 50-40
    with open('data/raw/city/nhdra.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        headers = lines[1].strip().split(',')  # Second row has actual headers

        reader = csv.DictReader(lines[2:], fieldnames=headers)  # Skip first two rows

        found_50_40 = False
        count = 0
        for row in reader:
            parcel_id = f"{row.get('rem mblu map', '').strip()}-{row.get('rem mblu block', '').strip()}-{row.get('rem mblu lot', '').strip()}"

            if parcel_id == '50-40':
                found_50_40 = True
                print(f'Found parcel 50-40: {parcel_id}')
                print(f'  Map: {row.get("rem mblu map", "N/A")}')
                print(f'  Block: {row.get("rem mblu block", "N/A")}')
                print(f'  Lot: {row.get("rem mblu lot", "N/A")}')

                # Check sales data
                current_price = row.get('saleprice', '').strip()
                current_date = row.get('saledate', '').strip()
                print(f'  Current sale price: {current_price}')
                print(f'  Current sale date: {current_date}')

                for i in range(1, 4):
                    price_key = f'ID{i} Prior Sale Price'
                    date_key = f'ID{i} Prior Sale Date'
                    price = row.get(price_key, '').strip()
                    date = row.get(date_key, '').strip()
                    print(f'  Prior {i} sale price: {price}, date: {date}')
                break

            count += 1
            if count > 1000:  # Don't read the whole file
                break

        if not found_50_40:
            print('Parcel 50-40 not found in first 1000 rows')

    print("\n=== CHECKING PARCEL ID FORMAT ===")
    # Read a few more to see the format
    with open('data/raw/city/nhdra.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        reader = csv.DictReader(lines[2:], fieldnames=headers)

        for i, row in enumerate(reader):
            if i >= 5:  # Just check first 5
                break
            map_val = row.get('rem mblu map', '').strip()
            block_val = row.get('rem mblu block', '').strip()
            lot_val = row.get('rem mblu lot', '').strip()
            parcel_id = f'{map_val}-{block_val}-{lot_val}'
            print(f'Row {i}: Map={map_val}, Block={block_val}, Lot={lot_val} -> Parcel ID: {parcel_id}')

if __name__ == '__main__':
    debug_parcel_extraction()
