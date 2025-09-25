#!/usr/bin/env python3
"""
Create a comparison file that formats NHDRA CSV sales data similar to annual NHDRA files
This simulates what the annual sales files would look like if based on the 4 sales slots from the flat file
"""

import pandas as pd
import csv

def create_nhdra_csv_sales_comparison():
    """Create a file that formats NHDRA CSV sales data like the annual files"""

    print('=== CREATING NHDRA CSV SALES COMPARISON FILE ===\n')

    # Read the comprehensive NHDRA CSV sales data we already extracted
    try:
        nhdra_sales = pd.read_excel('data/processed/nhdra_csv_comprehensive_sales.xlsx')
        print(f'Loaded {len(nhdra_sales)} sales from NHDRA CSV comprehensive file')
    except FileNotFoundError:
        print('NHDRA CSV comprehensive file not found. Running extraction first...')
        # Import and run the extraction
        from nhdra_csv_sales_extraction import extract_nhdra_csv_sales
        nhdra_sales = extract_nhdra_csv_sales()
        if nhdra_sales is None:
            return

    # Filter to match the annual files' date range (2020-2024)
    nhdra_sales['sale_year'] = nhdra_sales['sale_date'].dt.year
    filtered_sales = nhdra_sales[
        (nhdra_sales['sale_year'] >= 2020) &
        (nhdra_sales['sale_year'] <= 2024)
    ].copy()

    print(f'Filtered to {len(filtered_sales)} sales from 2020-2024 (matching annual files)')

    # Format to match annual NHDRA file structure
    # The annual files have columns like: Verno, Sale\nDate, Book\nPage, Grantor, Grantee, etc.
    # We'll create a simplified version with the key fields we have

    comparison_records = []

    for _, sale in filtered_sales.iterrows():
        record = {
            'Verno': '',  # Not available in NHDRA CSV
            'Sale\nDate': sale['sale_date'].strftime('%m/%d/%Y') if pd.notna(sale['sale_date']) else '',
            'Book\nPage': '',  # Not directly available
            'Grantor': '',  # Not available in sales data
            'Grantee': '',  # Not available in sales data
            'Deed\nType': '',  # Not available
            'Cama\nCount': '',  # Not available
            'Acres': '',  # Not available
            'Address': '',  # Not available
            'Map\nLot': sale['parcel_id'],
            'Verified\nPrice': f"${sale['sale_price']:,.0f}" if pd.notna(sale['sale_price']) else '',
            'Current\nAssed': '',  # Not available
            'Previous\nAssed': '',  # Not available
            'Ratio': '',  # Not available
            'Prop\nCode': '',  # Not available
            'Mod\nCode': '',  # Not available
            'Special\nCode': '',  # Not available
            'XCode1': '',  # Not available
            'XNotes1': '',  # Not available
            'XCode2': '',  # Not available
            'XNotes2': '',  # Not available
            'Main\nXCode': '',  # Not available
            'MainX\nNotes': '',  # Not available
            'Town\nNotes': '',  # Not available
            'State\nNotes': '',  # Not available
            'Source_Year': sale['sale_year'],
            'Source_File': 'NHDRA_CSV_Flat_File',
            'NHDRA_Sale_Type': sale['sale_type'],  # Current, prior_1, prior_2, prior_3
            'Qualified': sale.get('qualified', ''),
            'Book_Page': sale.get('book_page', '')
        }
        comparison_records.append(record)

    # Create DataFrame and save
    comparison_df = pd.DataFrame(comparison_records)

    # Sort to match annual file format (though we don't have all sorting fields)
    comparison_df = comparison_df.sort_values(['Map\nLot', 'Sale\nDate'])

    output_file = 'data/processed/nhdra_csv_sales_formatted_like_annual.xlsx'
    comparison_df.to_excel(output_file, index=False)

    print(f'✅ Created comparison file: {output_file}')
    print(f'   Records: {len(comparison_df)}')
    print(f'   Columns: {len(comparison_df.columns)}')
    print(f'   Unique parcels: {comparison_df["Map\nLot"].nunique()}')

    # Show sample
    print(f'\nSample records:')
    sample = comparison_df.head(3)
    for _, row in sample.iterrows():
        print(f'  {row["Map\nLot"]}: {row["Sale\nDate"]} - {row["Verified\nPrice"]} ({row["NHDRA_Sale_Type"]})')

    # Compare with actual annual file
    try:
        annual_file = pd.read_excel('data/processed/comprehensive_sales_2020-2024.xlsx')
        print(f'\nComparison with actual annual file:')
        print(f'  Annual file: {len(annual_file)} records')
        print(f'  NHDRA CSV formatted: {len(comparison_df)} records')
        print(f'  Difference: {len(comparison_df) - len(annual_file)} records')

        # Compare unique parcels
        annual_parcels = set(annual_file['Map\nLot'].dropna())
        csv_parcels = set(comparison_df['Map\nLot'].dropna())
        common_parcels = len(annual_parcels & csv_parcels)

        print(f'  Annual file unique parcels: {len(annual_parcels)}')
        print(f'  NHDRA CSV unique parcels: {len(csv_parcels)}')
        print(f'  Common parcels: {common_parcels}')

    except Exception as e:
        print(f'Could not compare with annual file: {e}')

    return comparison_df

if __name__ == '__main__':
    create_nhdra_csv_sales_comparison()
