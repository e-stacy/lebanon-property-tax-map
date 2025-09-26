#!/usr/bin/env python3
"""
Create normalized Excel files from NHDRA and sales data
One row per sale for easier comparison
"""

import pandas as pd
import os

def create_nhdra_normalized():
    print("=== CREATING NORMALIZED NHDRA SALES FILES ===\n")

    # Create output directory if it doesn't exist
    os.makedirs('data/processed', exist_ok=True)

    # 1. Process original NHDRA file
    print("Processing original NHDRA CSV...")
    nhdra_df = pd.read_csv('data/raw/city/nhdra.csv', header=1)
    print(f"Loaded {len(nhdra_df)} parcels from NHDRA")

    # Create normalized rows for NHDRA
    nhdra_sales = []

    for _, row in nhdra_df.iterrows():
        # Extract parcel ID components
        map_num = str(row.get('rem mblu map', '')).strip()
        block = str(row.get('rem mblu block', '')).strip()
        lot = str(row.get('rem mblu lot', '')).strip()

        parcel_id_parts = [p for p in [map_num, block, lot] if p and p != 'nan' and p != '']
        parcel_id = '-'.join(parcel_id_parts) if parcel_id_parts else 'unknown'

        # Skip if we can't create a meaningful parcel ID
        if parcel_id == 'unknown' or len(parcel_id_parts) < 2:
            continue

        # Current sale
        if row.get('saleprice') and float(row['saleprice']) > 0:
            nhdra_sales.append({
                'parcel_id': parcel_id,
                'sale_date': str(row.get('saledate', '')).split(' ')[0] if pd.notna(row.get('saledate')) else '',
                'sale_price': float(row['saleprice']),
                'qualified': row.get('qualified', ''),
                'book_page': row.get('book pg', ''),
                'sale_type': 'current',
                'source': 'original_nhdra'
            })

        # Prior sales
        for i in range(1, 4):
            price_field = f'ID{i} Prior Sale Price'
            date_field = f'ID{i} Prior Sale Date'
            book_field = f'ID{i} Prior Book Page'

            price = row.get(price_field)
            if price and str(price).strip() and str(price) != '0':
                try:
                    price_val = float(price)
                    nhdra_sales.append({
                        'parcel_id': parcel_id,
                        'sale_date': str(row.get(date_field, '')).split(' ')[0] if pd.notna(row.get(date_field)) else '',
                        'sale_price': price_val,
                        'qualified': 'Q',  # Prior sales typically qualified
                        'book_page': row.get(book_field, ''),
                        'sale_type': f'prior_{i}',
                        'source': 'original_nhdra'
                    })
                except (ValueError, TypeError):
                    continue

    # Create DataFrame and sort
    nhdra_sales_df = pd.DataFrame(nhdra_sales)
    nhdra_sales_df = nhdra_sales_df.sort_values(['parcel_id', 'sale_date'])

    # Save as Excel with proper formatting
    nhdra_excel_file = 'data/processed/nhdra.xlsx'

    with pd.ExcelWriter(nhdra_excel_file, engine='openpyxl') as writer:
        nhdra_sales_df.to_excel(writer, sheet_name='Sales', index=False)

        # Get workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Sales']

        # Format parcel_id column as text to prevent date formatting
        from openpyxl.styles import NamedStyle
        text_style = NamedStyle(name='text_style', number_format='@')
        workbook.add_named_style(text_style)

        # Apply text formatting to parcel_id column
        parcel_col = None
        for col_num, col_name in enumerate(nhdra_sales_df.columns, 1):
            if col_name == 'parcel_id':
                parcel_col = col_num
                break

        if parcel_col:
            for row_num in range(2, len(nhdra_sales_df) + 2):  # Start from row 2 (after header)
                cell = worksheet.cell(row=row_num, column=parcel_col)
                cell.number_format = '@'  # Text format

    print(f"✅ Created nhdra.xlsx: {len(nhdra_sales_df)} sales records from {nhdra_sales_df['parcel_id'].nunique()} parcels")

    # 2. Process combined sales file
    print("\nProcessing 2019-2024 combined sales...")
    sales_df = pd.read_csv('data/processed/sales.csv')
    print(f"Loaded {len(sales_df)} sales from comprehensive dataset")

    # Filter to 2019-2024 and format
    sales_2019_2024 = []
    for _, row in sales_df.iterrows():
        sale_date = pd.to_datetime(row['sale_date'], errors='coerce')
        if pd.notna(sale_date) and sale_date.year >= 2019:
            sales_2019_2024.append({
                'parcel_id': row['parcel_id'],
                'sale_date': str(row['sale_date']).split(' ')[0] if pd.notna(row['sale_date']) else '',
                'sale_price': row['sale_price'] if pd.notna(row['sale_price']) else 0,
                'qualified': row.get('qualified', ''),
                'book_page': row.get('book_page', ''),
                'sale_type': 'verified_sale',
                'source': row.get('data_source', 'comprehensive')
            })

    # Create DataFrame and sort
    sales_2019_2024_df = pd.DataFrame(sales_2019_2024)
    sales_2019_2024_df = sales_2019_2024_df.sort_values(['parcel_id', 'sale_date'])

    # Save as Excel
    sales_excel_file = 'data/processed/nhdra-sales.xlsx'

    with pd.ExcelWriter(sales_excel_file, engine='openpyxl') as writer:
        sales_2019_2024_df.to_excel(writer, sheet_name='Sales', index=False)

        # Format parcel_id column as text
        workbook = writer.book
        worksheet = writer.sheets['Sales']

        parcel_col = None
        for col_num, col_name in enumerate(sales_2019_2024_df.columns, 1):
            if col_name == 'parcel_id':
                parcel_col = col_num
                break

        if parcel_col:
            for row_num in range(2, len(sales_2019_2024_df) + 2):
                cell = worksheet.cell(row=row_num, column=parcel_col)
                cell.number_format = '@'

    print(f"✅ Created nhdra-sales.xlsx: {len(sales_2019_2024_df)} sales records from {sales_2019_2024_df['parcel_id'].nunique()} parcels")

    # Summary
    print("\n=== NORMALIZATION SUMMARY ===")
    print(f"Original NHDRA: {len(nhdra_sales_df)} sales from {nhdra_sales_df['parcel_id'].nunique()} parcels")
    print(f"Combined Sales: {len(sales_2019_2024_df)} sales from {sales_2019_2024_df['parcel_id'].nunique()} parcels")

    # Find overlap
    nhdra_parcels = set(nhdra_sales_df['parcel_id'].unique())
    sales_parcels = set(sales_2019_2024_df['parcel_id'].unique())
    overlap = nhdra_parcels & sales_parcels

    print(f"Parcels in both datasets: {len(overlap)}")

    return nhdra_excel_file, sales_excel_file

if __name__ == '__main__':
    create_nhdra_normalized()
