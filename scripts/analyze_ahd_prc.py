#!/usr/bin/env python3
"""
Analyze AHD vs PRC assessment values
"""

import pandas as pd

def analyze_ahd_prc():
    print("=== COLUMN NAME ANALYSIS ===")
    df_nhdra = pd.read_csv('data/raw/city/nhdra.csv', nrows=5, header=1)

    print('Columns containing "ahd":')
    ahd_cols = [col for col in df_nhdra.columns if 'ahd' in col.lower()]
    for col in ahd_cols:
        print(f'  {col}')

    print('\nColumns containing "prc":')
    prc_cols = [col for col in df_nhdra.columns if 'prc' in col.lower()]
    for col in prc_cols:
        print(f'  {col}')

    # Check if there are any clues in the data about what AHD represents
    print('\n=== CHECKING FOR TEMPORAL PATTERNS ===')
    df_full = pd.read_csv('data/raw/city/nhdra.csv', header=1)

    # Look at parcels that have different AHD and PRC values
    different = df_full[df_full['ahd ttl assess'] != df_full['prc ttl assess']]
    if len(different) > 0:
        print(f'Parcels with different AHD/PRC values: {len(different)}')

        # Check if AHD is consistently lower than PRC (suggesting it's from an earlier assessment)
        ahd_lower = (different['ahd ttl assess'] < different['prc ttl assess']).sum()
        ahd_higher = (different['ahd ttl assess'] > different['prc ttl assess']).sum()

        print(f'  AHD < PRC: {ahd_lower} ({ahd_lower/len(different)*100:.1f}%)')
        print(f'  AHD > PRC: {ahd_higher} ({ahd_higher/len(different)*100:.1f}%)')

        print('\nSample differences:')
        samples = different.head(3)
        for idx, row in samples.iterrows():
            parcel = f"{row['rem mblu map']}-{row['rem mblu block']}-{row['rem mblu lot']}"
            ahd = row['ahd ttl assess']
            prc = row['prc ttl assess']
            diff = prc - ahd
            pct_change = (diff / ahd) * 100 if ahd > 0 else 0
            print(f'  {parcel}: AHD={ahd:,.0f}, PRC={prc:,.0f}, Change={diff:,.0f} ({pct_change:+.1f}%)')

if __name__ == '__main__':
    analyze_ahd_prc()
