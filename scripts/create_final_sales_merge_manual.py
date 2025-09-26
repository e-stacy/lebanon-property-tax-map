#!/usr/bin/env python3
"""
Create final merged sales dataset - manual approach to avoid pandas concat issues
"""

import pandas as pd
import csv

def create_final_sales_merge_manual():
    """Create the final merged sales dataset using manual CSV writing"""

    print('=== CREATING FINAL SALES DATA MERGE (MANUAL) ===\n')

    # Load data sources
    nhdra_csv = pd.read_excel('data/processed/nhdra_csv_comprehensive_sales.xlsx')
    annual_combined = pd.read_excel('data/processed/comprehensive_sales_2020-2024.xlsx')

    print(f'Loaded NHDRA CSV: {len(nhdra_csv)} records')
    print(f'Loaded Annual Combined: {len(annual_combined)} records')

    # Prepare data for manual merging
    all_sales_records = []

    # Tier 1: 2025 to 10/1/2024 from NHDRA CSV
    print('Processing Tier 1: 2025+ sales from NHDRA CSV...')
    tier1_mask = (
        (nhdra_csv['sale_date'] >= pd.Timestamp('2024-10-01')) &
        (nhdra_csv['sale_price'] > 0) &
        (nhdra_csv['sale_date'] > pd.Timestamp('1900-01-01'))
    )
    tier1_sales = nhdra_csv[tier1_mask]

    for _, row in tier1_sales.iterrows():
        record = {
            'parcel_id': row['parcel_id'],
            'sale_date': row['sale_date'].strftime('%Y-%m-%d') if pd.notna(row['sale_date']) else '',
            'sale_price': float(row['sale_price']) if pd.notna(row['sale_price']) else 0,
            'data_source': 'nhdra_csv_2025',
            'strategy_tier': 'Tier 1: 2025+ Recent',
            'sale_type': row.get('sale_type', ''),
            'qualified': row.get('qualified', ''),
            'book_page': row.get('book_page', '')
        }
        all_sales_records.append(record)

    print(f'  Added {len(tier1_sales)} Tier 1 sales')

    # Tier 2: 10/1/2019 to 9/30/2024 from Annual Combined
    print('Processing Tier 2: 2019-2024 verified sales...')
    annual_combined['sale_date'] = pd.to_datetime(annual_combined['Sale\nDate'], errors='coerce')
    annual_combined['sale_price'] = pd.to_numeric(
        annual_combined['Verified\nPrice'].replace('[\$,]', '', regex=True),
        errors='coerce'
    )

    tier2_mask = (
        (annual_combined['sale_date'] >= pd.Timestamp('2019-10-01')) &
        (annual_combined['sale_date'] <= pd.Timestamp('2024-09-30')) &
        (annual_combined['sale_price'] > 0) &
        (annual_combined['sale_date'] > pd.Timestamp('1900-01-01'))
    )
    tier2_sales = annual_combined[tier2_mask]

    for _, row in tier2_sales.iterrows():
        record = {
            'parcel_id': row.get('Map\nLot', ''),
            'sale_date': row['sale_date'].strftime('%Y-%m-%d') if pd.notna(row['sale_date']) else '',
            'sale_price': float(row['sale_price']) if pd.notna(row['sale_price']) else 0,
            'data_source': 'annual_combined_2019_2024',
            'strategy_tier': 'Tier 2: 2019-2024 Verified',
            'sale_type': 'verified_transaction',
            'property_address': row.get('Address', ''),
            'deed_type': row.get('Deed\nType', ''),
            'grantor': row.get('Grantor', ''),
            'grantee': row.get('Grantee', ''),
            'current_assessed': row.get('Current\nAssed', ''),
            'previous_assessed': row.get('Previous\nAssed', ''),
            'assessment_ratio': row.get('Ratio', ''),
            'property_code': row.get('Prop\nCode', '')
        }
        all_sales_records.append(record)

    print(f'  Added {len(tier2_sales)} Tier 2 sales')

    # Tier 3: Before 10/1/2019 from NHDRA CSV
    print('Processing Tier 3: Pre-2019 historical sales...')
    tier3_mask = (
        (nhdra_csv['sale_date'] < pd.Timestamp('2019-10-01')) &
        (nhdra_csv['sale_price'] > 0) &
        (nhdra_csv['sale_date'] > pd.Timestamp('1900-01-01'))
    )
    tier3_sales = nhdra_csv[tier3_mask]

    for _, row in tier3_sales.iterrows():
        record = {
            'parcel_id': row['parcel_id'],
            'sale_date': row['sale_date'].strftime('%Y-%m-%d') if pd.notna(row['sale_date']) else '',
            'sale_price': float(row['sale_price']) if pd.notna(row['sale_price']) else 0,
            'data_source': 'nhdra_csv_historical',
            'strategy_tier': 'Tier 3: Pre-2019 Historical',
            'sale_type': row.get('sale_type', ''),
            'qualified': row.get('qualified', ''),
            'book_page': row.get('book_page', '')
        }
        all_sales_records.append(record)

    print(f'  Added {len(tier3_sales)} Tier 3 sales')

    # Remove duplicates manually
    print('\nRemoving duplicates...')
    seen = set()
    unique_records = []

    for record in all_sales_records:
        key = f"{record['parcel_id']}|{record['sale_date']}|{record['sale_price']}"
        if key not in seen:
            seen.add(key)
            unique_records.append(record)

    duplicates_removed = len(all_sales_records) - len(unique_records)
    print(f'  Removed {duplicates_removed} duplicates')

    # Write to CSV manually
    output_file = 'data/processed/sales.csv'

    if unique_records:
        # Collect all possible fieldnames
        all_fieldnames = set()
        for record in unique_records:
            all_fieldnames.update(record.keys())
        fieldnames = sorted(list(all_fieldnames))

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique_records)

    print(f'\n✅ Final merged sales dataset saved to: {output_file}')
    print(f'   Records: {len(unique_records)}')
    print(f'   Fields: {len(fieldnames) if unique_records else 0}')

    # Summary statistics
    total_sales = len(unique_records)

    # Count by tier
    tier_counts = {}
    for record in unique_records:
        tier = record.get('strategy_tier', 'Unknown')
        tier_counts[tier] = tier_counts.get(tier, 0) + 1

    print(f'\nFINAL DATASET SUMMARY:')
    print(f'  Total Sales: {total_sales}')
    print(f'  Unique Parcels: {len(set(r["parcel_id"] for r in unique_records))}')

    print(f'\nSales by Strategy Tier:')
    for tier, count in tier_counts.items():
        print(f'  {tier}: {count} sales ({count/total_sales*100:.1f}%)')

    # Show sample records
    print(f'\nSample Records:')
    for i, record in enumerate(unique_records[:3]):
        date_str = record.get('sale_date', 'N/A')
        price_str = f"${record.get('sale_price', 0):,.0f}"
        print(f'  {i+1}. {record["parcel_id"]}: {date_str} {price_str} ({record["data_source"]})')

    return unique_records

if __name__ == '__main__':
    merged_data = create_final_sales_merge_manual()

    print(f'\n🎯 MERGE COMPLETE!')
    print(f'Created comprehensive sales dataset with {len(merged_data)} records')
    print(f'for citizen property tax analysis.')
