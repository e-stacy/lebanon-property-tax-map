#!/usr/bin/env python3
"""
Populate missing Previous Assessed values using AHD assessment data from original NHDRA
"""

import pandas as pd
import os

def populate_previous_assessed():
    print("=== POPULATING MISSING PREVIOUS ASSESSED VALUES ===\n")

    # Load the enriched sales file
    sales_file = 'data/processed/sales-data-09-25-25.xlsx'
    print(f"Loading sales data: {sales_file}")
    df_sales = pd.read_excel(sales_file)
    print(f"Sales data shape: {df_sales.shape}")

    # Load original NHDRA data
    nhdra_file = 'data/raw/city/nhdra.csv'
    print(f"\nLoading NHDRA data: {nhdra_file}")
    df_nhdra = pd.read_csv(nhdra_file, header=1)
    print(f"NHDRA data shape: {df_nhdra.shape}")

    # Create parcel ID mapping for NHDRA data
    def create_parcel_id(row):
        map_num = str(row.get('rem mblu map', '')).strip()
        block = str(row.get('rem mblu block', '')).strip()
        lot = str(row.get('rem mblu lot', '')).strip()
        unit = str(row.get('rem mblu unit', '')).strip()
        parts = [p for p in [map_num, block, lot, unit] if p and p != 'nan' and p != '']
        return '-'.join(parts) if parts else ''

    df_nhdra['parcel_id'] = df_nhdra.apply(create_parcel_id, axis=1)
    print(f"NHDRA parcels with IDs: {len(df_nhdra[df_nhdra['parcel_id'] != ''])}")

    # Create lookup dictionary for AHD assessment values
    ahd_lookup = {}
    for _, row in df_nhdra.iterrows():
        parcel_id = row['parcel_id']
        ahd_value = row.get('ahd ttl assess')
        if parcel_id and pd.notna(ahd_value) and ahd_value > 0:
            ahd_lookup[parcel_id] = ahd_value

    print(f"Created AHD lookup for {len(ahd_lookup)} parcels with assessment values")

    # Identify records that need Previous Assessed values populated
    missing_prev_mask = df_sales['Previous\nAssed'].isna()
    historical_source_mask = df_sales['SourceFile'] == 'nhdra-historical.xlsx'
    needs_update_mask = missing_prev_mask & historical_source_mask

    records_to_update = df_sales[needs_update_mask]
    print(f"\nRecords to update: {len(records_to_update)}")

    # Update the Previous Assessed values
    updated_count = 0
    for idx in records_to_update.index:
        map_lot = str(df_sales.at[idx, 'Map\nLot']).strip()
        if map_lot in ahd_lookup:
            ahd_value = ahd_lookup[map_lot]
            df_sales.at[idx, 'Previous\nAssed'] = ahd_value
            updated_count += 1

    print(f"Successfully updated {updated_count} records with Previous Assessed values")

    # Verify the updates
    print("\n=== VERIFICATION ===")
    final_missing = df_sales['Previous\nAssed'].isna().sum()
    final_filled = len(df_sales) - final_missing
    fill_rate = final_filled / len(df_sales) * 100

    print(f"Total records: {len(df_sales)}")
    print(f"Previous Assessed filled: {final_filled} ({fill_rate:.1f}%)")
    print(f"Previous Assessed missing: {final_missing} ({100-fill_rate:.1f}%)")

    # Check by source
    print(f"\nBy source after update:")
    source_stats = df_sales.groupby('SourceFile')['Previous\nAssed'].agg(
        filled=lambda x: x.notna().sum(),
        total='count'
    )
    for source, stats in source_stats.iterrows():
        pct = stats['filled'] / stats['total'] * 100
        print(f"  {source}: {stats['filled']}/{stats['total']} ({pct:.1f}%)")

    # Save the updated file
    output_file = 'data/processed/sales-data-09-25-25.xlsx'  # Overwrite the existing file
    print(f"\nSaving updated file: {output_file}")

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_sales.to_excel(writer, sheet_name='Sales', index=False)

        # Ensure Map Lot column stays as text
        workbook = writer.book
        worksheet = writer.sheets['Sales']

        map_lot_col = None
        for col_num, col_name in enumerate(df_sales.columns, 1):
            if col_name == 'Map\nLot':
                map_lot_col = col_num
                break

        if map_lot_col:
            for row_num in range(2, len(df_sales) + 2):
                cell = worksheet.cell(row=row_num, column=map_lot_col)
                cell.number_format = '@'

    print("✅ Successfully populated Previous Assessed values!")

    # Show sample of updated records
    print("\nSample of updated records:")
    updated_records = df_sales[needs_update_mask & df_sales['Previous\nAssed'].notna()].head(3)
    for idx, row in updated_records.iterrows():
        map_lot = row['Map\nLot']
        prev_assessed = row['Previous\nAssed']
        current_assessed = row['Current\nAssed']
        print(f"  {map_lot}: Previous=${prev_assessed:,.0f}, Current=${current_assessed:,.0f}")

    return updated_count

if __name__ == '__main__':
    populate_previous_assessed()
