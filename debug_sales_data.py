#!/usr/bin/env python3
"""
Debug sales data and assessment issues
"""

import pandas as pd

def debug_issues():
    print("=== DEBUGGING SALES AND ASSESSMENT DATA ===\n")

    # Check sales data for parcel 50-40
    print("=== SALES DATA FOR PARCEL 50-40 ===")
    sales_df = pd.read_csv('data/processed/final_property_sales_dataset.csv')
    parcel_50_40_sales = sales_df[sales_df['parcel_id'] == '50-40']
    print(f"Sales records found: {len(parcel_50_40_sales)}")

    if len(parcel_50_40_sales) > 0:
        print("Sales data:")
        for idx, row in parcel_50_40_sales.iterrows():
            sale_date = row.get('sale_date', 'N/A')
            sale_price = row.get('sale_price', 'N/A')
            source = row.get('data_source', 'N/A')
            print(f"  Date: {sale_date}, Price: ${sale_price}, Source: {source}")
    else:
        print("No sales data found for parcel 50-40")

    # Check parcels data for 50-40
    print("\n=== PARCELS DATA FOR 50-40 ===")
    parcels_df = pd.read_csv('data/processed/parcels.csv')
    parcel_50_40 = parcels_df[parcels_df['parcel_id'] == '50-40']
    if len(parcel_50_40) > 0:
        row = parcel_50_40.iloc[0]
        parcel_id = row['parcel_id']
        current = row.get('total_value', 'N/A')
        previous = row.get('nhdra_ahd ttl assess', 'N/A')
        print(f"Parcel found: {parcel_id}")
        print(f"Current assessed: ${current}")
        print(f"Previous assessed: ${previous}")
    else:
        print("Parcel 50-40 not found in parcels data")

    # Check for 108 school
    print("\n=== SEARCHING FOR 108 SCHOOL ===")
    try:
        school_addresses = parcels_df[parcels_df['situs_address'].str.contains('SCHOOL', na=False, case=False)]
        if len(school_addresses) > 0:
            print(f"Found {len(school_addresses)} addresses containing 'SCHOOL'")
            school_108_addr = school_addresses[school_addresses['situs_address'].str.contains('108', na=False)]
            if len(school_108_addr) > 0:
                print("108 School addresses:")
                for idx, row in school_108_addr.iterrows():
                    parcel_id = row['parcel_id']
                    address = row['situs_address']
                    current = row.get('total_value', 'N/A')
                    previous = row.get('nhdra_ahd ttl assess', 'N/A')
                    print(f"  {parcel_id}: {address}")
                    print(f"    Current=${current}, Previous=${previous}")
            else:
                print("No 108 School addresses found")
        else:
            print("No school addresses found")
    except Exception as e:
        print(f"Error searching for schools: {e}")

    # Check how sales data is structured
    print("\n=== SALES DATA STRUCTURE ===")
    if len(parcel_50_40_sales) > 0:
        print("Sample sales record structure:")
        sample = parcel_50_40_sales.iloc[0]
        for col in sales_df.columns:
            if col in sample and pd.notna(sample[col]):
                print(f"  {col}: {sample[col]}")

if __name__ == '__main__':
    debug_issues()
