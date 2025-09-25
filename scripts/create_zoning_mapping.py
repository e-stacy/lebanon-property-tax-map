import csv
from collections import defaultdict

print('=== CREATING ZONING MAPPING STRATEGY ===')

# Create neighborhood -> zoning mapping from existing data
neighborhood_zoning_map = defaultdict(lambda: defaultdict(int))

# Load processed data and build mapping
with open('data/parcels.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        zoning = row.get('nhdra_lnd zone', '').strip()
        neighborhood = row.get('nhdra_lnd nbhd', '').strip()

        if zoning and neighborhood:
            neighborhood_zoning_map[neighborhood][zoning] += 1

# Create the mapping: neighborhood -> most common zoning
zoning_mapping = {}
for neighborhood, zoning_counts in neighborhood_zoning_map.items():
    most_common_zoning = max(zoning_counts.items(), key=lambda x: x[1])[0]
    zoning_mapping[neighborhood] = most_common_zoning

print(f'Created mapping for {len(zoning_mapping)} neighborhoods:')

# Show the mapping
for neighborhood in sorted(zoning_mapping.keys()):
    zoning = zoning_mapping[neighborhood]
    count = neighborhood_zoning_map[neighborhood][zoning]
    print(f'  {neighborhood} -> {zoning} ({count} parcels)')

# Count how many missing zoning parcels we can fix
missing_can_fix = 0
with open('data/parcels.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        has_nhdra = bool(row.get('nhdra_saleprice'))
        zoning = row.get('nhdra_lnd zone', '').strip()
        neighborhood = row.get('nhdra_lnd nbhd', '').strip()

        if has_nhdra and not zoning and neighborhood in zoning_mapping:
            missing_can_fix += 1

print(f'\nCan fix zoning for {missing_can_fix} parcels using neighborhood mapping')

# Show what percentage this represents
total_missing = 1253  # From previous analysis
print(f'This represents {missing_can_fix/total_missing*100:.1f}% of missing zoning parcels')

# Save the mapping for use in the fix
import json
with open('zoning_mapping.json', 'w') as f:
    json.dump(zoning_mapping, f, indent=2)

print('\nSaved zoning mapping to zoning_mapping.json')
