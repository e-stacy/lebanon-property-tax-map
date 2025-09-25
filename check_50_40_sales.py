#!/usr/bin/env python3
"""
Check if parcel 50-40 sales are now in the comprehensive file
"""

import pandas as pd

def check_50_40_sales():
    print('=== CHECKING UPDATED NHDRA COMPREHENSIVE SALES FOR 50-40 ===')
    df_nhdra_comp = pd.read_excel('data/processed/nhdra_csv_comprehensive_sales.xlsx')
    nhdra_50_40 = df_nhdra_comp[df_nhdra_comp['parcel_id'] == '50-40']
    print(f'Parcel 50-40 in updated comprehensive NHDRA: {len(nhdra_50_40)} records')

    if len(nhdra_50_40) > 0:
        print('Updated comprehensive NHDRA data for 50-40:')
        for idx, row in nhdra_50_40.iterrows():
            sale_date = str(row.get('sale_date', 'N/A')).split(' ')[0]
            sale_price = row.get('sale_price', 'N/A')
            sale_type = row.get('sale_type', 'N/A')
            book_page = row.get('book_page', 'N/A')
            print(f'  Date: {sale_date}, Price: ${sale_price}, Type: {sale_type}, Book: {book_page}')
    else:
        # Check what parcel IDs exist that contain '50'
        potential_matches = df_nhdra_comp[df_nhdra_comp['parcel_id'].str.contains('50', na=False)]
        print(f'Potential matches containing "50": {len(potential_matches)}')
        if len(potential_matches) > 0:
            sample_ids = potential_matches['parcel_id'].head(5).tolist()
            print(f'Sample IDs: {sample_ids}')

if __name__ == '__main__':
    check_50_40_sales()
