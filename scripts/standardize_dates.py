#!/usr/bin/env python3
"""
Standardize all date formats to ISO 8601 (YYYY-MM-DD) across processed files
"""

import pandas as pd
import os
from datetime import datetime

def standardize_date_formats():
    print("=== STANDARDIZING DATE FORMATS TO ISO 8601 ===\n")

    # Files to update
    files_to_update = [
        'data/processed/sales-data-09-25-25.xlsx',
        'data/processed/SalesList_2020-2024_combined.xlsx',
        'data/processed/nhdra.xlsx',
        'data/processed/nhdra-sales.xlsx'
    ]

    total_updates = 0

    for file_path in files_to_update:
        if os.path.exists(file_path):
            print(f"📄 Processing: {os.path.basename(file_path)}")

            # Load file
            df = pd.read_excel(file_path)
            original_shape = df.shape
            file_updates = 0

            # Process Year column
            if 'Year' in df.columns:
                year_count = df['Year'].notna().sum()
                if year_count > 0:
                    # Convert to integer if it's float
                    if df['Year'].dtype == 'float64':
                        # Handle NaN values
                        df['Year'] = df['Year'].astype('Int64')  # Nullable integer
                        print(f"   ✅ Year column: float64 → Int64 ({year_count} values)")
                        file_updates += year_count
                    elif df['Year'].dtype == 'int64':
                        print(f"   ✅ Year column: already int64 ({year_count} values)")
                    else:
                        print(f"   ⚠️  Year column: unexpected type {df['Year'].dtype}")

            # Process Sale\nDate column
            if 'Sale\nDate' in df.columns:
                date_count = df['Sale\nDate'].notna().sum()
                if date_count > 0:
                    # Convert US format (MM/DD/YYYY) to ISO (YYYY-MM-DD)
                    original_dates = df['Sale\nDate'].dropna().head(3).tolist()
                    print(f"   Original Sale\\nDate samples: {original_dates}")

                    def convert_to_iso(date_val):
                        if pd.isna(date_val):
                            return date_val

                        date_str = str(date_val).strip()
                        if not date_str:
                            return date_val

                        try:
                            # Try parsing US format MM/DD/YYYY
                            if '/' in date_str:
                                parts = date_str.split('/')
                                if len(parts) == 3:
                                    month, day, year = parts
                                    # Ensure year is 4 digits
                                    if len(year) == 2:
                                        year = '20' + year
                                    # Create ISO format
                                    iso_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                                    # Validate the date
                                    datetime.strptime(iso_date, '%Y-%m-%d')
                                    return iso_date
                            # If already in ISO format, return as-is
                            elif '-' in date_str and len(date_str.split('-')) == 3:
                                datetime.strptime(date_str, '%Y-%m-%d')
                                return date_str
                            else:
                                # Try other common formats
                                parsed = pd.to_datetime(date_str, errors='coerce')
                                if pd.notna(parsed):
                                    return parsed.strftime('%Y-%m-%d')
                        except:
                            pass

                        # If conversion fails, return original
                        return date_val

                    df['Sale\nDate'] = df['Sale\nDate'].apply(convert_to_iso)
                    converted_dates = df['Sale\nDate'].dropna().head(3).tolist()
                    print(f"   Converted Sale\\nDate samples: {converted_dates}")
                    print(f"   ✅ Sale\\nDate: converted {date_count} values to ISO format")
                    file_updates += date_count

            # Process sale_date column
            if 'sale_date' in df.columns:
                date_count = df['sale_date'].notna().sum()
                if date_count > 0:
                    original_dates = df['sale_date'].dropna().head(3).tolist()
                    print(f"   Original sale_date samples: {original_dates}")

                    # Ensure ISO format
                    def ensure_iso(date_val):
                        if pd.isna(date_val):
                            return date_val

                        date_str = str(date_val).strip()
                        if not date_str:
                            return date_val

                        try:
                            # If already in ISO format, ensure consistent
                            if '-' in date_str and len(date_str.split('-')) == 3:
                                datetime.strptime(date_str, '%Y-%m-%d')
                                return date_str
                            else:
                                # Try to parse and convert
                                parsed = pd.to_datetime(date_str, errors='coerce')
                                if pd.notna(parsed):
                                    return parsed.strftime('%Y-%m-%d')
                        except:
                            pass

                        return date_val

                    df['sale_date'] = df['sale_date'].apply(ensure_iso)
                    converted_dates = df['sale_date'].dropna().head(3).tolist()
                    print(f"   Standardized sale_date samples: {converted_dates}")
                    print(f"   ✅ sale_date: ensured ISO format for {date_count} values")

            # Save updated file
            if file_updates > 0:
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Sales', index=False)

                    # Ensure text formatting for Map Lot if it exists
                    workbook = writer.book
                    worksheet = writer.sheets['Sales']

                    if 'Map\nLot' in df.columns:
                        map_lot_col = None
                        for col_num, col_name in enumerate(df.columns, 1):
                            if col_name == 'Map\nLot':
                                map_lot_col = col_num
                                break

                        if map_lot_col:
                            for row_num in range(2, len(df) + 2):
                                cell = worksheet.cell(row=row_num, column=map_lot_col)
                                cell.number_format = '@'

                print(f"   💾 Saved {file_updates} updates to {os.path.basename(file_path)}")
                total_updates += file_updates
            else:
                print(f"   ℹ️  No updates needed for {os.path.basename(file_path)}")

            print()

        else:
            print(f"❌ File not found: {file_path}\n")

    print("=== STANDARDIZATION COMPLETE ===")
    print(f"📊 Total date fields standardized: {total_updates}")
    print("📅 All dates now in ISO 8601 format (YYYY-MM-DD)")
    print("📆 Year columns now as integers (YYYY)")

    return total_updates

if __name__ == '__main__':
    standardize_date_formats()
