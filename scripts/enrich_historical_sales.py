#!/usr/bin/env python3
"""
Enrich historical sales rows in sales-data-09-25-25.xlsx with parcel-level data from original nhdra.csv
"""

import pandas as pd
import os

def enrich_historical_sales():
    print("=== ENRICHING HISTORICAL SALES DATA ===")

    # Load the merged file
    merged_file = 'data/processed/sales-data-09-25-25.xlsx'
    print(f"Loading merged file: {merged_file}")
    df_merged = pd.read_excel(merged_file)
    print(f"Merged file shape: {df_merged.shape}")

    # Load original NHDRA data
    nhdra_file = 'data/raw/city/nhdra.csv'
    print(f"\nLoading original NHDRA: {nhdra_file}")
    df_nhdra = pd.read_csv(nhdra_file, header=1)
    print(f"NHDRA shape: {df_nhdra.shape}")

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

    # Create lookup dictionary for fast parcel data access
    parcel_lookup = {}
    for _, row in df_nhdra.iterrows():
        parcel_id = row['parcel_id']
        if parcel_id:
            parcel_lookup[parcel_id] = {
                'address': f"{row.get('rem prcl locn street', '')} {row.get('rem prcl locn', '')}".strip(),
                'acres': row.get('prc ttl lnd area acres'),
                'prop_code': row.get('rem use code'),
                'current_assed': row.get('prc ttl assess'),
                'owner_name': row.get('own name', ''),
                'land_zone': row.get('lnd zone', ''),
                'total_assess_bldg': row.get('prc ttl assess bldg'),
                'total_assess_land': row.get('prc ttl assess lnd'),
                'living_area': row.get('cns area living'),
                'year_built': row.get('vns ayb'),
                'grade': row.get('vns grade'),
                'stories': row.get('vns stories'),
                'heat_type': row.get('vns heat type desc'),
                'heat_fuel': row.get('vns heat fuel desc'),
                'nbhd': row.get('lnd nbhd')
            }

    print(f"Created lookup for {len(parcel_lookup)} parcels")

    # Field mapping from NHDRA to merged file (parcel-level only)
    field_mapping = {
        'Address': 'address',
        'Acres': 'prc ttl lnd area acres',
        'Prop\nCode': 'rem use code',
        'Current\nAssed': 'prc ttl assess',
        'Grantor': 'own name',  # Owner name could be used for grantor if no sale-specific data
        'Town\nNotes': 'lnd zone',  # Zoning code
        'Year Built': 'vns ayb',  # Year built for filtering
        'Heat Type': 'vns heat type desc'  # Heating type for filtering
    }

    print("\nField mapping for enrichment:")
    for merged_col, nhdra_key in field_mapping.items():
        print(f"  {merged_col} ← {nhdra_key}")

    # Identify historical rows that need enrichment
    historical_mask = df_merged['SourceFile'] == 'nhdra-historical.xlsx'
    historical_rows = df_merged[historical_mask]
    print(f"\nHistorical rows to enrich: {len(historical_rows)}")

    # Update historical rows with parcel data
    updated_count = 0
    for idx in historical_rows.index:
        map_lot = str(df_merged.at[idx, 'Map\nLot']).strip()
        if map_lot in parcel_lookup:
            parcel_data = parcel_lookup[map_lot]

            # Update parcel-level fields
            for merged_col, nhdra_key in field_mapping.items():
                if nhdra_key in parcel_data and pd.isna(df_merged.at[idx, merged_col]):
                    value = parcel_data[nhdra_key]
                    if pd.notna(value) and value != '':
                        df_merged.at[idx, merged_col] = value
                        updated_count += 1

    print(f"Total field updates made: {updated_count}")

    # Save updated file
    output_file = 'data/processed/sales-data-09-25-25.xlsx'
    print(f"\nSaving enriched file: {output_file}")

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_merged.to_excel(writer, sheet_name='Sales', index=False)

        # Ensure Map Lot column stays as text
        workbook = writer.book
        worksheet = writer.sheets['Sales']

        map_lot_col = None
        for col_num, col_name in enumerate(df_merged.columns, 1):
            if col_name == 'Map\nLot':
                map_lot_col = col_num
                break

        if map_lot_col:
            for row_num in range(2, len(df_merged) + 2):
                cell = worksheet.cell(row=row_num, column=map_lot_col)
                cell.number_format = '@'

    print("✅ Successfully enriched historical sales data!")

    # Summary statistics
    print("\n=== ENRICHMENT SUMMARY ===")
    print(f"Total rows: {len(df_merged)}")
    print(f"Historical rows: {len(historical_rows)}")
    print(f"Fields updated: {updated_count}")

    # Sample enriched row
    sample_historical = df_merged[historical_mask].head(1)
    if not sample_historical.empty:
        print(f"\nSample enriched historical row:")
        row = sample_historical.iloc[0]
        enriched_fields = [col for col in field_mapping.keys() if pd.notna(row[col])]
        print(f"  Enriched fields: {enriched_fields}")
        for field in enriched_fields[:3]:  # Show first 3
            print(f"  {field}: {row[field]}")

    return output_file

if __name__ == '__main__':
    enrich_historical_sales()
