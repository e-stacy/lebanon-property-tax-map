#!/usr/bin/env python3
"""
Find example parcels with diverse sales data
"""

import pandas as pd

def find_parcel_examples():
    # Read the comprehensive sales data
    sales_df = pd.read_csv('data/processed/final_property_sales_dataset.csv')

    # Group by parcel_id and count sales by source
    parcel_sources = {}
    for _, row in sales_df.iterrows():
        parcel_id = row['parcel_id']
        source = row['data_source']

        if parcel_id not in parcel_sources:
            parcel_sources[parcel_id] = set()
        parcel_sources[parcel_id].add(source)

    # Find parcels with sales from all three sources
    all_three_sources = set(['nhdra_csv_2025', 'annual_combined_2019_2024', 'nhdra_csv_historical'])
    parcels_with_all_sources = [pid for pid, sources in parcel_sources.items() if sources == all_three_sources]

    print(f'Parcels with sales from ALL THREE quality ranges: {len(parcels_with_all_sources)}')
    print()

    if parcels_with_all_sources:
        # Show details for the first parcel
        parcel_id = parcels_with_all_sources[0]
        show_parcel_details(parcel_id, sales_df, parcel_sources)
    else:
        print('No parcels found with sales from all three quality ranges.')
        print()
        print('Let me check for parcels with the most diverse sales data...')

        # Find parcels with the most different sources
        parcel_source_counts = [(pid, len(sources)) for pid, sources in parcel_sources.items()]
        parcel_source_counts.sort(key=lambda x: x[1], reverse=True)

        for parcel_id, count in parcel_source_counts[:3]:
            show_parcel_details(parcel_id, sales_df, parcel_sources)
            print()

def show_parcel_details(parcel_id, sales_df, parcel_sources):
    parcel_sales = sales_df[sales_df['parcel_id'] == parcel_id].sort_values('sale_date', ascending=False)
    sources = parcel_sources[parcel_id]

    print(f'=== PARCEL {parcel_id} ===')
    print(f'Sources: {list(sources)} ({len(sources)} different sources)')
    print(f'Total sales: {len(parcel_sales)}')
    print()

    for _, sale in parcel_sales.iterrows():
        date = sale['sale_date']
        price = f"${sale['sale_price']:,.0f}" if pd.notna(sale['sale_price']) else 'N/A'
        source = sale['data_source']
        tier = sale['strategy_tier']
        print(f'  {date}: {price} ({source} - {tier})')
    print()

    # Show property details from parcels.csv
    try:
        parcels_df = pd.read_csv('data/processed/parcels.csv')
        property_info = parcels_df[parcels_df['parcel_id'] == parcel_id]
        if not property_info.empty:
            prop = property_info.iloc[0]
            print(f'Property Details:')
            print(f'  Address: {prop.get("situs_address", "Unknown")}')
            print(f'  Owner: {prop.get("owner_name", "Unknown")}')
            print(f'  Class: {prop.get("class_code", "Unknown")}')
            print(f'  Total Value: ${prop.get("total_value", 0):,.0f}')
            print(f'  Year Built: {prop.get("nhdra_vns ayb", "Unknown")}')
    except Exception as e:
        print(f'Could not load property details: {e}')

if __name__ == '__main__':
    find_parcel_examples()
