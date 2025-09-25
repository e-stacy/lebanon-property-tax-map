#!/usr/bin/env python3
"""
Analyze date formats across all processed files
"""

import pandas as pd
import os

def analyze_date_formats():
    print("=== DATE FORMAT ANALYSIS ACROSS PROCESSED FILES ===\n")

    # Files to check
    files_to_check = [
        'data/processed/sales-data-09-25-25.xlsx',
        'data/processed/SalesList_2020-2024_combined.xlsx',
        'data/processed/nhdra.xlsx',
        'data/processed/nhdra-sales.xlsx'
    ]

    date_formats = {}

    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path)
                print(f"📄 {os.path.basename(file_path)}:")
                print(f"   Shape: {df.shape}")

                # Check for date-related columns
                date_cols = [col for col in df.columns if 'date' in col.lower() or col == 'Year']

                for col in date_cols:
                    if col in df.columns:
                        non_null_count = df[col].notna().sum()
                        if non_null_count > 0:
                            sample_vals = df[col].dropna().head(5).tolist()
                            data_type = str(df[col].dtype)

                            print(f"   {col}:")
                            print(f"     Non-null: {non_null_count}")
                            print(f"     Data type: {data_type}")
                            print(f"     Samples: {sample_vals}")

                            # Track format patterns
                            if col not in date_formats:
                                date_formats[col] = {}

                            # Analyze format patterns
                            if 'datetime' in data_type.lower():
                                date_formats[col]['datetime64'] = date_formats[col].get('datetime64', 0) + 1
                            elif 'int' in data_type.lower():
                                date_formats[col]['integer'] = date_formats[col].get('integer', 0) + 1
                            elif 'float' in data_type.lower():
                                date_formats[col]['float'] = date_formats[col].get('float', 0) + 1
                            elif 'object' in data_type.lower():
                                # Check if string dates
                                string_dates = [str(x) for x in sample_vals if pd.notna(x)]
                                if string_dates:
                                    # Check for YYYY-MM-DD pattern
                                    has_iso = any('-' in str(x) and len(str(x).split('-')) == 3 for x in string_dates)
                                    has_us = any('/' in str(x) for x in string_dates)
                                    has_year_only = all(len(str(x)) == 4 and str(x).isdigit() for x in string_dates)

                                    if has_year_only:
                                        date_formats[col]['year_only'] = date_formats[col].get('year_only', 0) + 1
                                    elif has_iso:
                                        date_formats[col]['string_iso'] = date_formats[col].get('string_iso', 0) + 1
                                    elif has_us:
                                        date_formats[col]['string_us'] = date_formats[col].get('string_us', 0) + 1
                                    else:
                                        date_formats[col]['string_other'] = date_formats[col].get('string_other', 0) + 1

                print()

            except Exception as e:
                print(f"   ❌ Error reading {os.path.basename(file_path)}: {e}\n")
        else:
            print(f"📄 {os.path.basename(file_path)}: File not found\n")

    # Summary and recommendations
    print("=== DATE FORMAT SUMMARY ===\n")

    for col, formats in date_formats.items():
        print(f"📅 {col}:")
        for fmt, count in formats.items():
            print(f"   {fmt}: {count} files")
        print()

    # Check for inconsistencies
    inconsistencies = []
    for col, formats in date_formats.items():
        if len(formats) > 1:
            inconsistencies.append(col)

    if inconsistencies:
        print("⚠️  INCONSISTENCIES FOUND:")
        for col in inconsistencies:
            print(f"   {col}: {date_formats[col]}")

        print("\n💡 RECOMMENDED STANDARD FORMAT:")
        print("   Date columns: YYYY-MM-DD (ISO 8601)")
        print("   Year columns: YYYY (4-digit year)")
        print("   Reason: ISO format is unambiguous, sortable, and Excel-compatible")
        print("   Example: '2023-12-25' instead of '12/25/2023'")
    else:
        print("✅ All date formats are consistent across files!")

    return date_formats

if __name__ == '__main__':
    analyze_date_formats()
