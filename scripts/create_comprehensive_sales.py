#!/usr/bin/env python3
"""
Create a comprehensive sales database by compiling all annual sales files
"""

import pandas as pd
import os
from pathlib import Path

def create_comprehensive_sales():
    """Compile all annual sales files into one comprehensive database"""

    print('=== CREATING COMPREHENSIVE SALES DATABASE ===\n')

    sales_dir = Path('data/raw/nhdra')
    annual_files = [
        'SalesList - 2020.xlsx',
        'SalesList - 2021.xlsx',
        'SalesList - 2022.xlsx',
        'SalesList - 2023.xlsx',
        'SalesList - 2024.xlsx'
    ]

    all_sales = []
    total_records = 0

    print('Processing annual sales files:')
    for filename in annual_files:
        filepath = sales_dir / filename
        if filepath.exists():
            try:
                df = pd.read_excel(filepath)
                year = filename.split(' - ')[1].split('.')[0]  # Extract year from filename
                df['Source_Year'] = year
                df['Source_File'] = filename

                all_sales.append(df)
                total_records += len(df)
                print(f'  ✅ {filename}: {len(df)} records')

                # Validate Map Lot column exists
                if 'Map\nLot' not in df.columns:
                    print(f'  ⚠️  Warning: Map Lot column not found in {filename}')
                else:
                    non_null_map_lot = df['Map\nLot'].notna().sum()
                    print(f'     Map Lot coverage: {non_null_map_lot}/{len(df)} ({non_null_map_lot/len(df)*100:.1f}%)')

            except Exception as e:
                print(f'  ❌ Error reading {filename}: {e}')
        else:
            print(f'  ❌ File not found: {filename}')

    if not all_sales:
        print('No sales files could be processed')
        return

    # Combine all sales data
    print(f'\nCombining {len(all_sales)} annual files...')
    comprehensive_df = pd.concat(all_sales, ignore_index=True)

    print(f'Comprehensive database created: {len(comprehensive_df)} total records')

    # Data quality checks
    print('\n=== DATA QUALITY SUMMARY ===')

    # Map Lot coverage
    map_lot_coverage = comprehensive_df['Map\nLot'].notna().sum()
    print(f'Map Lot coverage: {map_lot_coverage}/{len(comprehensive_df)} ({map_lot_coverage/len(comprehensive_df)*100:.1f}%)')

    # Price data coverage
    price_coverage = comprehensive_df['Verified\nPrice'].notna().sum()
    print(f'Price coverage: {price_coverage}/{len(comprehensive_df)} ({price_coverage/len(comprehensive_df)*100:.1f}%)')

    # Date coverage
    date_coverage = comprehensive_df['Sale\nDate'].notna().sum()
    print(f'Date coverage: {date_coverage}/{len(comprehensive_df)} ({date_coverage/len(comprehensive_df)*100:.1f}%)')

    # Records by year
    print(f'\nRecords by year:')
    year_counts = comprehensive_df['Source_Year'].value_counts().sort_index()
    for year, count in year_counts.items():
        print(f'  {year}: {count} records')

    # Unique parcels
    unique_parcels = comprehensive_df['Map\nLot'].nunique()
    print(f'\\nUnique parcels with sales: {unique_parcels}')

    # Save comprehensive file
    output_path = 'data/processed/comprehensive_sales_2020-2024.xlsx'
    try:
        comprehensive_df.to_excel(output_path, index=False)
        print(f'\\n✅ Comprehensive sales database saved to: {output_path}')
        print(f'   File size: {len(comprehensive_df)} records, {len(comprehensive_df.columns)} columns')
    except Exception as e:
        print(f'❌ Error saving file: {e}')

    # Create summary statistics
    print(f'\n=== SALES SUMMARY STATISTICS ===')

    # Price statistics (clean data)
    price_data = pd.to_numeric(comprehensive_df['Verified\nPrice'], errors='coerce')
    price_data = price_data.dropna()

    if len(price_data) > 0:
        print(f'Price statistics (valid entries: {len(price_data)}):')
        print(f'  Mean: ${price_data.mean():,.0f}')
        print(f'  Median: ${price_data.median():,.0f}')
        print(f'  Min: ${price_data.min():,.0f}')
        print(f'  Max: ${price_data.max():,.0f}')

        # Price distribution
        print(f'  Price ranges:')
        print(f'    Under $100K: {len(price_data[price_data < 100000])}')
        print(f'    $100K-$500K: {len(price_data[(price_data >= 100000) & (price_data < 500000)])}')
        print(f'    $500K-$1M: {len(price_data[(price_data >= 500000) & (price_data < 1000000)])}')
        print(f'    Over $1M: {len(price_data[price_data >= 1000000])}')

    return comprehensive_df

if __name__ == '__main__':
    create_comprehensive_sales()
