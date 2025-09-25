#!/usr/bin/env python3
"""
Check the normalized Excel files
"""

import pandas as pd

def check_files():
    print("=== SAMPLE FROM nhdra.xlsx ===")
    df1 = pd.read_excel('data/processed/nhdra.xlsx')
    print(df1.head(10))

    print("\n=== SAMPLE FROM nhdra-sales.xlsx ===")
    df2 = pd.read_excel('data/processed/nhdra-sales.xlsx')
    print(df2.head(10))

    print("\n=== COMPARISON STATS ===")
    print(f"NHDRA total sales: {len(df1)}")
    print(f"Sales 2019-2024: {len(df2)}")
    print(f"Price range NHDRA: ${df1['sale_price'].min():,.0f} - ${df1['sale_price'].max():,.0f}")
    print(f"Price range Sales: ${df2['sale_price'].min():,.0f} - ${df2['sale_price'].max():,.0f}")
    print(f"Date range NHDRA: {df1['sale_date'].min()} - {df1['sale_date'].max()}")
    print(f"Date range Sales: {df2['sale_date'].min()} - {df2['sale_date'].max()}")

if __name__ == '__main__':
    check_files()
