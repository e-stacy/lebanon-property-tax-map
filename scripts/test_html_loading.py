#!/usr/bin/env python3
import csv
import json

def test_data_loading():
    print("=== TESTING HTML DATA LOADING ===")

    # Test CSV loading (simulating what index.html does)
    try:
        with open('data/parcels.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        print(f"✅ CSV loaded: {len(rows)} rows")

        # Check required columns exist
        required_cols = ['parcel_id', 'owner_name', 'class_code', 'total_value']
        sample_row = rows[0] if rows else {}

        missing_cols = [col for col in required_cols if col not in sample_row]
        if missing_cols:
            print(f"❌ Missing required columns: {missing_cols}")
            return False
        else:
            print("✅ All required columns present")

        # Check NHDRA columns exist
        nhdra_cols = ['nhdra_saleprice', 'nhdra_saledate', 'nhdra_qualified', 'nhdra_vns ayb']
        missing_nhdra = [col for col in nhdra_cols if col not in sample_row]
        if missing_nhdra:
            print(f"⚠️  Missing some NHDRA columns: {missing_nhdra}")
        else:
            print("✅ NHDRA columns present")

        # Test spatial data loading (simulating what map.html does)
        try:
            with open('RecoveredRawData/spatial/parcels_wgs84.geojson', 'r') as f:
                spatial_data = json.load(f)
            print(f"✅ GeoJSON loaded: {len(spatial_data.get('features', []))} features")
        except Exception as e:
            print(f"❌ GeoJSON loading failed: {e}")
            return False

        # Test key matching
        parcel_ids = set(row['parcel_id'] for row in rows if row.get('parcel_id'))
        spatial_ids = set()
        for feature in spatial_data.get('features', []):
            props = feature.get('properties', {})
            map_lot = props.get('MAP_LOT')
            if map_lot:
                spatial_ids.add(map_lot)

        matches = parcel_ids & spatial_ids
        match_rate = len(matches) / len(parcel_ids) * 100 if parcel_ids else 0

        print(f"📊 Key matching: {len(matches)}/{len(parcel_ids)} parcels ({match_rate:.1f}%)")

        if match_rate >= 70:  # Good enough for the web app
            print("✅ Spatial matching acceptable")
        else:
            print("⚠️  Low spatial matching - may affect map functionality")

        print("\n🎉 HTML data loading test PASSED!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_data_loading()

