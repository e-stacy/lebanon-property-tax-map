#!/usr/bin/env python3
"""
Create final merged sales dataset using the validated strategy
"""

import pandas as pd
from datetime import datetime

def create_final_sales_merge():
    """Create the final merged sales dataset following the validated strategy"""

    print('=== CREATING FINAL SALES DATA MERGE ===\n')

    # Load all data sources
    print('Loading data sources...')

    # NHDRA CSV (comprehensive historical data)
    nhdra_csv = pd.read_excel('data/processed/nhdra_csv_comprehensive_sales.xlsx')
    print(f'✅ NHDRA CSV: {len(nhdra_csv)} records')

    # Annual Combined (high-quality recent data)
    annual_combined = pd.read_excel('data/processed/comprehensive_sales_2020-2024.xlsx')
    annual_combined['sale_date'] = pd.to_datetime(annual_combined['Sale\nDate'], errors='coerce')
    print(f'✅ Annual Combined: {len(annual_combined)} records')

    # Implement the validated strategy
    merged_sales = []

    print('\nImplementing validated sales strategy...')

    # Tier 1: 2025 to 10/1/2024 → NHDRA CSV (only source available)
    print('Tier 1: 2025 to 10/1/2024 from NHDRA CSV...')
    tier1_sales = nhdra_csv[
        (nhdra_csv['sale_date'] >= pd.Timestamp('2024-10-01')) &
        (nhdra_csv['sale_date'] <= pd.Timestamp('2025-12-31')) &
        (nhdra_csv['sale_price'] > 0) &
        (nhdra_csv['sale_date'] > pd.Timestamp('1900-01-01'))
    ].copy()

    tier1_sales['data_source'] = 'nhdra_csv_2025'
    tier1_sales['strategy_tier'] = 'Tier 1: 2025+ Recent'
    merged_sales.append(tier1_sales)
    print(f'  Added {len(tier1_sales)} sales from 2025+')

    # Tier 2: 10/1/2019 to 9/30/2024 → Annual Combined (highest quality)
    print('Tier 2: 10/1/2019 to 9/30/2024 from Annual Combined...')
    tier2_sales = annual_combined[
        (annual_combined['sale_date'] >= pd.Timestamp('2019-10-01')) &
        (annual_combined['sale_date'] <= pd.Timestamp('2024-09-30'))
    ].copy()

    # Convert price column and filter valid sales
    tier2_sales['sale_price'] = pd.to_numeric(
        tier2_sales['Verified\nPrice'].replace('[\$,]', '', regex=True),
        errors='coerce'
    )

    tier2_sales = tier2_sales[
        (tier2_sales['sale_price'] > 0) &
        (tier2_sales['sale_price'].notna())
    ]

    # Standardize columns to match NHDRA CSV format
    column_mapping = {
        'Map\nLot': 'parcel_id',
        'Sale\nDate': 'sale_date',
        'Verified\nPrice': 'original_price_display',
        'sale_price': 'sale_price',
        'Address': 'property_address',
        'Deed\nType': 'deed_type',
        'Grantor': 'grantor',
        'Grantee': 'grantee',
        'Current\nAssed': 'current_assessed',
        'Previous\nAssed': 'previous_assessed',
        'Ratio': 'assessment_ratio',
        'Prop\nCode': 'property_code',
        'Source_Year': 'source_year'
    }

    tier2_sales = tier2_sales.rename(columns=column_mapping)

    tier2_sales['data_source'] = 'annual_combined_2019_2024'
    tier2_sales['strategy_tier'] = 'Tier 2: 2019-2024 Verified'
    tier2_sales['sale_type'] = 'verified_transaction'  # These are actual transaction records

    merged_sales.append(tier2_sales)
    print(f'  Added {len(tier2_sales)} verified sales from 2019-2024')

    # Tier 3: Before 10/1/2019 → NHDRA CSV (historical data)
    print('Tier 3: Before 10/1/2019 from NHDRA CSV...')
    tier3_sales = nhdra_csv[
        (nhdra_csv['sale_date'] < pd.Timestamp('2019-10-01')) &
        (nhdra_csv['sale_price'] > 0) &
        (nhdra_csv['sale_date'] > pd.Timestamp('1900-01-01'))
    ].copy()

    tier3_sales['data_source'] = 'nhdra_csv_historical'
    tier3_sales['strategy_tier'] = 'Tier 3: Pre-2019 Historical'
    merged_sales.append(tier3_sales)
    print(f'  Added {len(tier3_sales)} historical sales from pre-2019')

    # Combine all tiers more carefully
    print('\nCombining all sales data...')

    # Create a list to hold all records as dictionaries
    all_records = []

    for df in merged_sales:
        for _, row in df.iterrows():
            record = {
                'parcel_id': row.get('parcel_id'),
                'sale_date': row.get('sale_date'),
                'sale_price': row.get('sale_price'),
                'data_source': row.get('data_source'),
                'strategy_tier': row.get('strategy_tier')
            }

            # Add any additional columns that exist
            for col in df.columns:
                if col not in record and pd.notna(row.get(col)):
                    record[col] = row.get(col)

            all_records.append(record)

    # Create final DataFrame from records
    final_sales_df = pd.DataFrame(all_records)

    # Remove duplicates based on parcel_id, sale_date, and sale_price
    original_count = len(final_sales_df)
    final_sales_df = final_sales_df.drop_duplicates(subset=['parcel_id', 'sale_date', 'sale_price'])
    duplicates_removed = original_count - len(final_sales_df)

    if duplicates_removed > 0:
        print(f'  Removed {duplicates_removed} duplicate sales')

    # Sort by parcel and date
    final_sales_df = final_sales_df.sort_values(['parcel_id', 'sale_date'])

    print(f'\nFINAL MERGED SALES DATASET:')
    print(f'  Total sales: {len(final_sales_df)}')
    print(f'  Unique parcels: {final_sales_df["parcel_id"].nunique()}')

    # Sales by strategy tier
    print(f'\nSales by Strategy Tier:')
    tier_counts = final_sales_df['strategy_tier'].value_counts()
    for tier, count in tier_counts.items():
        print(f'  {tier}: {count} sales')

    # Sales by year
    final_sales_df['sale_year'] = final_sales_df['sale_date'].dt.year
    print(f'\nSales by Year:')
    year_counts = final_sales_df['sale_year'].value_counts().sort_index()
    for year, count in year_counts.items():
        print(f'  {year}: {count} sales')

    # Data quality summary
    print(f'\nData Quality Summary:')
    valid_prices = (final_sales_df['sale_price'] > 0).sum()
    valid_dates = (final_sales_df['sale_date'] > pd.Timestamp('1900-01-01')).sum()
    print(f'  Valid prices: {valid_prices}/{len(final_sales_df)} ({valid_prices/len(final_sales_df)*100:.1f}%)')
    print(f'  Valid dates: {valid_dates}/{len(final_sales_df)} ({valid_dates/len(final_sales_df)*100:.1f}%)')

    # Save the final merged dataset
    output_file = 'data/processed/final_merged_sales_dataset.xlsx'
    final_sales_df.to_excel(output_file, index=False)

    print(f'\n✅ Final merged sales dataset saved to: {output_file}')
    print(f'   Records: {len(final_sales_df)}')
    print(f'   Columns: {len(final_sales_df.columns)}')
    print(f'   Date range: {final_sales_df["sale_date"].min()} to {final_sales_df["sale_date"].max()}')

    # Show sample of the merged data
    print(f'\nSample of merged data:')
    sample_cols = ['parcel_id', 'sale_date', 'sale_price', 'data_source', 'strategy_tier']
    sample = final_sales_df[sample_cols].head(5)
    for _, row in sample.iterrows():
        print(f'  {row["parcel_id"]}: {row["sale_date"].date()} ${row["sale_price"]:,.0f} ({row["data_source"]})')

    # Create summary statistics
    summary_stats = {
        'total_sales': len(final_sales_df),
        'unique_parcels': final_sales_df['parcel_id'].nunique(),
        'date_range_start': final_sales_df['sale_date'].min(),
        'date_range_end': final_sales_df['sale_date'].max(),
        'tier_breakdown': tier_counts.to_dict(),
        'year_breakdown': year_counts.to_dict(),
        'quality_metrics': {
            'valid_prices_pct': valid_prices/len(final_sales_df)*100,
            'valid_dates_pct': valid_dates/len(final_sales_df)*100
        }
    }

    return final_sales_df, summary_stats

if __name__ == '__main__':
    merged_data, stats = create_final_sales_merge()

    print(f'\n🎯 MERGE COMPLETE!')
    print(f'Your property tax map now has {stats["total_sales"]} comprehensive sales records')
    print(f'across {stats["unique_parcels"]} parcels from {stats["date_range_start"].year} to {stats["date_range_end"].year}')
