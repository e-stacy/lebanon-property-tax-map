import csv

print('=== ZONING PATTERNS ANALYSIS ===')

# Analyze what types of properties are missing zoning
missing_zoning_analysis = {
    'by_use_code': {},
    'by_neighborhood': {},
    'by_sale_price': {'0': 0, '1-100k': 0, '100k-500k': 0, '500k+': 0},
    'total_missing': 0
}

# Load processed data
with open('data/parcels.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        has_nhdra = bool(row.get('nhdra_saleprice'))
        zoning = row.get('nhdra_lnd zone', '').strip()

        if has_nhdra:
            use_code = row.get('nhdra_rem use code', '').strip()
            neighborhood = row.get('nhdra_lnd nbhd', '').strip()

            if not zoning:
                missing_zoning_analysis['total_missing'] += 1

                # Count by use code
                if use_code not in missing_zoning_analysis['by_use_code']:
                    missing_zoning_analysis['by_use_code'][use_code] = 0
                missing_zoning_analysis['by_use_code'][use_code] += 1

                # Count by neighborhood
                if neighborhood not in missing_zoning_analysis['by_neighborhood']:
                    missing_zoning_analysis['by_neighborhood'][neighborhood] = 0
                missing_zoning_analysis['by_neighborhood'][neighborhood] += 1

                # Count by sale price range
                try:
                    price = float(row.get('nhdra_saleprice', 0))
                    if price == 0:
                        missing_zoning_analysis['by_sale_price']['0'] += 1
                    elif price < 100000:
                        missing_zoning_analysis['by_sale_price']['1-100k'] += 1
                    elif price < 500000:
                        missing_zoning_analysis['by_sale_price']['100k-500k'] += 1
                    else:
                        missing_zoning_analysis['by_sale_price']['500k+'] += 1
                except (ValueError, TypeError):
                    missing_zoning_analysis['by_sale_price']['0'] += 1

print(f"Total parcels with NHDRA data missing zoning: {missing_zoning_analysis['total_missing']}")

print(f"\nMissing zoning by property use code (top 5):")
sorted_use_codes = sorted(missing_zoning_analysis['by_use_code'].items(), key=lambda x: x[1], reverse=True)[:5]
for code, count in sorted_use_codes:
    print(f"  {code}: {count} parcels")

print(f"\nMissing zoning by land neighborhood (top 5):")
sorted_neighborhoods = sorted(missing_zoning_analysis['by_neighborhood'].items(), key=lambda x: x[1], reverse=True)[:5]
for nbhd, count in sorted_neighborhoods:
    print(f"  {nbhd}: {count} parcels")

print(f"\nMissing zoning by sale price range:")
for price_range, count in missing_zoning_analysis['by_sale_price'].items():
    print(f"  {price_range}: {count} parcels")

# Check if land neighborhood could be a proxy for zoning
print(f"\n=== LAND NEIGHBORHOOD AS ZONING PROXY ===")
zoning_by_neighborhood = {}
with open('data/parcels.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        zoning = row.get('nhdra_lnd zone', '').strip()
        neighborhood = row.get('nhdra_lnd nbhd', '').strip()

        if zoning and neighborhood:
            key = f"{neighborhood}->{zoning}"
            if key not in zoning_by_neighborhood:
                zoning_by_neighborhood[key] = 0
            zoning_by_neighborhood[key] += 1

print("Common neighborhood->zoning mappings:")
sorted_mappings = sorted(zoning_by_neighborhood.items(), key=lambda x: x[1], reverse=True)[:10]
for mapping, count in sorted_mappings:
    print(f"  {mapping}: {count} parcels")
