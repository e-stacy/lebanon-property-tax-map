#!/usr/bin/env python3
"""
Check the actual content of the sales CSV
"""

import pandas as pd

def check_csv_content():
    df_sales = pd.read_csv('data/processed/final_property_sales_dataset.csv')
    parcel_50_40_sales = df_sales[df_sales['parcel_id'] == '50-40']

    print('Raw CSV content for parcel 50-40:')
    for idx, row in parcel_50_40_sales.iterrows():
        print(f'Row {idx}:')
        for col in df_sales.columns:
            val = row[col]
            if pd.notna(val):
                print(f'  {col}: "{val}"')
            else:
                print(f'  {col}: <null>')
        print()

    # Check if sale_price column has values
    print('Sale price values in dataset:')
    price_samples = df_sales['sale_price'].dropna().head(5).tolist()
    print(f'Sample sale prices: {price_samples}')

if __name__ == '__main__':
    check_csv_content()
