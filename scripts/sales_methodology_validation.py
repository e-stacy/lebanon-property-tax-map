#!/usr/bin/env python3
"""
Validate sales data quality using the user's methodology:
1. NHDRA has 3 most recent sales slots
2. 2025 sales should be in most recent slot
3. Pre-2025 sales in chronological order (2nd most recent, then 3rd)
4. 2024-2019 sales should align exactly if no 2025 sales
5. Older sales trusted on face value
"""

import csv
import pandas as pd
from datetime import datetime
from collections import defaultdict

def validate_sales_methodology():
    """Test the user's sales validation methodology"""

    print('=== SALES METHODOLOGY VALIDATION ===\n')

    # Load NHDRA sales data
    nhdra_sales = {}
    nhdra_processed = 0

    try:
        with open('data/raw/RawData/data/Lebanon/nhdra.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            headers = lines[1].strip().split(',')
            data_lines = lines[2:]

            reader = csv.DictReader(data_lines, fieldnames=headers)

            for row in reader:
                nhdra_processed += 1

                # Extract parcel ID
                parcel_id = f"{row.get('rem mblu map', '').strip()}-{row.get('rem mblu block', '').strip()}-{row.get('rem mblu lot', '').strip()}"

                if parcel_id and parcel_id != '--':
                    # Current sale (columns 19-22)
                    current_sale = {
                        'price': row.get('saleprice', '').strip(),
                        'date': row.get('saledate', '').strip(),
                        'qualified': row.get('qualified', '').strip()
                    }

                    # Prior sales (columns 61-69)
                    prior_sales = []
                    for i in range(1, 4):  # ID1, ID2, ID3
                        price_key = f'ID{i} Prior Sale Price'
                        date_key = f'ID{i} Prior Sale Date'

                        price = row.get(price_key, '').strip()
                        date = row.get(date_key, '').strip()

                        if price and date and date != '1900-01-01 00:00:00':
                            prior_sales.append({
                                'price': price,
                                'date': date,
                                'level': i  # 1 = most recent prior, 2 = 2nd most recent, etc.
                            })

                    nhdra_sales[parcel_id] = {
                        'current_sale': current_sale,
                        'prior_sales': prior_sales
                    }

        print(f'NHDRA records processed: {nhdra_processed}')
        print(f'NHDRA parcels with sales data: {len(nhdra_sales)}')

    except Exception as e:
        print(f'Error reading NHDRA: {e}')
        return

    # Load separate sales files (2020-2024)
    separate_sales = defaultdict(list)
    separate_processed = 0

    try:
        sales_combined = pd.read_excel('data/raw/RawData/data/NHDRA/SalesList_2020-2024_combined.xlsx')

        for _, row in sales_combined.iterrows():
            separate_processed += 1

            map_lot = str(row['Map\nLot']).strip()
            if map_lot:
                sale_date = row.get('Sale\nDate')
                verified_price = row.get('Verified\nPrice')

                if pd.notna(sale_date) and pd.notna(verified_price):
                    try:
                        price_val = float(str(verified_price).replace('$', '').replace(',', ''))
                        date_obj = pd.to_datetime(sale_date)

                        separate_sales[map_lot].append({
                            'date': date_obj,
                            'price': price_val,
                            'year': date_obj.year
                        })
                    except (ValueError, TypeError):
                        continue

        # Sort sales by date for each parcel (most recent first)
        for parcel_id in separate_sales:
            separate_sales[parcel_id].sort(key=lambda x: x['date'], reverse=True)

        print(f'Separate sales records processed: {separate_processed}')
        print(f'Separate parcels with sales: {len(separate_sales)}')

    except Exception as e:
        print(f'Error reading separate sales: {e}')
        return

    # Find overlapping parcels
    overlapping_parcels = set(nhdra_sales.keys()) & set(separate_sales.keys())
    print(f'Overlapping parcels: {len(overlapping_parcels)}')

    if not overlapping_parcels:
        print('No overlapping parcels found - cannot validate methodology')
        return

    # Validate methodology on overlapping parcels
    validation_results = []
    error_count = 0

    print(f'\n=== TESTING METHODOLOGY ON {len(overlapping_parcels)} PARCELS ===\n')

    for parcel_id in sorted(list(overlapping_parcels)[:50]):  # Test first 50 for efficiency
        nhdra_data = nhdra_sales[parcel_id]
        separate_data = separate_sales[parcel_id]

        # Extract sales dates from separate data
        separate_dates = [sale['date'] for sale in separate_data]
        separate_years = [sale['year'] for sale in separate_data]

        # Check for 2025 sales
        has_2025_sales = any(year == 2025 for year in separate_years)

        # Build expected NHDRA structure per methodology
        expected_nhdra_sales = []

        if has_2025_sales:
            # 2025 sales should be in current sale slot
            sales_2025 = [sale for sale in separate_data if sale['year'] == 2025]
            if sales_2025:
                expected_nhdra_sales.append({
                    'slot': 'current',
                    'expected_date': sales_2025[0]['date'],
                    'expected_price': sales_2025[0]['price']
                })

            # Pre-2025 sales in chronological order
            pre_2025_sales = [sale for sale in separate_data if sale['year'] < 2025][:2]
            for i, sale in enumerate(pre_2025_sales):
                expected_nhdra_sales.append({
                    'slot': f'prior_{i+1}',
                    'expected_date': sale['date'],
                    'expected_price': sale['price']
                })
        else:
            # No 2025 sales, so 2024-2019 should align with recent sales slots
            recent_sales = separate_data[:3]  # 3 most recent
            for i, sale in enumerate(recent_sales):
                if i == 0:
                    expected_nhdra_sales.append({
                        'slot': 'current',
                        'expected_date': sale['date'],
                        'expected_price': sale['price']
                    })
                else:
                    expected_nhdra_sales.append({
                        'slot': f'prior_{i}',
                        'expected_date': sale['date'],
                        'expected_price': sale['price']
                    })

        # Compare with actual NHDRA data
        issues = []

        # Check current sale
        current_sale = nhdra_data['current_sale']
        if expected_nhdra_sales and expected_nhdra_sales[0]['slot'] == 'current':
            expected = expected_nhdra_sales[0]
            if current_sale['date']:
                try:
                    actual_date = pd.to_datetime(current_sale['date'])
                    expected_date = expected['expected_date']

                    # Allow some date tolerance (same month/year)
                    if abs((actual_date - expected_date).days) > 30:  # More than 30 days difference
                        issues.append(f"Current sale date mismatch: NHDRA={actual_date.date()} vs Expected={expected_date.date()}")
                except:
                    issues.append("Current sale date format issue")

        # Check prior sales
        prior_sales = nhdra_data['prior_sales']
        for i, expected_sale in enumerate(expected_nhdra_sales[1:], 1):  # Skip current sale
            if i <= len(prior_sales):
                actual_sale = prior_sales[i-1]  # NHDRA prior_1 is most recent prior
                try:
                    actual_date = pd.to_datetime(actual_sale['date'])
                    expected_date = expected_sale['expected_date']

                    if abs((actual_date - expected_date).days) > 30:
                        issues.append(f"Prior sale {i} date mismatch: NHDRA={actual_date.date()} vs Expected={expected_date.date()}")
                except:
                    issues.append(f"Prior sale {i} date format issue")

        validation_results.append({
            'parcel_id': parcel_id,
            'has_2025_sales': has_2025_sales,
            'separate_sales_count': len(separate_data),
            'nhdra_current_sale': bool(current_sale['date'] and current_sale['date'] != '1900-01-01 00:00:00'),
            'nhdra_prior_sales': len(prior_sales),
            'issues': issues,
            'error_count': len(issues)
        })

        if issues:
            error_count += 1

    # Summary
    total_tested = len(validation_results)
    error_parcels = sum(1 for r in validation_results if r['error_count'] > 0)

    print('METHODOLOGY VALIDATION RESULTS:')
    print(f'Parcels tested: {total_tested}')
    print(f'Parcels with errors: {error_parcels} ({error_parcels/total_tested*100:.1f}%)')
    print(f'Error-free parcels: {total_tested - error_parcels} ({(total_tested - error_parcels)/total_tested*100:.1f}%)')

    # Show sample errors
    if error_parcels > 0:
        print(f'\nSAMPLE ERRORS (first 5):')
        error_samples = [r for r in validation_results if r['issues']][:5]
        for result in error_samples:
            print(f"  {result['parcel_id']}: {len(result['issues'])} issues")
            for issue in result['issues'][:2]:  # Show first 2 issues per parcel
                print(f"    - {issue}")

    # Overall assessment
    print(f'\n=== METHODOLOGY VALIDITY ASSESSMENT ===')
    if error_parcels / total_tested < 0.1:  # Less than 10% errors
        print('✅ METHODOLOGY LOGICALLY VALID')
        print('   Low error rate suggests correct chronological ordering in NHDRA data')
    elif error_parcels / total_tested < 0.3:  # Less than 30% errors
        print('⚠️ METHODOLOGY PARTIALLY VALID')
        print('   Moderate error rate suggests some data quality issues')
    else:
        print('❌ METHODOLOGY LOGIC FLAWED')
        print('   High error rate suggests fundamental data quality problems')

    print(f'\nData quality confidence: {(total_tested - error_parcels)/total_tested*100:.1f}%')

if __name__ == '__main__':
    validate_sales_methodology()
