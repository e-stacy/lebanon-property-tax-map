#!/usr/bin/env python3
"""
Create NHDRA comparison file showing original vs corrected sales data
"""

import pandas as pd
import csv
from collections import defaultdict

def create_nhdra_comparison():
    print("=== CREATING NHDRA SALES DATA COMPARISON ===\n")

    # Read NHDRA original data
    print("Reading original NHDRA CSV...")
    nhdra_df = pd.read_csv('data/raw/RawData/data/Lebanon/nhdra.csv', header=1)  # Skip first row of unnameds
    print(f"Loaded {len(nhdra_df)} parcels from NHDRA")

    # Read our comprehensive sales data
    print("Reading comprehensive sales data...")
    sales_df = pd.read_csv('data/processed/final_property_sales_dataset.csv')
    print(f"Loaded {len(sales_df)} sales records")

    # Group sales by parcel_id for quick lookup
    sales_by_parcel = defaultdict(list)
    for _, sale in sales_df.iterrows():
        parcel_id = sale['parcel_id']
        sales_by_parcel[parcel_id].append(sale)

    # Sort sales by date for each parcel (most recent first)
    for parcel_id in sales_by_parcel:
        sales_by_parcel[parcel_id].sort(key=lambda x: x['sale_date'], reverse=True)

    # Create output CSV
    output_file = 'data/processed/nhdra_sales_comparison.csv'
    fieldnames = [
        'comparison_type', 'parcel_id', 'map', 'block', 'lot',
        'current_sale_price', 'current_sale_date', 'current_qualified', 'current_book_page',
        'prior1_sale_price', 'prior1_sale_date', 'prior1_book_page',
        'prior2_sale_price', 'prior2_sale_date', 'prior2_book_page',
        'prior3_sale_price', 'prior3_sale_date', 'prior3_book_page',
        'data_quality_notes'
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        processed_parcels = 0

        for _, nhdra_row in nhdra_df.iterrows():
            # Extract parcel ID components
            map_num = str(nhdra_row.get('rem mblu map', '')).strip()
            block = str(nhdra_row.get('rem mblu block', '')).strip()
            lot = str(nhdra_row.get('rem mblu lot', '')).strip()

            # Create parcel ID (handle empty/missing components)
            parcel_id_parts = [map_num, block, lot]
            parcel_id_parts = [p for p in parcel_id_parts if p and p != 'nan' and p != '']
            parcel_id = '-'.join(parcel_id_parts) if parcel_id_parts else 'unknown'

            # Skip if we can't create a meaningful parcel ID
            if parcel_id == 'unknown' or len(parcel_id_parts) < 2:
                continue

            processed_parcels += 1

            # ORIGINAL NHDRA DATA ROW
            original_row = {
                'comparison_type': 'ORIGINAL_NHDRA',
                'parcel_id': parcel_id,
                'map': map_num,
                'block': block,
                'lot': lot,
                'current_sale_price': nhdra_row.get('saleprice', ''),
                'current_sale_date': str(nhdra_row.get('saledate', '')).split(' ')[0] if pd.notna(nhdra_row.get('saledate')) else '',
                'current_qualified': nhdra_row.get('qualified', ''),
                'current_book_page': nhdra_row.get('book pg', ''),
                'prior1_sale_price': nhdra_row.get('ID1 Prior Sale Price', ''),
                'prior1_sale_date': str(nhdra_row.get('ID1 Prior Sale Date', '')).split(' ')[0] if pd.notna(nhdra_row.get('ID1 Prior Sale Date')) else '',
                'prior1_book_page': nhdra_row.get('ID1 Prior Book Page', ''),
                'prior2_sale_price': nhdra_row.get('ID2 Prior Sale Price', ''),
                'prior2_sale_date': str(nhdra_row.get('ID2 Prior Sale Date', '')).split(' ')[0] if pd.notna(nhdra_row.get('ID2 Prior Sale Date')) else '',
                'prior2_book_page': nhdra_row.get('ID2 Prior Book Page', ''),
                'prior3_sale_price': nhdra_row.get('ID3 Prior Sale Price', ''),
                'prior3_sale_date': str(nhdra_row.get('ID3 Prior Sale Date', '')).split(' ')[0] if pd.notna(nhdra_row.get('ID3 Prior Sale Date')) else '',
                'prior3_book_page': nhdra_row.get('ID3 Prior Book Page', ''),
                'data_quality_notes': 'Original NHDRA flat file data'
            }
            writer.writerow(original_row)

            # CORRECTED DATA ROW
            corrected_row = {
                'comparison_type': 'CORRECTED_COMPREHENSIVE',
                'parcel_id': parcel_id,
                'map': map_num,
                'block': block,
                'lot': lot,
                'data_quality_notes': 'Comprehensive sales data from multiple sources'
            }

            # Create truly comprehensive sales data by combining ALL sources
            # Start with original NHDRA data as foundation, then add enhancements
            all_sales = []

            # Add ALL original NHDRA sales first (they include metadata like book_page)
            # Current sale - include even if $0 as it represents a transaction
            current_price = nhdra_row.get('saleprice')
            if current_price is not None and str(current_price).strip():
                try:
                    price_val = float(current_price)
                    all_sales.append({
                        'sale_price': price_val,
                        'sale_date': nhdra_row.get('saledate'),
                        'qualified': nhdra_row.get('qualified', 'Q'),
                        'book_page': nhdra_row.get('book pg', ''),
                        'source': 'original_nhdra_current'
                    })
                except (ValueError, TypeError):
                    pass  # Skip invalid prices

            # Prior sales - include even if $0 as they represent transaction history
            for i in range(1, 4):
                price_field = f'ID{i} Prior Sale Price'
                date_field = f'ID{i} Prior Sale Date'
                book_field = f'ID{i} Prior Book Page'

                price = nhdra_row.get(price_field)
                if price is not None and str(price).strip():
                    try:
                        price_val = float(price)
                        all_sales.append({
                            'sale_price': price_val,
                            'sale_date': nhdra_row.get(date_field),
                            'qualified': 'Q',  # Prior sales typically qualified
                            'book_page': nhdra_row.get(book_field, ''),
                            'source': f'original_nhdra_prior{i}'
                        })
                    except (ValueError, TypeError):
                        pass  # Skip invalid prices

            # Add our merged comprehensive data as enhancements (only if they add new information)
            merged_sales = sales_by_parcel.get(parcel_id, [])
            for sale in merged_sales:
                sale_price = sale.get('sale_price')
                if pd.notna(sale_price) and sale_price > 0:
                    # Check if this sale already exists in our collection
                    exists = any(
                        abs(float(sale_price) - float(existing['sale_price'])) < 1 and
                        str(sale['sale_date']).split(' ')[0] == str(existing['sale_date']).split(' ')[0]
                        for existing in all_sales
                        if existing['sale_price'] > 0  # Only compare with non-zero prices
                    )
                    if not exists:
                        all_sales.append({
                            'sale_price': float(sale_price),
                            'sale_date': sale.get('sale_date'),
                            'qualified': sale.get('qualified', 'Q'),
                            'book_page': sale.get('book_page', ''),  # May be empty for recent sales
                            'source': sale.get('data_source', 'comprehensive_merged')
                        })

            # Remove duplicates more intelligently
            # Consider sales duplicates if they have the same date and price is very close
            unique_sales = []
            for sale in all_sales:
                if pd.isna(sale['sale_date']):
                    continue  # Skip sales without dates

                sale_date = str(sale['sale_date']).split(' ')[0]
                sale_price = sale['sale_price']

                is_duplicate = False
                for existing in unique_sales:
                    existing_date = str(existing['sale_date']).split(' ')[0]
                    existing_price = existing['sale_price']

                    # Same date and price difference < $1 = duplicate
                    if (sale_date == existing_date and
                        abs(float(sale_price) - float(existing_price)) < 1):
                        is_duplicate = True
                        break

                if not is_duplicate:
                    unique_sales.append(sale)

            # Sort by date (most recent first)
            def safe_date_sort(sale):
                date_val = sale.get('sale_date')
                if pd.isna(date_val) or date_val is None:
                    return '1900-01-01'
                return str(date_val).split(' ')[0]

            comprehensive_sales = sorted(unique_sales, key=safe_date_sort, reverse=True)

            # Fill in the 4 sales slots with truly comprehensive data
            for i, sale in enumerate(comprehensive_sales[:4]):  # Take up to 4 most recent sales
                sale_date = str(sale['sale_date']).split(' ')[0] if pd.notna(sale['sale_date']) else ''
                sale_price = sale['sale_price'] if pd.notna(sale['sale_price']) else ''

                if i == 0:  # Current/most recent sale
                    corrected_row['current_sale_price'] = sale_price
                    corrected_row['current_sale_date'] = sale_date
                    corrected_row['current_qualified'] = sale.get('qualified', 'Q')  # Assume qualified
                    corrected_row['current_book_page'] = sale.get('book_page', '')
                elif i == 1:  # Prior sale 1
                    corrected_row['prior1_sale_price'] = sale_price
                    corrected_row['prior1_sale_date'] = sale_date
                    corrected_row['prior1_book_page'] = sale.get('book_page', '')
                elif i == 2:  # Prior sale 2
                    corrected_row['prior2_sale_price'] = sale_price
                    corrected_row['prior2_sale_date'] = sale_date
                    corrected_row['prior2_book_page'] = sale.get('book_page', '')
                elif i == 3:  # Prior sale 3
                    corrected_row['prior3_sale_price'] = sale_price
                    corrected_row['prior3_sale_date'] = sale_date
                    corrected_row['prior3_book_page'] = sale.get('book_page', '')

            # Add quality improvement notes
            original_sales = sum(1 for key in ['current_sale_price', 'prior1_sale_price', 'prior2_sale_price', 'prior3_sale_price']
                               if original_row.get(key) and str(original_row[key]).strip() and str(original_row[key]) != '0')
            corrected_sales = sum(1 for key in ['current_sale_price', 'prior1_sale_price', 'prior2_sale_price', 'prior3_sale_price']
                                if corrected_row.get(key) and str(corrected_row[key]).strip() and str(corrected_row[key]) != '0')

            # Count additional sources used
            sources_used = set()
            for sale in comprehensive_sales[:4]:
                sources_used.add(sale.get('source', 'unknown'))

            additional_sources = sources_used - {'original_nhdra_fallback'}

            if corrected_sales > original_sales:
                corrected_row['data_quality_notes'] += f' - ENHANCED: {original_sales} → {corrected_sales} sales from {len(sources_used)} sources'
            elif len(additional_sources) > 0:
                corrected_row['data_quality_notes'] += f' - VALIDATED: {corrected_sales} sales from {len(sources_used)} sources (includes original data)'
            else:
                corrected_row['data_quality_notes'] += f' - PRESERVED: {corrected_sales} sales from original NHDRA data'

            writer.writerow(corrected_row)

    print(f"\n✅ Created comparison file: {output_file}")
    print(f"Processed {processed_parcels} parcels")
    print(f"Total rows in output: {processed_parcels * 2}")  # 2 rows per parcel

    # Create a summary
    print("\n=== DATA QUALITY IMPROVEMENT SUMMARY ===")
    print("This file demonstrates how the city's NHDRA data can be significantly improved by:")
    print("1. Cross-referencing multiple data sources")
    print("2. Filling missing sales data")
    print("3. Correcting inaccurate or incomplete records")
    print("4. Providing comprehensive historical context")
    print("\nEach parcel has TWO rows:")
    print("- ORIGINAL_NHDRA: What the city currently has")
    print("- CORRECTED_COMPREHENSIVE: What it should be with proper data management")

    return output_file

if __name__ == '__main__':
    create_nhdra_comparison()
