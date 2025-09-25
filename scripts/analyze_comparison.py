#!/usr/bin/env python3
"""
Analyze the NHDRA comparison file and create Excel version
"""

import pandas as pd

def analyze_comparison():
    # Convert to Excel for easier viewing
    csv_file = 'data/processed/nhdra_sales_comparison.csv'
    excel_file = 'data/processed/nhdra_sales_comparison.xlsx'

    df = pd.read_csv(csv_file)
    df.to_excel(excel_file, index=False)

    print(f'✅ Created Excel version: {excel_file}')

    # Show some statistics
    print(f'\n=== COMPARISON STATISTICS ===')
    print(f'Total parcels: {len(df) // 2}')
    print(f'Total rows: {len(df)}')

    # Count improvements using the new categories
    enhanced = df[df['data_quality_notes'].str.contains('ENHANCED', na=False)]
    validated = df[df['data_quality_notes'].str.contains('VALIDATED', na=False)]
    preserved = df[df['data_quality_notes'].str.contains('PRESERVED', na=False)]

    print(f'\nParcels with enhanced sales data: {len(enhanced) // 2}')
    print(f'Parcels with validated sales data: {len(validated) // 2}')
    print(f'Parcels with preserved sales data: {len(preserved) // 2}')

    # Show a few examples of enhancements
    print(f'\n=== SAMPLE ENHANCEMENTS ===')
    enhancement_examples = df[df['data_quality_notes'].str.contains('ENHANCED', na=False)].head(8)  # Get more rows
    current_parcel = None

    for _, row in enhancement_examples.iterrows():
        if row['comparison_type'] == 'ORIGINAL_NHDRA':
            current_parcel = row['parcel_id']
            print(f"\nParcel {row['parcel_id']}:")
            original_sales = sum(1 for col in ['current_sale_price', 'prior1_sale_price', 'prior2_sale_price', 'prior3_sale_price']
                               if pd.notna(row[col]) and str(row[col]).strip() and str(row[col]) != '0.0' and str(row[col]) != '')
            print(f"  Original: {original_sales} sales")
        elif row['comparison_type'] == 'CORRECTED_COMPREHENSIVE':
            corrected_sales = sum(1 for col in ['current_sale_price', 'prior1_sale_price', 'prior2_sale_price', 'prior3_sale_price']
                                if pd.notna(row[col]) and str(row[col]).strip() and str(row[col]) != '0.0' and str(row[col]) != '')
            print(f"  Corrected: {corrected_sales} sales")
            print(f"  {row['data_quality_notes']}")

    print(f'\n=== HOW TO USE THIS FILE ===')
    print('1. Open nhdra_sales_comparison.xlsx in Excel or similar')
    print('2. Filter by "comparison_type" column to see ORIGINAL vs CORRECTED')
    print('3. Sort by "data_quality_notes" to see improvement examples')
    print('4. Compare sales data columns to see missing/inaccurate data')
    print('\nThis file proves that proper data management can significantly')
    print('improve the quality and completeness of property tax records!')

if __name__ == '__main__':
    analyze_comparison()
