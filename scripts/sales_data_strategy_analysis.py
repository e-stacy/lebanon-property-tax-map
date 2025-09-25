#!/usr/bin/env python3
"""
Analyze sales data availability and validate the user's proposed data strategy
"""

import pandas as pd
from datetime import datetime

def analyze_sales_strategy():
    """Analyze the user's proposed sales data strategy"""

    print('=== SALES DATA STRATEGY ANALYSIS ===\n')

    # Load available data sources
    sources = {}

    # Annual combined sales (high quality, complete metadata)
    try:
        annual = pd.read_excel('data/processed/comprehensive_sales_2020-2024.xlsx')
        annual['sale_date'] = pd.to_datetime(annual['Sale\nDate'], errors='coerce')
        sources['annual_combined'] = annual
        print(f'✅ Annual Combined: {len(annual)} records')
    except Exception as e:
        print(f'❌ Annual Combined: {e}')

    # NHDRA CSV sales (comprehensive but mixed quality)
    try:
        nhdra = pd.read_excel('data/processed/nhdra_csv_comprehensive_sales.xlsx')
        sources['nhdra_csv'] = nhdra
        print(f'✅ NHDRA CSV: {len(nhdra)} records')
    except Exception as e:
        print(f'❌ NHDRA CSV: {e}')

    if not sources:
        print('No data sources available')
        return

    # Analyze time period coverage
    print('\n=== TIME PERIOD COVERAGE ===')

    periods = [
        ('2025 to 10/1/2024', pd.Timestamp('2024-10-01'), pd.Timestamp('2025-12-31')),
        ('10/1/2019 to 9/30/2024', pd.Timestamp('2019-10-01'), pd.Timestamp('2024-09-30')),
        ('Before 10/1/2019', pd.Timestamp('1800-01-01'), pd.Timestamp('2019-09-30'))
    ]

    period_coverage = {}

    for period_name, start_date, end_date in periods:
        print(f'\n{period_name}:')
        period_coverage[period_name] = {}

        for source_name, df in sources.items():
            if 'sale_date' in df.columns:
                period_sales = df[
                    (df['sale_date'] >= start_date) &
                    (df['sale_date'] <= end_date)
                ]

                # Filter for valid sales
                if source_name == 'annual_combined':
                    price_col = 'Verified\nPrice'
                else:
                    price_col = 'sale_price'

                # Convert price to numeric for comparison
                period_sales[price_col] = pd.to_numeric(period_sales[price_col], errors='coerce')

                valid_sales = period_sales[
                    (period_sales[price_col] > 0) &
                    (period_sales[price_col].notna()) &
                    (period_sales['sale_date'] > pd.Timestamp('1900-01-01'))
                ]

                print(f'  {source_name.upper()}: {len(valid_sales)} valid sales')
                period_coverage[period_name][source_name] = len(valid_sales)
            else:
                print(f'  {source_name.upper()}: Date column issue')
                period_coverage[period_name][source_name] = 0

    # User's proposed strategy
    print('\n=== USER PROPOSED STRATEGY ===')
    print('1. 2025 to 10/1/2024: NHDRA CSV (only source)')
    print('2. 10/1/2019 to 9/30/2024: Annual Combined (higher quality)')
    print('3. Before 10/1/2019: NHDRA CSV (only source)')

    # Validate strategy
    print('\n=== STRATEGY VALIDATION ===')

    strategy_issues = []

    # Check Period 1: 2025 to 10/1/2024
    period1_nhdra = period_coverage['2025 to 10/1/2024']['nhdra_csv']
    period1_annual = period_coverage['2025 to 10/1/2024']['annual_combined']

    print(f'Period 1 (2025 to 10/1/2024):')
    print(f'  NHDRA CSV: {period1_nhdra} sales')
    print(f'  Annual: {period1_annual} sales')

    if period1_annual > period1_nhdra:
        strategy_issues.append('Annual files have more 2025 sales than NHDRA CSV - consider using annual data')

    # Check Period 2: 10/1/2019 to 9/30/2024
    period2_nhdra = period_coverage['10/1/2019 to 9/30/2024']['nhdra_csv']
    period2_annual = period_coverage['10/1/2019 to 9/30/2024']['annual_combined']

    print(f'\nPeriod 2 (10/1/2019 to 9/30/2024):')
    print(f'  NHDRA CSV: {period2_nhdra} sales')
    print(f'  Annual: {period2_annual} sales')

    if period2_nhdra > period2_annual * 2:
        strategy_issues.append('NHDRA CSV has significantly more sales than annual files - possible data quality issues')

    # Check Period 3: Before 10/1/2019
    period3_nhdra = period_coverage['Before 10/1/2019']['nhdra_csv']
    period3_annual = period_coverage['Before 10/1/2019']['annual_combined']

    print(f'\nPeriod 3 (Before 10/1/2019):')
    print(f'  NHDRA CSV: {period3_nhdra} sales')
    print(f'  Annual: {period3_annual} sales')

    if period3_annual > 0:
        strategy_issues.append('Annual files contain pre-2019 sales - unexpected')

    # Overall assessment
    print('\n=== STRATEGY ASSESSMENT ===')

    if not strategy_issues:
        print('✅ STRATEGY VALID: Your proposed hierarchy appears sound')
        print('   - Uses highest quality data where available')
        print('   - Falls back to available sources appropriately')
    else:
        print('⚠️ STRATEGY ISSUES FOUND:')
        for issue in strategy_issues:
            print(f'   • {issue}')

    # Alternative recommendations
    print('\n=== ALTERNATIVE RECOMMENDATIONS ===')
    print('1. Validate all sales prices > $1,000 (filter out $0/placeholder entries)')
    print('2. Cross-reference overlapping parcels between sources')
    print('3. Flag sales with invalid dates (1901-01-01, etc.)')
    print('4. Prefer Annual Combined for 2019-2024 (better metadata)')
    print('5. Use NHDRA CSV only for 2025 and historical data')

    # Create implementation summary
    print('\n=== IMPLEMENTATION SUMMARY ===')
    total_sales = sum(len(df) for df in sources.values())
    print(f'Total sales available: {total_sales}')

    recommended_sales = (
        period_coverage['2025 to 10/1/2024']['nhdra_csv'] +
        period_coverage['10/1/2019 to 9/30/2024']['annual_combined'] +
        period_coverage['Before 10/1/2019']['nhdra_csv']
    )
    print(f'Sales in recommended strategy: {recommended_sales}')
    print(f'Coverage: {recommended_sales/total_sales*100:.1f}% of available data')

if __name__ == '__main__':
    analyze_sales_strategy()
