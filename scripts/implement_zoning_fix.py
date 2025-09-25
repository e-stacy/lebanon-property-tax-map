import csv
import json

print('=== IMPLEMENTING ZONING FIX ===')

# Load the zoning mapping
with open('zoning_mapping.json', 'r') as f:
    zoning_mapping = json.load(f)

print(f'Loaded zoning mapping for {len(zoning_mapping)} neighborhoods')

# Read the current data and apply zoning fixes
parcels = []
fixed_count = 0

with open('data/parcels.csv', 'r') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    for row in reader:
        original_zoning = row.get('nhdra_lnd zone', '').strip()
        neighborhood = row.get('nhdra_lnd nbhd', '').strip()
        has_nhdra = bool(row.get('nhdra_saleprice'))

        # Apply zoning fix if conditions are met
        if has_nhdra and not original_zoning and neighborhood in zoning_mapping:
            new_zoning = zoning_mapping[neighborhood]
            row['nhdra_lnd zone'] = new_zoning
            fixed_count += 1
            print(f'Fixed {row["parcel_id"]}: {neighborhood} -> {new_zoning}')

        parcels.append(row)

print(f'\nFixed zoning for {fixed_count} parcels')

# Write the updated data back
with open('data/parcels.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(parcels)

print('Updated data/parcels.csv with zoning fixes')

# Log the changes
with open('artifacts/zoning_fix_log.txt', 'w') as f:
    f.write(f'Zoning Fix Applied: {fixed_count} parcels\n')
    f.write(f'Mapping used: zoning_mapping.json\n')
    f.write(f'Backup saved as: data/parcels_backup_before_zoning_fix.csv\n')

print('Changes logged to artifacts/zoning_fix_log.txt')
