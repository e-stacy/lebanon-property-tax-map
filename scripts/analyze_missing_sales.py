#!/usr/bin/env python3
"""
Analyze why some sales are missing from comprehensive data
"""

import pandas as pd

def analyze_missing():
    # Check what the nhdra_csv_historical source contains
    sales_df = pd.read_csv('data/processed/final_property_sales_dataset.csv')
    historical_sales = sales_df[sales_df['data_source'] == 'nhdra_csv_historical']
    parcel_historical = historical_sales[historical_sales['parcel_id'] == '4-23-706']

    print('Historical NHDRA data for parcel 4-23-706:')
    for _, sale in parcel_historical.iterrows():
        print(f'  {sale["sale_date"]} - ${sale["sale_price"]} - {sale.get("book_page", "N/A")}')

    print()
    print(f'Total historical sales across all parcels: {len(historical_sales)}')
    print(f'Unique parcels in historical data: {historical_sales["parcel_id"].nunique()}')

    # Check annual data
    annual_sales = sales_df[sales_df['data_source'] == 'annual_combined_2019_2024']
    parcel_annual = annual_sales[annual_sales['parcel_id'] == '4-23-706']

    print()
    print('Annual combined data for parcel 4-23-706:')
    for _, sale in parcel_annual.iterrows():
        print(f'  {sale["sale_date"]} - ${sale["sale_price"]} - {sale.get("book_page", "N/A")}')

    # Compare with original NHDRA
    print()
    print('Original NHDRA data for comparison:')
    nhdra_df = pd.read_csv('data/raw/RawData/data/Lebanon/nhdra.csv', header=1)
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

    print()
    print('ANALYSIS:')
    print('The original NHDRA has 4 sales, but comprehensive data only has 2.')
    print('Missing from comprehensive:')
    print('1. Second 2015 sale (different book/page) - may not be in historical extract')
    print('2. 1996 $0 sale - likely filtered out as $0 value')
    print('3. The annual data has the 2021 sale with different date (filing delay)')

if __name__ == '__main__':
    analyze_missing()
