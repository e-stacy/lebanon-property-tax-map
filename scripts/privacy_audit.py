#!/usr/bin/env python3
import csv
import re
from collections import defaultdict

# Privacy audit patterns
privacy_patterns = {
    'po_box': re.compile(r'p\.?o\.?\s*box', re.IGNORECASE),
    'unknown': re.compile(r'unknown|confidential|protected|redacted', re.IGNORECASE),
    'single_number': re.compile(r'^\d{1,3}$'),
    'temporary': re.compile(r'temp|temporary', re.IGNORECASE),
    'generic': re.compile(r'test|sample|demo|example', re.IGNORECASE),
    'non_standard': re.compile(r'^[^a-zA-Z0-9\s#\-\.]'),
    'very_short': re.compile(r'^.{1,5}$'),
    'all_numbers': re.compile(r'^\d+$'),
}

audit_results = {
    'total_records': 0,
    'flagged_records': [],
    'pattern_counts': defaultdict(int),
    'address_patterns': defaultdict(list),
}

print('🔍 Starting Privacy Audit...')
print('=' * 50)

try:
    with open('data/parcels.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, 1):
            audit_results['total_records'] = i

            address = row.get('situs_address', '').strip()
            owner = row.get('owner_name', '').strip()
            parcel_id = row.get('parcel_id', '').strip()

            # Check for privacy flags
            privacy_flags = []

            # Address pattern checks
            if address:
                for pattern_name, pattern in privacy_patterns.items():
                    if pattern.search(address):
                        privacy_flags.append(f'address_{pattern_name}')
                        audit_results['pattern_counts'][f'address_{pattern_name}'] += 1
                        if len(audit_results['address_patterns'][pattern_name]) < 5:  # Limit examples
                            audit_results['address_patterns'][pattern_name].append(address)

            # Owner name checks
            if owner:
                if privacy_patterns['unknown'].search(owner):
                    privacy_flags.append('owner_unknown')
                    audit_results['pattern_counts']['owner_unknown'] += 1

            # Flag record if any privacy concerns
            if privacy_flags:
                audit_results['flagged_records'].append({
                    'parcel_id': parcel_id,
                    'address': address,
                    'owner': owner,
                    'flags': privacy_flags,
                    'row_number': i
                })

except Exception as e:
    print(f'❌ Error reading CSV: {e}')
    exit(1)

print(f'📊 Audit Complete')
print(f'Total Records: {audit_results["total_records"]}')
print(f'Flagged Records: {len(audit_results["flagged_records"])}')
print()

if audit_results['flagged_records']:
    print('🚨 POTENTIALLY PROTECTED RECORDS:')
    print('-' * 50)
    for record in audit_results['flagged_records'][:10]:  # Show first 10
        print(f'Parcel: {record["parcel_id"]}')
        print(f'Address: {record["address"]}')
        print(f'Owner: {record["owner"]}')
        print(f'Flags: {record["flags"]}')
        print()

    if len(audit_results['flagged_records']) > 10:
        print(f'... and {len(audit_results["flagged_records"]) - 10} more')
    print()

print('📈 PATTERN ANALYSIS:')
print('-' * 30)
for pattern, count in sorted(audit_results['pattern_counts'].items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f'{pattern}: {count} records')
        if pattern in audit_results['address_patterns'] and audit_results['address_patterns'][pattern]:
            examples = audit_results['address_patterns'][pattern][:3]
            print(f'  Examples: {examples}')
        print()

if len(audit_results['flagged_records']) == 0:
    print('✅ NO PRIVACY CONCERNS FOUND')
    print('All addresses appear to be legitimate residential/commercial addresses.')
else:
    print(f'⚠️  FOUND {len(audit_results["flagged_records"])} RECORDS WITH POTENTIAL PRIVACY CONCERNS')
    print('These should be reviewed by the city clerk before publication.')

print()
print('🔒 RECOMMENDATIONS:')
print('- Share audit results with city clerk')
print('- Flag these records in any published dataset')
print('- Consider anonymization for high-risk records')
print('- Add disclaimer about NH domestic violence protections')
