#!/usr/bin/env python3
"""
Compare sales data across all Lebanon folder files to check data quality and merging accuracy
"""

import csv

def analyze_sales_data():
    """Analyze sales data across all Lebanon folder files"""

    files_to_check = [
        'data/raw/city/parcels.csv',
        'data/raw/city/buildings.csv',
        'data/raw/city/land.csv',
        'data/raw/city/nhdra.csv'
    ]

    print('=== SALES DATA COMPARISON ACROSS LEBANON FILES ===\n')

    all_sales_data = {}

    for file_path in files_to_check:
        filename = file_path.split('/')[-1].upper()
        print(f'{filename}:')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if 'nhdra.csv' in file_path:
                    # Special handling for NHDRA format
                    lines = f.readlines()
                    headers = lines[1].strip().split(',')  # Second row has headers
                    data_lines = lines[2:]  # Data starts from third row
                    reader = csv.DictReader(data_lines, fieldnames=headers)
                else:
                    reader = csv.DictReader(f)

                # Count records and check for sales data
                record_count = 0
                sales_fields = []
                sample_sales_data = []
                sales_records_with_data = 0

                for row in reader:
                    record_count += 1

                    # Look for sales-related fields
                    has_sales_data = False
                    for key, value in row.items():
                        if key and 'sale' in key.lower() and value and value.strip() and value.strip() != '0' and value.strip() != '1900-01-01 00:00:00':
                            has_sales_data = True
                            if key not in sales_fields:
                                sales_fields.append(key)
                            if len(sample_sales_data) < 2:
                                sample_sales_data.append(f'{key}: {value}')

                    if has_sales_data:
                        sales_records_with_data += 1

                print(f'  Total Records: {record_count}')
                print(f'  Records with Sales Data: {sales_records_with_data}')
                print(f'  Sales Fields Found: {len(sales_fields)}')
                if sales_fields:
                    print(f'  Sales Field Names: {sales_fields[:3]}...')  # Show first 3
                    if sample_sales_data:
                        print(f'  Sample: {sample_sales_data[0][:60]}...')
                else:
                    print('  No sales data found')

                all_sales_data[filename] = {
                    'total_records': record_count,
                    'sales_records': sales_records_with_data,
                    'sales_fields': len(sales_fields),
                    'field_names': sales_fields[:5]
                }

        except Exception as e:
            print(f'  Error: {e}')
            all_sales_data[filename] = {'error': str(e)}
        print()

    # Summary comparison
    print('=== SALES DATA SUMMARY ===')
    print('File                     | Records | With Sales | Sales Fields')
    print('-------------------------|---------|------------|-------------')
    for filename, data in all_sales_data.items():
        if 'error' not in data:
            print('<25')
        else:
            print('<25')

    # Check if NHDRA sales data matches Vision sales data
    print('\n=== SALES DATA QUALITY CHECK ===')

    # Compare with the separate sales files
    try:
        import pandas as pd
        sales_combined = pd.read_excel('data/raw/nhdra/SalesList_2020-2024_combined.xlsx')

        print(f'Separate NHDRA Sales Files: {len(sales_combined)} records')

        # Check if the Vision exports have any sales data
        vision_has_sales = any(data.get('sales_records', 0) > 0 for data in all_sales_data.values() if 'error' not in data)
        nhdra_has_sales = all_sales_data.get('NHDRA.CSV', {}).get('sales_records', 0) > 0

        print(f'Vision exports have sales data: {"Yes" if vision_has_sales else "No"}')
        print(f'NHDRA CSV has sales data: {"Yes" if nhdra_has_sales else "No"}')

        if not vision_has_sales and nhdra_has_sales:
            print('❌ CONFIRMED: City did NOT include sales data in Vision exports')
            print('✅ Sales data only available in separate NHDRA files')

    except Exception as e:
        print(f'Could not check separate sales files: {e}')

if __name__ == '__main__':
    analyze_sales_data()
