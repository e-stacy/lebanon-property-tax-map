#!/usr/bin/env python3
"""
Detailed analysis of sales data discrepancies to understand root causes
"""

import csv
import pandas as pd
from datetime import datetime
from collections import defaultdict

def analyze_sales_discrepancies():
    """Deep dive into sales data discrepancies"""

    print('=== DETAILED SALES DATA ANALYSIS ===\n')

    # Load both datasets
    nhdra_data = {}
    separate_data = defaultdict(list)

    # Load NHDRA
    with open('data/raw/RawData/data/Lebanon/nhdra.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        headers = lines[1].strip().split(',')
        data_lines = lines[2:]

        reader = csv.DictReader(data_lines, fieldnames=headers)
        for row in reader:
            parcel_id = f"{row.get('rem mblu map', '').strip()}-{row.get('rem mblu block', '').strip()}-{row.get('rem mblu lot', '').strip()}"
            if parcel_id and parcel_id != '--':
                nhdra_data[parcel_id] = row

    # Load separate sales
    sales_combined = pd.read_excel('data/raw/RawData/data/NHDRA/SalesList_2020-2024_combined.xlsx')
    for _, row in sales_combined.iterrows():
        map_lot = str(row['Map\nLot']).strip()
        if map_lot:
            sale_date = row.get('Sale\nDate')
            verified_price = row.get('Verified\nPrice')

            if pd.notna(sale_date) and pd.notna(verified_price):
                try:
                    price_val = float(str(verified_price).replace('$', '').replace(',', ''))
                    date_obj = pd.to_datetime(sale_date)
                    separate_data[map_lot].append({
                        'date': date_obj,
                        'price': price_val,
                        'year': date_obj.year
                    })
                except:
                    continue

    # Sort separate sales by date
    for parcel_id in separate_data:
        separate_data[parcel_id].sort(key=lambda x: x['date'], reverse=True)

    # Analyze discrepancies in detail
    overlapping_parcels = set(nhdra_data.keys()) & set(separate_data.keys())
    print(f'Analyzing {len(overlapping_parcels)} overlapping parcels in detail...\n')

    discrepancy_analysis = []

    for parcel_id in sorted(list(overlapping_parcels)[:20]):  # Analyze first 20
        nhdra = nhdra_data[parcel_id]
        separate_sales = separate_data[parcel_id]

        # Extract NHDRA sales
        nhdra_sales = []

        # Current sale
        current_price = nhdra.get('saleprice', '').strip()
        current_date = nhdra.get('saledate', '').strip()
        if current_price and current_date != '1900-01-01 00:00:00':
            try:
                nhdra_sales.append({
                    'date': pd.to_datetime(current_date),
                    'price': float(current_price),
                    'type': 'current'
                })
            except:
                pass

        # Prior sales
        for i in range(1, 4):
            price_key = f'ID{i} Prior Sale Price'
            date_key = f'ID{i} Prior Sale Date'
            price = nhdra.get(price_key, '').strip()
            date = nhdra.get(date_key, '').strip()

            if price and date != '1900-01-01 00:00:00':
                try:
                    nhdra_sales.append({
                        'date': pd.to_datetime(date),
                        'price': float(price),
                        'type': f'prior_{i}'
                    })
                except:
                    pass

        # Compare
        analysis = {
            'parcel_id': parcel_id,
            'nhdra_sales_count': len(nhdra_sales),
            'separate_sales_count': len(separate_sales),
            'nhdra_sales': nhdra_sales,
            'separate_sales': separate_sales,
            'discrepancies': []
        }

        # Check chronological ordering
        if len(nhdra_sales) > 1:
            nhdra_dates = [sale['date'] for sale in nhdra_sales]
            if nhdra_dates != sorted(nhdra_dates, reverse=True):
                analysis['discrepancies'].append('NHDRA sales not in reverse chronological order')

        # Check for date/price matches
        for nhdra_sale in nhdra_sales:
            matches = []
            for sep_sale in separate_sales:
                date_diff = abs((nhdra_sale['date'] - sep_sale['date']).days)
                price_diff_pct = abs(nhdra_sale['price'] - sep_sale['price']) / sep_sale['price'] * 100

                if date_diff <= 30 and price_diff_pct <= 5:  # Within 30 days and 5% price
                    matches.append(sep_sale)

            if not matches:
                analysis['discrepancies'].append(f"No match found for NHDRA sale: {nhdra_sale['date'].date()} ${nhdra_sale['price']:,.0f}")

        discrepancy_analysis.append(analysis)

    # Report findings
    total_discrepancies = sum(len(a['discrepancies']) for a in discrepancy_analysis)
    parcels_with_discrepancies = sum(1 for a in discrepancy_analysis if a['discrepancies'])

    print('DETAILED ANALYSIS RESULTS:')
    print(f'Parcels analyzed: {len(discrepancy_analysis)}')
    print(f'Parcels with discrepancies: {parcels_with_discrepancies} ({parcels_with_discrepancies/len(discrepancy_analysis)*100:.1f}%)')
    print(f'Total discrepancy instances: {total_discrepancies}')

    print('\nSAMPLE DISCREPANCY DETAILS:')
    for analysis in discrepancy_analysis[:5]:
        if analysis['discrepancies']:
            print(f"\n{analysis['parcel_id']}:")
            print(f"  NHDRA sales: {analysis['nhdra_sales_count']} | Separate sales: {analysis['separate_sales_count']}")
            for disc in analysis['discrepancies'][:2]:  # Show first 2 discrepancies
                print(f"  ❌ {disc}")

    # Overall assessment
    print(f'\n=== ROOT CAUSE ANALYSIS ===')

    if parcels_with_discrepancies / len(discrepancy_analysis) > 0.5:
        print('🔴 SEVERE DATA QUALITY ISSUES:')
        print('   - High discrepancy rate suggests systematic problems')
        print('   - City merging process appears fundamentally flawed')
        print('   - NHDRA sales data should NOT be trusted without validation')
    elif parcels_with_discrepancies / len(discrepancy_analysis) > 0.2:
        print('🟡 MODERATE DATA QUALITY ISSUES:')
        print('   - Some discrepancies but many records are accurate')
        print('   - City merging has inconsistencies but is mostly correct')
        print('   - NHDRA sales data usable with caution')
    else:
        print('🟢 GOOD DATA QUALITY:')
        print('   - Low discrepancy rate indicates reliable merging')
        print('   - City data integration appears sound')
        print('   - NHDRA sales data can be trusted')

if __name__ == '__main__':
    analyze_sales_discrepancies()
