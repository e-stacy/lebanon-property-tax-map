#!/usr/bin/env python3
"""
Examine parcel 4-23-706 to understand phantom sales issue
"""

import pandas as pd

def examine_parcel():
    # Read the comparison data
    df = pd.read_csv('data/processed/nhdra_sales_comparison.csv')

    # Find parcel 4-23-706
    parcel_data = df[df['parcel_id'] == '4-23-706']
    print('=== PARCEL 4-23-706 ANALYSIS ===')
    print()

    for _, row in parcel_data.iterrows():
        print(f"{row['comparison_type']}:")
        print(f"  Current Sale: {row['current_sale_date']} - ${row['current_sale_price']} - {row['current_qualified']} - {row['current_book_page']}")
        print(f"  Prior 1: {row['prior1_sale_date']} - ${row['prior1_sale_price']} - {row['prior1_book_page']}")
        print(f"  Prior 2: {row['prior2_sale_date']} - ${row['prior2_sale_price']} - {row['prior2_book_page']}")
        print(f"  Prior 3: {row['prior3_sale_date']} - ${row['prior3_sale_price']} - {row['prior3_book_page']}")
        print(f"  Notes: {row['data_quality_notes']}")
        print()

    # Also check the raw comprehensive sales data for this parcel
    print('=== RAW COMPREHENSIVE SALES DATA ===')
    sales_df = pd.read_csv('data/processed/final_property_sales_dataset.csv')
    parcel_sales = sales_df[sales_df['parcel_id'] == '4-23-706'].sort_values('sale_date')
    print(f"Found {len(parcel_sales)} sales in comprehensive data:")
    for _, sale in parcel_sales.iterrows():
        print(f"  {sale['sale_date']} - ${sale['sale_price']} - {sale.get('book_page', 'N/A')} - {sale['data_source']} - {sale['strategy_tier']}")
    print()

    # Check original NHDRA data
    print('=== ORIGINAL NHDRA DATA ===')
    nhdra_df = pd.read_csv('data/raw/city/nhdra.csv', header=1)
    nhdra_parcel = nhdra_df[(nhdra_df['rem mblu map'] == '4') &
                           (nhdra_df['rem mblu block'] == '23') &
                           (nhdra_df['rem mblu lot'] == '706')]

    if not nhdra_parcel.empty:
        row = nhdra_parcel.iloc[0]
        print("Original NHDRA sales data:")
        print(f"  Current: {row.get('saledate')} - ${row.get('saleprice')} - {row.get('book pg')}")
        print(f"  Prior1: {row.get('ID1 Prior Sale Date')} - ${row.get('ID1 Prior Sale Price')} - {row.get('ID1 Prior Book Page')}")
        print(f"  Prior2: {row.get('ID2 Prior Sale Date')} - ${row.get('ID2 Prior Sale Price')} - {row.get('ID2 Prior Book Page')}")
        print(f"  Prior3: {row.get('ID3 Prior Sale Date')} - ${row.get('ID3 Prior Sale Price')} - {row.get('ID3 Prior Book Page')}")
    else:
        print("Parcel not found in original NHDRA data")

if __name__ == '__main__':
    examine_parcel()
