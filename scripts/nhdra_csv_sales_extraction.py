#!/usr/bin/env python3
"""
Extract comprehensive sales history from NHDRA CSV flat file (city-submitted data)
"""

import csv
import pandas as pd
from datetime import datetime

def extract_nhdra_csv_sales():
    """Extract all sales data from the NHDRA CSV file into a comprehensive format"""

    print('=== EXTRACTING SALES FROM NHDRA CSV (CITY DATA) ===\n')

    nhdra_sales = []

    try:
        with open('data/raw/RawData/data/Lebanon/nhdra.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            headers = lines[1].strip().split(',')  # Second row has actual headers

            reader = csv.DictReader(lines[2:], fieldnames=headers)  # Skip first two rows

            for row in reader:
                parcel_id = f"{row.get('rem mblu map', '').strip()}-{row.get('rem mblu block', '').strip()}-{row.get('rem mblu lot', '').strip()}"

                if parcel_id and parcel_id != '--':
                    # Extract all sales for this parcel
                    parcel_sales = []

                    # Current sale (most recent)
                    current_price = row.get('saleprice', '').strip()
                    current_date = row.get('saledate', '').strip()
                    current_qualified = row.get('qualified', '').strip()

                    if current_price and current_date != '1900-01-01 00:00:00':
                        try:
                            price_val = float(current_price)
                            date_obj = pd.to_datetime(current_date)
                            parcel_sales.append({
                                'parcel_id': parcel_id,
                                'sale_date': date_obj,
                                'sale_price': price_val,
                                'sale_type': 'current',
                                'qualified': current_qualified,
                                'source': 'nhdra_csv'
                            })
                        except (ValueError, TypeError):
                            pass

                    # Prior sales (up to 3)
                    for i in range(1, 4):
                        price_key = f'ID{i} Prior Sale Price'
                        date_key = f'ID{i} Prior Sale Date'
                        book_key = f'ID{i} Prior Book Page'

                        price = row.get(price_key, '').strip()
                        date = row.get(date_key, '').strip()
                        book_page = row.get(book_key, '').strip()

                        if price and date and date != '1900-01-01 00:00:00':
                            try:
                                price_val = float(price)
                                date_obj = pd.to_datetime(date)
                                parcel_sales.append({
                                    'parcel_id': parcel_id,
                                    'sale_date': date_obj,
                                    'sale_price': price_val,
                                    'sale_type': f'prior_{i}',
                                    'book_page': book_page,
                                    'source': 'nhdra_csv'
                                })
                            except (ValueError, TypeError):
                                pass

                    # Add all sales for this parcel
                    nhdra_sales.extend(parcel_sales)

        print(f'Extracted {len(nhdra_sales)} total sales from NHDRA CSV')

        # Convert to DataFrame for analysis
        nhdra_df = pd.DataFrame(nhdra_sales)

        if not nhdra_df.empty:
            # Sort by parcel and date
            nhdra_df = nhdra_df.sort_values(['parcel_id', 'sale_date'])

            # Save comprehensive NHDRA CSV sales file
            output_path = 'data/processed/nhdra_csv_comprehensive_sales.xlsx'
            nhdra_df.to_excel(output_path, index=False)

            print(f'✅ Saved NHDRA CSV sales to: {output_path}')
            print(f'   Records: {len(nhdra_df)}')
            print(f'   Unique parcels: {nhdra_df["parcel_id"].nunique()}')

            # Sales by year
            nhdra_df['sale_year'] = nhdra_df['sale_date'].dt.year
            year_counts = nhdra_df['sale_year'].value_counts().sort_index()

            print(f'\nSales by year (NHDRA CSV):')
            for year, count in year_counts.items():
                print(f'  {year}: {count} sales')

            return nhdra_df

    except Exception as e:
        print(f'Error extracting NHDRA CSV sales: {e}')
        return None

if __name__ == '__main__':
    extract_nhdra_csv_sales()
