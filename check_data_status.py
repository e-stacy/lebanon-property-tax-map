#!/usr/bin/env python3
"""
Check the current status of all data files
"""

import pandas as pd
import os

def check_data_status():
    print("=== CURRENT DATA STATUS EVALUATION ===\n")

    # Check raw data
    print("RAW DATA:")
    raw_files = {
        'city/nhdra.csv': 'Original NHDRA parcels',
        'city/parcels.csv': 'City parcels export',
        'city/buildings.csv': 'City buildings',
        'city/land.csv': 'City land',
        'nhdra/SalesList_2020-2024_combined.xlsx': 'Combined NHDRA sales'
    }

    for file_path, description in raw_files.items():
        full_path = f'data/raw/{file_path}'
        if os.path.exists(full_path):
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(full_path, nrows=5)
                else:
                    df = pd.read_excel(full_path, nrows=5)
                print(f"  ✅ {file_path}: {len(df)} rows - {description}")
            except Exception as e:
                print(f"  ❌ {file_path}: Error - {e}")
        else:
            print(f"  ❌ {file_path}: Missing")

    print("\nPROCESSED DATA:")
    processed_files = [
        'parcels.csv',
        'final_property_sales_dataset.csv',
        'sales-data-09-25-25.xlsx'
    ]

    for filename in processed_files:
        file_path = f'data/processed/{filename}'
        if os.path.exists(file_path):
            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                print(f"  ✅ {filename}: {len(df)} rows, {len(df.columns)} columns")
            except Exception as e:
                print(f"  ❌ {filename}: Error - {e}")
        else:
            print(f"  ❌ {filename}: Missing")

    # Check for data quality issues
    print("\nDATA QUALITY CHECK:")

    # Check parcels
    try:
        df_parcels = pd.read_csv('data/processed/parcels.csv')
        unique_parcels = df_parcels['parcel_id'].nunique()
        total_parcels = len(df_parcels)
        duplicates = total_parcels - unique_parcels
        print(f"  Parcels: {unique_parcels} unique, {duplicates} duplicates")
    except:
        print("  Parcels: Unable to check")

    # Check sales
    try:
        df_sales = pd.read_csv('data/processed/final_property_sales_dataset.csv')
        unique_sales_parcels = df_sales['parcel_id'].nunique()
        total_sales = len(df_sales)
        print(f"  Sales: {total_sales} records for {unique_sales_parcels} parcels")
    except:
        print("  Sales: Unable to check")

if __name__ == '__main__':
    check_data_status()
