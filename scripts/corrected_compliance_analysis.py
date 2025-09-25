#!/usr/bin/env python3
"""
Corrected City Compliance Analysis - Based on Actual Data Provided
"""

def corrected_compliance_analysis():
    print('=== CORRECTED CITY COMPLIANCE ASSESSMENT ===\n')

    # What the user actually received from the city
    city_provided_actual = {
        'nhdra.csv': [
            'All NHDRA merged data', 'Property identifiers', 'Assessment values',
            'Sales history (some)', 'Zoning information', 'Building details',
            'Complete merged dataset from state submission'
        ]
    }

    # What the user had to obtain separately
    obtained_separately = {
        'Vision Exports': [
            'Parcel Master Export.csv', 'Building Export.csv', 'Land Export.csv'
        ],
        'Sales Data': [
            'SalesList Excel files (2020-2024)', 'Obtained via separate NHDRA FOIA'
        ]
    }

    print('WHAT CITY ACTUALLY PROVIDED:')
    print(f'  • 1 CSV file: nhdra.csv ({len(city_provided_actual["nhdra.csv"])} data categories)')
    print()

    print('WHAT USER HAD TO OBTAIN SEPARATELY:')
    for source, items in obtained_separately.items():
        print(f'  • {source}:')
        for item in items:
            print(f'    - {item}')
    print()

    # Check what's in nhdra.csv vs Vision exports
    try:
        with open('data/raw/RawData/data/Lebanon/nhdra.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            header_row = lines[1]  # Second row has actual headers
            headers = header_row.strip().split(',')
            print(f'NHDRA CSV FIELDS: {len(headers)}')
            print('Sample fields:', headers[:10])

            # Check for key fields
            key_indicators = ['map', 'block', 'lot', 'use', 'zone', 'ayb', 'fuel', 'sale']
            field_counts = {}
            for indicator in key_indicators:
                count = sum(1 for h in headers if indicator.lower() in h.lower())
                field_counts[indicator] = count

            print('\nKey field coverage in NHDRA:')
            for indicator, count in field_counts.items():
                status = '✅' if count > 0 else '❌'
                print(f'  {indicator.upper():6}: {status} {count} fields')

    except Exception as e:
        print(f'Error reading nhdra.csv: {e}')

    print()
    print('REVISED COMPLIANCE ASSESSMENT:')
    print('❌ TECHNICAL NON-COMPLIANCE:')
    print('  • Only provided 1 pre-compiled file instead of raw system exports')
    print('  • Did not provide direct Vision Government Solutions access')
    print('  • Forced user to make multiple FOIA requests')
    print()
    print('❌ SUBSTANTIVE NON-COMPLIANCE:')
    print('  • Sales data incomplete (only recent years via separate request)')
    print('  • No direct access to live Vision system data')
    print('  • Data compilation method unclear')
    print()
    print('CONCLUSION:')
    print('City provided minimal compliance - one compiled file instead of full system access.')
    print('User had to piece together data from multiple sources and FOIA requests.')

if __name__ == '__main__':
    corrected_compliance_analysis()
