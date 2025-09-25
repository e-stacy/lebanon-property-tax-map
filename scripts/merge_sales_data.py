#!/usr/bin/env python3
"""
Merge SalesList_2020-2024_combined.xlsx (template) with nhdra-historical.xlsx
"""

import pandas as pd
import os

def merge_sales_data():
    print("=== MERGING SALES DATA ===")

    # Load the template file (main structure)
    template_file = 'data/processed/SalesList_2020-2024_combined.xlsx'
    print(f"Loading template: {template_file}")
    df_template = pd.read_excel(template_file)
    print(f"Template shape: {df_template.shape}")
    print(f"Template columns: {list(df_template.columns)}")

    # Load the historical data
    historical_file = 'data/processed/nhdra-historical.xlsx'
    print(f"\nLoading historical: {historical_file}")
    df_historical = pd.read_excel(historical_file)
    print(f"Historical shape: {df_historical.shape}")
    print(f"Historical columns: {list(df_historical.columns)}")

    # Create a mapping from historical columns to template columns
    column_mapping = {
        'parcel_id': 'Map\nLot',  # Map parcel_id to Map Lot field
        'sale_date': 'Sale\nDate',
        'sale_price': 'Verified\nPrice',
        'qualified': None,  # No direct equivalent, will be blank
        'book_page': 'Book\nPage'
    }

    print("\nColumn mapping:")
    for hist_col, template_col in column_mapping.items():
        print(f"  {hist_col} → {template_col}")

    # Create new dataframe with template structure for historical data
    historical_mapped = []

    for _, row in df_historical.iterrows():
        new_row = {}

        # Copy all template columns, defaulting to empty
        for col in df_template.columns:
            new_row[col] = None  # Default to blank

        # Map historical data to appropriate template columns
        for hist_col, template_col in column_mapping.items():
            if template_col and hist_col in df_historical.columns:
                value = row[hist_col]
                # Handle parcel_id formatting - ensure it's text
                if hist_col == 'parcel_id':
                    value = str(value)
                new_row[template_col] = value

        # Add source indicator
        new_row['SourceFile'] = 'nhdra-historical.xlsx'

        historical_mapped.append(new_row)

    # Convert to dataframe
    df_historical_mapped = pd.DataFrame(historical_mapped)

    print(f"\nMapped historical data shape: {df_historical_mapped.shape}")

    # Combine the dataframes
    print("\nCombining datasets...")
    df_combined = pd.concat([df_template, df_historical_mapped], ignore_index=True)

    print(f"Combined shape: {df_combined.shape}")

    # Sort by Sale Date (most recent first)
    if 'Sale\nDate' in df_combined.columns:
        df_combined = df_combined.sort_values('Sale\nDate', ascending=False, na_position='last')

    # Save the merged file
    output_file = 'data/processed/sales-data-09-25-25.xlsx'
    print(f"\nSaving to: {output_file}")

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_combined.to_excel(writer, sheet_name='Sales', index=False)

        # Format Map Lot column as text to prevent date formatting
        workbook = writer.book
        worksheet = writer.sheets['Sales']

        map_lot_col = None
        for col_num, col_name in enumerate(df_combined.columns, 1):
            if col_name == 'Map\nLot':
                map_lot_col = col_num
                break

        if map_lot_col:
            for row_num in range(2, len(df_combined) + 2):
                cell = worksheet.cell(row=row_num, column=map_lot_col)
                cell.number_format = '@'  # Text format

    print("✅ Successfully created merged file!")
    print(f"   Template rows: {len(df_template)}")
    print(f"   Historical rows: {len(df_historical_mapped)}")
    print(f"   Total rows: {len(df_combined)}")

    return output_file

if __name__ == '__main__':
    merge_sales_data()
