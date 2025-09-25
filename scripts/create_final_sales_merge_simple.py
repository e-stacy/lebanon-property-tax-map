#!/usr/bin/env python3
"""
Create final merged sales dataset - simplified approach
"""

import pandas as pd

def create_final_sales_merge_simple():
    """Create the final merged sales dataset using a simpler approach"""

    print('=== CREATING FINAL SALES DATA MERGE (SIMPLE) ===\n')

    # Load data sources
    nhdra_csv = pd.read_excel('data/processed/nhdra_csv_comprehensive_sales.xlsx')
    annual_combined = pd.read_excel('data/processed/comprehensive_sales_2020-2024.xlsx')

    print(f'Loaded NHDRA CSV: {len(nhdra_csv)} records')
    print(f'Loaded Annual Combined: {len(annual_combined)} records')

    # Prepare the three tiers separately

    # Tier 1: 2025 to 10/1/2024 from NHDRA CSV
    tier1 = nhdra_csv[
        (nhdra_csv['sale_date'] >= pd.Timestamp('2024-10-01')) &
        (nhdra_csv['sale_price'] > 0) &
        (nhdra_csv['sale_date'] > pd.Timestamp('1900-01-01'))
    ].copy()
    tier1['data_source'] = 'nhdra_csv_2025'
    tier1['strategy_tier'] = 'Tier 1: 2025+ Recent'

    # Tier 2: 10/1/2019 to 9/30/2024 from Annual Combined (highest quality)
    annual_combined['sale_date'] = pd.to_datetime(annual_combined['Sale\nDate'], errors='coerce')
    annual_combined['sale_price'] = pd.to_numeric(
        annual_combined['Verified\nPrice'].replace('[\$,]', '', regex=True),
        errors='coerce'
    )

    tier2 = annual_combined[
        (annual_combined['sale_date'] >= pd.Timestamp('2019-10-01')) &
        (annual_combined['sale_date'] <= pd.Timestamp('2024-09-30')) &
        (annual_combined['sale_price'] > 0) &
        (annual_combined['sale_date'] > pd.Timestamp('1900-01-01'))
    ].copy()

    # Rename columns for consistency
    column_rename = {
        'Map\nLot': 'parcel_id',
        'Sale\nDate': 'sale_date',
        'Verified\nPrice': 'original_price_display',
        'Address': 'property_address',
        'Deed\nType': 'deed_type',
        'Grantor': 'grantor',
        'Grantee': 'grantee',
        'Current\nAssed': 'current_assessed',
        'Previous\nAssed': 'previous_assessed',
        'Ratio': 'assessment_ratio',
        'Prop\nCode': 'property_code'
    }

    tier2 = tier2.rename(columns=column_rename)
    tier2['data_source'] = 'annual_combined_2019_2024'
    tier2['strategy_tier'] = 'Tier 2: 2019-2024 Verified'

    # Tier 3: Before 10/1/2019 from NHDRA CSV
    tier3 = nhdra_csv[
        (nhdra_csv['sale_date'] < pd.Timestamp('2019-10-01')) &
        (nhdra_csv['sale_price'] > 0) &
        (nhdra_csv['sale_date'] > pd.Timestamp('1900-01-01'))
    ].copy()
    tier3['data_source'] = 'nhdra_csv_historical'
    tier3['strategy_tier'] = 'Tier 3: Pre-2019 Historical'

    # Combine using append (more reliable than concat)
    print('\nCombining tiers...')
    final_df = tier1._append(tier2, ignore_index=True, sort=False)
    final_df = final_df._append(tier3, ignore_index=True, sort=False)

    print(f'Combined dataset: {len(final_df)} records')

    # Remove duplicates
    original_count = len(final_df)
    final_df = final_df.drop_duplicates(subset=['parcel_id', 'sale_date', 'sale_price'])
    duplicates_removed = original_count - len(final_df)

    print(f'Removed {duplicates_removed} duplicates')

    # Add year column for analysis
    final_df['sale_year'] = final_df['sale_date'].dt.year

    # Final statistics
    print(f'\nFINAL MERGED SALES DATASET:')
    print(f'  Total sales: {len(final_df)}')
    print(f'  Unique parcels: {final_df["parcel_id"].nunique()}')
    print(f'  Date range: {final_df["sale_date"].min()} to {final_df["sale_date"].max()}')

    # Sales by tier
    print(f'\nSales by Strategy Tier:')
    tier_counts = final_df['strategy_tier'].value_counts()
    for tier, count in tier_counts.items():
        print(f'  {tier}: {count} sales')

    # Sales by year
    print(f'\nSales by Year:')
    year_counts = final_df['sale_year'].value_counts().sort_index()
    for year, count in year_counts.items():
        print(f'  {year}: {count} sales')

    # Save the final dataset
    output_file = 'data/processed/final_property_sales_dataset.xlsx'
    final_df.to_excel(output_file, index=False)

    print(f'\n✅ Final merged sales dataset saved to: {output_file}')
    print(f'   Records: {len(final_df)}')
    print(f'   Columns: {len(final_df.columns)}')

    # Show sample
    print(f'\nSample records:')
    sample_cols = ['parcel_id', 'sale_date', 'sale_price', 'data_source', 'strategy_tier']
    sample = final_df[sample_cols].head(5)
    for _, row in sample.iterrows():
        date_str = row['sale_date'].strftime('%Y-%m-%d') if pd.notna(row['sale_date']) else 'N/A'
        price_str = f"${row['sale_price']:,.0f}" if pd.notna(row['sale_price']) else 'N/A'
        print(f'  {row["parcel_id"]}: {date_str} {price_str} ({row["data_source"]})')

    return final_df

if __name__ == '__main__':
    merged_data = create_final_sales_merge_simple()

    print(f'\n🎯 MERGE COMPLETE!')
    print(f'Property tax map now has comprehensive sales data for citizen analysis.')
    print(f'Dataset includes verified transactions from 2019-2025 with historical context.')
