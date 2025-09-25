#!/usr/bin/env python3
"""
Check parcel 50-40 data structure
"""

import pandas as pd

def check_parcel_50_40():
    # Check the original NHDRA data for parcel 50-40
    df_orig = pd.read_csv('data/raw/city/nhdra.csv', header=1)

    # Find parcel 50-40
    mask = (df_orig['rem mblu map'] == 50) & (df_orig['rem mblu block'] == 40)
    parcel_50_40 = df_orig[mask]

    if len(parcel_50_40) > 0:
        row = parcel_50_40.iloc[0]
        print('Found parcel 50-40 in original data:')
        print(f'  Map: {row["rem mblu map"]}')
        print(f'  Block: {row["rem mblu block"]}')
        print(f'  Lot: "{row["rem mblu lot"]}"')
        print(f'  Unit: "{row["rem mblu unit"]}"')

        # Create parcel ID the same way as the extraction script
        parcel_id = f"{row['rem mblu map']}-{row['rem mblu block']}-{row['rem mblu lot']}"
        print(f'  Generated parcel ID: "{parcel_id}"')

        # Check if lot is empty/NaN
        lot_val = row['rem mblu lot']
        print(f'  Lot value type: {type(lot_val)}, value: {repr(lot_val)}')

    else:
        print('Parcel 50-40 not found with map=50, block=40')

    # Also check the parcels CSV to see how it's stored there
    print('\n=== CHECKING PARCELS CSV ===')
    df_parcels = pd.read_csv('data/processed/parcels.csv')
    parcels_50_40 = df_parcels[df_parcels['parcel_id'] == '50-40']
    if len(parcels_50_40) > 0:
        print('Found parcel 50-40 in parcels CSV')
    else:
        print('Parcel 50-40 not found in parcels CSV')
        # Check what parcel IDs look like
        sample_ids = df_parcels['parcel_id'].head(10).tolist()
        print(f'Sample parcel IDs: {sample_ids}')

if __name__ == '__main__':
    check_parcel_50_40()
