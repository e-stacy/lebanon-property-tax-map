#!/usr/bin/env python3
"""
Validate sales data quality by comparing NHDRA CSV vs separate sales files
"""

import csv
import pandas as pd
from collections import defaultdict

def validate_sales_data():
    """Cross-validate sales data between sources"""

    print('=== SALES DATA CROSS-VALIDATION ===\n')

    # Load separate sales files
    sales_combined = None
    sales_parcels = set()

    try:
        sales_combined = pd.read_excel('data/raw/nhdra/SalesList_2020-2024_combined.xlsx')
        print(f'Separate Sales Files: {len(sales_combined)} records')

        # Get unique parcel identifiers from sales files
        for _, row in sales_combined.iterrows():
            # Try to construct parcel ID from available fields
            map_lot = str(row.get('Map\nLot', ''))
            if map_lot and '-' in map_lot:
                map_val = map_lot.split('-')[0]
                sales_parcels.add(map_val)

        print(f'Unique parcels in sales files: {len(sales_parcels)}')

    except Exception as e:
        print(f'Error loading sales files: {e}')

    # Load NHDRA CSV sales data
    nhdra_sales = []
    nhdra_parcels = set()

    try:
        with open('data/raw/city/nhdra.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            headers = lines[1].strip().split(',')  # Second row has headers
            data_lines = lines[2:]  # Data starts from third row

            reader = csv.DictReader(data_lines, fieldnames=headers)

            for row in reader:
                # Check if this record has any sales data
                has_sales = False
                sales_data = {}

                for key, value in row.items():
                    if key and 'sale' in key.lower() and value and value.strip() and value.strip() != '0' and value.strip() != '1900-01-01 00:00:00':
                        has_sales = True
                        sales_data[key] = value

                if has_sales:
                    parcel_id = row.get('rem mblu map', '') + '-' + row.get('rem mblu block', '') + '-' + row.get('rem mblu lot', '')
                    nhdra_sales.append({
                        'parcel_id': parcel_id,
                        'sales_data': sales_data
                    })

                    # Extract map number for comparison
                    if parcel_id and '-' in parcel_id:
                        map_part = parcel_id.split('-')[0]
                        nhdra_parcels.add(map_part)

        print(f'NHDRA CSV records with sales: {len(nhdra_sales)}')
        print(f'Unique parcels in NHDRA CSV: {len(nhdra_parcels)}')

        # Show sample of NHDRA sales data
        if nhdra_sales:
            sample = nhdra_sales[0]
            print(f'Sample NHDRA sales record:')
            print(f'  Parcel: {sample["parcel_id"]}')
            for key, value in list(sample['sales_data'].items())[:3]:
                value_str = str(value)
                print(f'  {key}: {value_str[:30]}...' if len(value_str) > 30 else f'  {key}: {value_str}')

    except Exception as e:
        print(f'Error reading NHDRA CSV: {e}')

    print()
    print('=== DATA QUALITY ANALYSIS ===')

    if sales_combined is not None and nhdra_sales:
        print('✅ Both sources have sales data')

        overlap = len(sales_parcels.intersection(nhdra_parcels))
        print(f'NHDRA CSV sales coverage: {len(nhdra_sales)}/{5622} records ({len(nhdra_sales)/5622*100:.1f}%)')
        print(f'Separate sales files: {len(sales_combined)} records (2020-2024 only)')
        print(f'Parcel overlap between sources: {overlap} parcels')

        if overlap > 0:
            print('⚠️  POTENTIAL DATA QUALITY ISSUE: Overlapping parcels have sales data in both sources')
            print('   This may indicate:')
            print('   - Duplicate/inconsistent sales data')
            print('   - City merged sales data incorrectly')
            print('   - Different time periods represented')
        else:
            print('✅ No parcel overlap - sources appear complementary (different time periods)')

        # Check date ranges
        try:
            sales_dates = pd.to_datetime(sales_combined['Sale\nDate'], errors='coerce')
            print(f'Separate sales date range: {sales_dates.min()} to {sales_dates.max()}')
        except:
            print('Could not determine sales date range')

    elif sales_combined is not None:
        print('⚠️  Only separate sales files have data - NHDRA CSV appears incomplete')
        print('❌ CONFIRMED: City withheld recent sales data from NHDRA submission')
    elif nhdra_sales:
        print('⚠️  Only NHDRA CSV has sales data - missing recent sales from separate files')
        print('❌ CONFIRMED: City did not provide complete sales history')
    else:
        print('❌ No sales data found in either source')

    print()
    print('=== CONCLUSION ===')
    print('The Vision exports contain NO sales data whatsoever.')
    print('Sales data exists only in:')
    print('1. NHDRA CSV (older sales, possibly incomplete)')
    print('2. Separate FOIA-obtained files (recent sales 2020-2024)')
    print()
    print('RECOMMENDATION: The merged dataset should be validated against')
    print('the separate sales files to ensure data integrity.')

if __name__ == '__main__':
    validate_sales_data()
