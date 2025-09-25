#!/usr/bin/env python3
import csv
import json
import sys

def analyze_nhdra_keys():
    print("=== NHDRA DATA STRUCTURE ANALYSIS ===")
    try:
        with open('RecoveredRawData/RawData/data/Lebanon/nhdra.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Skip first row (Unnamed), use second row as headers
            next(reader)
            headers = next(reader)

            sample_rows = []
            for i, row in enumerate(reader):
                if i >= 5: break  # Just first 5 samples
                if len(row) >= len(headers):
                    row_dict = dict(zip(headers, row))
                    sample_rows.append({
                        'map': row_dict.get('rem mblu map', '').strip(),
                        'block': row_dict.get('rem mblu block', '').strip(),
                        'lot': row_dict.get('rem mblu lot', '').strip(),
                        'unit': row_dict.get('rem mblu unit', '').strip(),
                        'address': (row_dict.get('rem prcl locn', '') or '').strip()[:40],
                        'owner': (row_dict.get('own name', '') or '').strip()[:25],
                        'use_code': row_dict.get('rem use code', '').strip(),
                    })

        for i, row in enumerate(sample_rows):
            key_parts = [row['map'], row['block']]
            if row['lot']: key_parts.append(row['lot'])
            if row['unit']: key_parts.append(row['unit'])
            constructed_key = '-'.join(key_parts)

            print(f"{i+1}: Map={row['map']}, Block={row['block']}, Lot={row['lot']}, Unit={row['unit']}")
            print(f"   -> '{constructed_key}' | {row['address']} | {row['owner']} | Use: {row['use_code']}")

    except Exception as e:
        print(f"Error analyzing NHDRA: {e}")

def analyze_spatial_keys():
    print("\n=== SPATIAL DATA ANALYSIS ===")
    try:
        with open('RecoveredRawData/spatial/parcels_wgs84.geojson', 'r', encoding='utf-8') as f:
            data = json.load(f)
            features = data.get('features', [])
            print(f"Spatial features: {len(features)}")

            # Sample first 5 MAP_LOT values
            map_lots = []
            for feature in features[:5]:
                props = feature.get('properties', {})
                map_lot = props.get('MAP_LOT', 'MISSING')
                map_lots.append(map_lot)

            print(f"Sample MAP_LOT values: {map_lots}")

    except Exception as e:
        print(f"Error analyzing spatial data: {e}")

def analyze_parcel_keys():
    print("\n=== PARCEL DATA ANALYSIS ===")
    try:
        with open('RecoveredRawData/RawData/data/Lebanon/parcels.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            sample_rows = []
            for i, row in enumerate(reader):
                if i >= 5: break
                sample_rows.append({
                    'parcel_id': row.get('parcel_id', '').strip(),
                    'owner': (row.get('owner_name', '') or '').strip()[:25],
                    'address': (row.get('situs_address', '') or '').strip()[:30],
                    'class': row.get('class_code', '').strip(),
                })

        for i, row in enumerate(sample_rows):
            print(f"{i+1}: '{row['parcel_id']}' | {row['owner']} | {row['address']} | Class: {row['class']}")

    except Exception as e:
        print(f"Error analyzing parcels: {e}")

if __name__ == "__main__":
    analyze_nhdra_keys()
    analyze_spatial_keys()
    analyze_parcel_keys()
    print("\n=== ANALYSIS COMPLETE ===")
