#!/usr/bin/env python3
"""
Validate sales price consistency between NHDRA CSV and separate sales files
"""

import csv
import pandas as pd
from collections import defaultdict

def validate_sales_prices():
    """Compare sales prices between NHDRA CSV and separate sales files"""

    print('=== SALES PRICE VALIDATION ===\n')

    # Load NHDRA CSV sales data
    nhdra_sales_data = {}
    nhdra_records_processed = 0

    try:
        with open('data/raw/city/nhdra.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            headers = lines[1].strip().split(',')  # Second row has headers
            data_lines = lines[2:]  # Data starts from third row

            reader = csv.DictReader(data_lines, fieldnames=headers)

            for row in reader:
                nhdra_records_processed += 1

                # Extract parcel ID
                map_val = row.get('rem mblu map', '').strip()
                block_val = row.get('rem mblu block', '').strip()
                lot_val = row.get('rem mblu lot', '').strip()

                if map_val and block_val and lot_val:
                    parcel_id = f"{map_val}-{block_val}-{lot_val}"

                    # Extract sales data
                    sales_info = {}
                    for key, value in row.items():
                        if key and 'sale' in key.lower():
                            if value and value.strip() and value.strip() != '0':
                                sales_info[key] = value.strip()

                    if sales_info:  # Only include if has sales data
                        nhdra_sales_data[parcel_id] = sales_info

        print(f'NHDRA CSV processed: {nhdra_records_processed} records')
        print(f'NHDRA parcels with sales: {len(nhdra_sales_data)}')

    except Exception as e:
        print(f'Error reading NHDRA CSV: {e}')
        return

    # Load separate sales files
    separate_sales_data = {}
    separate_records_processed = 0

    try:
        sales_combined = pd.read_excel('data/raw/nhdra/SalesList_2020-2024_combined.xlsx')

        for _, row in sales_combined.iterrows():
            separate_records_processed += 1

            # Extract parcel ID from Map\nLot field (note: actual column name has newline)
            map_lot = row['Map\nLot']
            if pd.notna(map_lot) and str(map_lot).strip():
                # Map\nLot format appears to be like "1-1-1" or similar
                parcel_id = str(map_lot).strip()
                sales_price = row['Verified\nPrice']

                # Handle different data types for price
                try:
                    if pd.notna(sales_price) and str(sales_price).strip():
                        # Remove any $ or , characters and convert to float
                        price_str = str(sales_price).replace('$', '').replace(',', '').strip()
                        price_val = float(price_str)
                        if price_val > 0:
                            sale_date = row.get('Sale\nDate')
                            separate_sales_data[parcel_id] = {
                                'price': price_val,
                                'date': str(sale_date) if pd.notna(sale_date) else None,
                                'source': 'separate_files'
                            }
                except (ValueError, TypeError):
                    # Skip invalid price data
                    continue

        print(f'Separate sales files processed: {separate_records_processed} records')
        print(f'Separate parcels with sales: {len(separate_sales_data)}')

    except Exception as e:
        print(f'Error reading separate sales files: {e}')
        return

    # Find overlapping parcels
    nhdra_parcels = set(nhdra_sales_data.keys())
    separate_parcels = set(separate_sales_data.keys())

    overlapping_parcels = nhdra_parcels.intersection(separate_parcels)

    print(f'\n=== OVERLAP ANALYSIS ===')
    print(f'NHDRA parcels: {len(nhdra_parcels)}')
    print(f'Separate sales parcels: {len(separate_parcels)}')
    print(f'Overlapping parcels: {len(overlapping_parcels)}')

    if not overlapping_parcels:
        print('❌ No overlapping parcels found')
        print('\nThis suggests the two datasets cover different time periods or use different parcel ID formats.')

        # Try fuzzy matching - check if any separate sales parcels contain NHDRA map numbers
        print('\n=== FUZZY MATCHING ATTEMPT ===')
        potential_matches = []

        for sep_parcel in separate_parcels:
            sep_map = sep_parcel.split('-')[0] if '-' in sep_parcel else sep_parcel

            # Look for NHDRA parcels that start with the same map number
            matching_nhdra = [p for p in nhdra_parcels if p.startswith(sep_map + '-')]

            if matching_nhdra:
                potential_matches.append((sep_parcel, matching_nhdra[:3]))  # Limit to first 3 matches

        if potential_matches:
            print(f'Found {len(potential_matches)} potential fuzzy matches:')
            for sep, nhdra_list in potential_matches[:10]:  # Show first 10
                print(f'  {sep} → {nhdra_list}')
        else:
            print('No potential fuzzy matches found')

        return

    # Compare sales data for overlapping parcels
    print(f'\n=== SALES PRICE COMPARISON ===')
    print(f'Comparing sales data for {len(overlapping_parcels)} overlapping parcels\n')

    comparison_results = []
    price_discrepancies = []
    date_discrepancies = []

    for parcel_id in sorted(overlapping_parcels):
        nhdra_info = nhdra_sales_data[parcel_id]
        separate_info = separate_sales_data[parcel_id]

        # Extract price from NHDRA (may be in different fields)
        nhdra_price = None
        nhdra_date = None

        for key, value in nhdra_info.items():
            if 'price' in key.lower() and value:
                try:
                    nhdra_price = float(value.replace('$', '').replace(',', ''))
                except:
                    pass
            if 'date' in key.lower() and value and value != '1900-01-01 00:00:00':
                nhdra_date = value

        separate_price = separate_info.get('price')
        separate_date = separate_info.get('date')

        result = {
            'parcel_id': parcel_id,
            'nhdra_price': nhdra_price,
            'separate_price': separate_price,
            'nhdra_date': nhdra_date,
            'separate_date': separate_date,
            'price_match': nhdra_price == separate_price if nhdra_price and separate_price else None,
            'date_match': nhdra_date == separate_date if nhdra_date and separate_date else None
        }

        comparison_results.append(result)

        # Check for discrepancies
        if result['price_match'] is False:
            price_discrepancies.append(result)
        if result['date_match'] is False:
            date_discrepancies.append(result)

    # Report results
    print(f'Total overlapping parcels analyzed: {len(comparison_results)}')

    if price_discrepancies:
        print(f'❌ Price discrepancies found: {len(price_discrepancies)}')
        print('\nPrice Discrepancy Examples:')
        for discrepancy in price_discrepancies[:5]:  # Show first 5
            print(f"  {discrepancy['parcel_id']}: NHDRA=${discrepancy['nhdra_price']:,.0f} vs Separate=${discrepancy['separate_price']:,.0f}")
    else:
        print('✅ No price discrepancies found in overlapping parcels')

    if date_discrepancies:
        print(f'❌ Date discrepancies found: {len(date_discrepancies)}')
        print('\nDate Discrepancy Examples:')
        for discrepancy in date_discrepancies[:3]:  # Show first 3
            print(f"  {discrepancy['parcel_id']}: NHDRA={discrepancy['nhdra_date']} vs Separate={discrepancy['separate_date']}")
    else:
        print('✅ No date discrepancies found in overlapping parcels')

    # Summary
    print(f'\n=== VALIDATION SUMMARY ===')
    if overlapping_parcels:
        consistent_prices = len(comparison_results) - len(price_discrepancies)
        consistent_dates = len(comparison_results) - len(date_discrepancies)

        print(f'Price consistency: {consistent_prices}/{len(comparison_results)} ({consistent_prices/len(comparison_results)*100:.1f}%)')
        print(f'Date consistency: {consistent_dates}/{len(comparison_results)} ({consistent_dates/len(comparison_results)*100:.1f}%)')

        if not price_discrepancies and not date_discrepancies:
            print('✅ EXCELLENT: All overlapping sales data is consistent')
        elif price_discrepancies or date_discrepancies:
            print('⚠️  CONCERNING: Discrepancies found in overlapping data')
            print('   This suggests potential data quality issues in city merging')
    else:
        print('❌ No overlapping parcels to validate')
        print('   Datasets appear to cover different time periods')

if __name__ == '__main__':
    validate_sales_prices()
