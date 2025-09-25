#!/usr/bin/env python3
"""
Compare sales data alignment between NHDRA CSV (city data) and comprehensive annual files
Focus on 2019-2025 sales as requested, treating pre-2019 as truth
"""

import pandas as pd
from datetime import datetime
import numpy as np

def compare_sales_alignment():
    """Compare sales alignment between city NHDRA CSV and annual NHDRA files"""

    print('=== SALES ALIGNMENT COMPARISON (2019-2025) ===\n')

    # Load the two comprehensive sales datasets
    try:
        # NHDRA CSV sales (city-submitted data)
        nhdra_csv_sales = pd.read_excel('data/processed/nhdra_csv_comprehensive_sales.xlsx')

        # Comprehensive annual sales (NHDRA-provided data)
        annual_sales = pd.read_excel('data/processed/comprehensive_sales_2020-2024.xlsx')

    except FileNotFoundError as e:
        print(f'Error: Required file not found: {e}')
        return

    # Filter to 2019-2025 sales only (as requested)
    nhdra_filtered = nhdra_csv_sales[
        (nhdra_csv_sales['sale_date'].dt.year >= 2019) &
        (nhdra_csv_sales['sale_date'].dt.year <= 2025)
    ].copy()

    # Convert Sale\nDate to datetime for filtering
    annual_sales['sale_date_dt'] = pd.to_datetime(annual_sales['Sale\nDate'], errors='coerce')

    annual_filtered = annual_sales[
        (annual_sales['sale_date_dt'].dt.year >= 2019) &
        (annual_sales['sale_date_dt'].dt.year <= 2025)
    ].copy()

    print(f'NHDRA CSV sales (2019-2025): {len(nhdra_filtered)} records')
    print(f'Annual sales (2019-2025): {len(annual_filtered)} records')

    # Standardize column names for comparison
    annual_filtered = annual_filtered.rename(columns={
        'Map\nLot': 'parcel_id',
        'Source_Year': 'source_year'
    })

    # Convert price to numeric
    annual_filtered['sale_price'] = pd.to_numeric(
        annual_filtered['Verified\nPrice'].replace('[\$,]', '', regex=True),
        errors='coerce'
    )

    # Keep the datetime column as sale_date
    annual_filtered['sale_date'] = annual_filtered['sale_date_dt']

    # Add source identifier
    nhdra_filtered['data_source'] = 'nhdra_csv'
    annual_filtered['data_source'] = 'annual_files'

    # Create comparison key (parcel_id + date + price)
    def create_comparison_key(row):
        date_str = row['sale_date'].strftime('%Y-%m-%d') if pd.notna(row['sale_date']) else 'none'
        price_str = f"{float(row['sale_price']):.0f}" if pd.notna(row['sale_price']) and not pd.isna(row['sale_price']) else 'none'
        return f"{row['parcel_id']}|{date_str}|{price_str}"

    nhdra_filtered['comparison_key'] = nhdra_filtered.apply(create_comparison_key, axis=1)
    annual_filtered['comparison_key'] = annual_filtered.apply(create_comparison_key, axis=1)

    # Find matches and mismatches
    nhdra_keys = set(nhdra_filtered['comparison_key'])
    annual_keys = set(annual_filtered['comparison_key'])

    matching_sales = nhdra_keys.intersection(annual_keys)
    nhdra_only = nhdra_keys - annual_keys
    annual_only = annual_keys - nhdra_keys

    print(f'\n=== ALIGNMENT RESULTS ===')
    print(f'Perfectly matching sales: {len(matching_sales)}')
    print(f'NHDRA CSV only: {len(nhdra_only)}')
    print(f'Annual files only: {len(annual_only)}')
    print(f'Total sales compared: {len(nhdra_filtered) + len(annual_filtered)}')
    print(f'Alignment rate: {len(matching_sales) / (len(nhdra_filtered) + len(annual_filtered)) * 100:.2f}%')

    # Detailed analysis by year
    print(f'\n=== YEAR-BY-YEAR ANALYSIS ===')
    years = range(2019, 2026)

    year_stats = []
    for year in years:
        nhdra_year = nhdra_filtered[nhdra_filtered['sale_date'].dt.year == year]
        annual_year = annual_filtered[annual_filtered['sale_date_dt'].dt.year == year]

        nhdra_count = len(nhdra_year)
        annual_count = len(annual_year)

        # Find matches for this year
        if nhdra_count > 0 and annual_count > 0:
            nhdra_year_keys = set(nhdra_year['comparison_key'])
            annual_year_keys = set(annual_year['comparison_key'])
            matches = len(nhdra_year_keys.intersection(annual_year_keys))
            match_rate = matches / (nhdra_count + annual_count) * 100 if (nhdra_count + annual_count) > 0 else 0
        else:
            matches = 0
            match_rate = 0

        year_stats.append({
            'year': year,
            'nhdra_count': nhdra_count,
            'annual_count': annual_count,
            'matches': matches,
            'match_rate': match_rate
        })

        status = '✅' if match_rate > 80 else '⚠️' if match_rate > 50 else '❌'
        print('<6')

    # Identify major discrepancies
    print(f'\n=== MAJOR DISCREPANCIES ===')

    # Find parcels with multiple sales in one source but not the other
    nhdra_parcel_counts = nhdra_filtered.groupby('parcel_id').size()
    annual_parcel_counts = annual_filtered.groupby('parcel_id').size()

    # Parcels with sales in both sources
    common_parcels = set(nhdra_parcel_counts.index) & set(annual_parcel_counts.index)

    discrepancy_details = []
    for parcel in list(common_parcels)[:20]:  # Sample first 20
        nhdra_sales = nhdra_parcel_counts[parcel]
        annual_sales = annual_parcel_counts[parcel]

        if abs(nhdra_sales - annual_sales) > 1:  # Significant difference
            discrepancy_details.append({
                'parcel_id': parcel,
                'nhdra_sales': nhdra_sales,
                'annual_sales': annual_sales,
                'difference': abs(nhdra_sales - annual_sales)
            })

    if discrepancy_details:
        print('Parcels with significant sales count differences:')
        for detail in discrepancy_details[:10]:
            print(f'  {detail["parcel_id"]}: NHDRA={detail["nhdra_sales"]}, Annual={detail["annual_sales"]} (diff={detail["difference"]})')

    # Create detailed mismatch report
    print(f'\n=== SAMPLE MISMATCH DETAILS ===')

    # Show some examples of mismatches
    mismatch_examples = []

    # NHDRA-only sales (recent years)
    nhdra_only_recent = nhdra_filtered[
        nhdra_filtered['sale_date'].dt.year >= 2020
    ]

    for _, sale in nhdra_only_recent.head(5).iterrows():
        mismatch_examples.append({
            'type': 'NHDRA_CSV_ONLY',
            'parcel_id': sale['parcel_id'],
            'date': sale['sale_date'].strftime('%Y-%m-%d') if pd.notna(sale['sale_date']) else 'N/A',
            'price': f"${sale['sale_price']:,.0f}" if pd.notna(sale['price']) else 'N/A',
            'year': sale['sale_year']
        })

    # Annual-only sales
    for _, sale in annual_filtered.head(5).iterrows():
        mismatch_examples.append({
            'type': 'ANNUAL_ONLY',
            'parcel_id': sale['parcel_id'],
            'date': sale['sale_date'].strftime('%Y-%m-%d') if pd.notna(sale['sale_date']) else 'N/A',
            'price': f"${sale['sale_price']:,.0f}" if pd.notna(sale['price']) else 'N/A',
            'year': sale['sale_date'].dt.year if pd.notna(sale['sale_date']) else 'N/A'
        })

    for example in mismatch_examples[:10]:
        print(f'  {example["type"]:15} | {example["parcel_id"]:12} | {example["date"]:10} | {example["price"]:12}')

    # Save detailed report
    output_path = 'data/processed/sales_alignment_report.xlsx'

    # Create summary DataFrame
    summary_data = []
    for year_stat in year_stats:
        summary_data.append({
            'Year': year_stat['year'],
            'NHDRA_CSV_Count': year_stat['nhdra_count'],
            'Annual_Files_Count': year_stat['annual_count'],
            'Matching_Sales': year_stat['matches'],
            'Match_Rate_%': round(year_stat['match_rate'], 2)
        })

    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(output_path, index=False)

    print(f'\n✅ Detailed alignment report saved to: {output_path}')

    return {
        'total_nhdra': len(nhdra_filtered),
        'total_annual': len(annual_filtered),
        'matches': len(matching_sales),
        'nhdra_only': len(nhdra_only),
        'annual_only': len(annual_only),
        'year_stats': year_stats
    }

if __name__ == '__main__':
    compare_sales_alignment()
