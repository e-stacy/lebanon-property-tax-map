#!/usr/bin/env python3
"""
Check for duplicate sales in parcel data
"""

import pandas as pd

def check_duplicates():
    # Check what sales are in our comprehensive data for parcel 4-23-706
    sales_df = pd.read_csv('data/processed/final_property_sales_dataset.csv')
    parcel_sales = sales_df[sales_df['parcel_id'] == '4-23-706'].sort_values('sale_date')
    print('All sales for parcel 4-23-706:')
    for _, sale in parcel_sales.iterrows():
        print(f'  {sale["sale_date"]} - ${sale["sale_price"]} - {sale.get("book_page", "N/A")} - {sale["data_source"]}')

    print()
    print('Checking for potential duplicates:')
    found_duplicates = False
    for i, sale1 in parcel_sales.iterrows():
        for j, sale2 in parcel_sales.iterrows():
            if i < j:
                date1 = pd.to_datetime(sale1['sale_date'])
                date2 = pd.to_datetime(sale2['sale_date'])
                price1 = float(sale1['sale_price'])
                price2 = float(sale2['sale_price'])
                date_diff = abs((date1 - date2).days)

                if date_diff <= 30 and abs(price1 - price2) < 1:
                    print(f'DUPLICATE FOUND: {sale1["sale_date"]} ${sale1["sale_price"]} vs {sale2["sale_date"]} ${sale2["sale_price"]} ({date_diff} days apart)')
                    found_duplicates = True

    if not found_duplicates:
        print('No duplicates found within 30 days and $1 price difference.')

    # Check original NHDRA data
    print()
    print('Original NHDRA data:')
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

if __name__ == '__main__':
    check_duplicates()
