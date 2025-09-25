#!/usr/bin/env python3
"""
Check the 108 school assessment data
"""

import pandas as pd

def check_108_school():
    # Check the 108 school assessment data
    df_parcels = pd.read_csv('data/processed/parcels.csv')

    # Find parcels with '108' in the address
    school_108 = df_parcels[df_parcels['situs_address'].str.contains('108', na=False, case=False)]
    if len(school_108) > 0:
        print('108 School parcel assessment data:')
        for idx, row in school_108.iterrows():
            parcel_id = row['parcel_id']
            address = row['situs_address']
            current = row.get('total_value', 'N/A')
            previous = row.get('nhdra_ahd ttl assess', 'N/A')
            print(f'{parcel_id}: {address}')
            print(f'  Current assessed: ${current}')
            print(f'  Previous assessed: ${previous}')

            if str(current) == str(previous) and current != 'N/A':
                print('  ⚠️  Previous = Current (this might be incorrect)')
            print()
    else:
        print('No parcels found with 108 in address')

    # Check the original NHDRA data for this parcel
    print('Checking original NHDRA data for 108 school:')
    df_nhdra = pd.read_csv('data/raw/city/nhdra.csv', header=1)

    # Find parcels with '108' in address
    nhdra_108 = df_nhdra[df_nhdra['rem prcl locn'].str.contains('108', na=False, case=False)]
    if len(nhdra_108) > 0:
        for idx, row in nhdra_108.iterrows():
            parcel_id = f"{row['rem mblu map']}-{row['rem mblu block']}-{row['rem mblu lot']}"
            address = row['rem prcl locn']
            current = row.get('prc ttl assess', 'N/A')
            previous = row.get('ahd ttl assess', 'N/A')
            print(f'{parcel_id}: {address}')
            print(f'  Current assessed: ${current}')
            print(f'  Previous assessed: ${previous}')
            print()
    else:
        print('No 108 school parcels found in original NHDRA data')

if __name__ == '__main__':
    check_108_school()
