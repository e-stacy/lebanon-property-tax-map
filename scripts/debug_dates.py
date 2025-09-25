#!/usr/bin/env python3
"""Debug date filtering issue"""

import pandas as pd

# Load annual sales
annual = pd.read_excel('data/processed/comprehensive_sales_2020-2024.xlsx')
annual['sale_date'] = pd.to_datetime(annual['Sale\nDate'], errors='coerce')

print('Annual sales date analysis:')
print(f'Total records: {len(annual)}')
print(f'Null dates: {annual["sale_date"].isna().sum()}')
print(f'Min date: {annual["sale_date"].min()}')
print(f'Max date: {annual["sale_date"].max()}')

print('\nFirst 5 dates:')
for i in range(5):
    print(f'  {annual["sale_date"].iloc[i]}')

# Test filtering
start_date = pd.Timestamp('2019-10-01')
end_date = pd.Timestamp('2024-09-30')

filtered = annual[
    (annual['sale_date'] >= start_date) &
    (annual['sale_date'] <= end_date)
]

print(f'\nFiltering {start_date} to {end_date}:')
print(f'  Results: {len(filtered)} records')

# Check why no records match
print('\nDebugging filter:')
print(f'  Records >= start_date: {len(annual[annual["sale_date"] >= start_date])}')
print(f'  Records <= end_date: {len(annual[annual["sale_date"] <= end_date])}')
print(f'  Records in range: {len(annual[(annual["sale_date"] >= start_date) & (annual["sale_date"] <= end_date)])}')
