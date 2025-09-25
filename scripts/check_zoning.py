import csv

print('=== ZONING DATA TRANSFER CHECK ===')

# Check a few specific records
with open('data/parcels.csv', 'r') as f:
    reader = csv.DictReader(f)
    sample_processed = []
    for i, row in enumerate(reader):
        if i >= 10: break
        sample_processed.append({
            'id': row.get('parcel_id'),
            'zoning': row.get('nhdra_lnd zone', '').strip(),
            'has_nhdra': bool(row.get('nhdra_saleprice'))
        })

print('Sample processed records:')
for rec in sample_processed:
    status = 'Has NHDRA' if rec['has_nhdra'] else 'No NHDRA'
    print(f'  {rec["id"]}: zoning="{rec["zoning"]}" ({status})')

# Check raw NHDRA for comparison
print('\nChecking raw NHDRA records:')
with open('RecoveredRawData/RawData/data/Lebanon/nhdra.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip first row
    headers = next(reader)  # Get headers

    for i, row in enumerate(reader):
        if i >= 10: break
        if len(row) >= len(headers):
            row_dict = dict(zip(headers, row))

            map_val = row_dict.get('rem mblu map', '').strip()
            block_val = row_dict.get('rem mblu block', '').strip()
            lot_val = row_dict.get('rem mblu lot', '').strip()
            unit_val = row_dict.get('rem mblu unit', '').strip()

            parts = [map_val, block_val]
            if lot_val: parts.append(lot_val)
            if unit_val: parts.append(unit_val)
            nhdra_id = '-'.join(parts)

            zoning_raw = row_dict.get('lnd zone', '').strip()

            print(f'  {nhdra_id}: zoning="{zoning_raw}"')
