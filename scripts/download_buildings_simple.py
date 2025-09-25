#!/usr/bin/env python3
"""
Simple Microsoft Building Footprints Downloader for Lebanon, NH

This simplified version downloads and filters without heavy GIS dependencies.
"""

import requests
import json
import gzip
from pathlib import Path

# Lebanon, NH bounding box (approximate)
LEBANON_BOUNDS = {
    'west': -72.35,
    'east': -72.15,
    'south': 43.55,
    'north': 43.75
}

def point_in_bounds(lon, lat, bounds):
    """Check if a point is within Lebanon bounds"""
    return (bounds['west'] <= lon <= bounds['east'] and
            bounds['south'] <= lat <= bounds['north'])

def download_and_filter():
    """Download NH buildings and filter to Lebanon area"""

    url = "https://usbuildingdata.blob.core.windows.net/usbuildings-v2/NewHampshire.geojson"

    print("🏗️  Downloading New Hampshire building footprints...")
    print("This will take several minutes (NH data is ~500MB)")

    try:
        # Download the data
        response = requests.get(url, stream=True)
        response.raise_for_status()

        print("📥 Processing and filtering to Lebanon...")

        # Process as stream to avoid loading everything into memory
        content = ""
        in_features = False
        feature_count = 0
        lebanon_count = 0
        lebanon_features = []

        for line in response.iter_lines(decode_unicode=True):
            if not line.strip():
                continue

            content += line + "\n"

            # Look for start of features array
            if '"features": [' in content and not in_features:
                in_features = True
                # Start collecting from here
                content = '{"type": "FeatureCollection", "features": [\n'

            if in_features:
                if line.strip() == '},' or line.strip() == '}':
                    # End of a feature
                    try:
                        # Try to parse this as a complete feature
                        temp_content = content + ']}'
                        temp_data = json.loads(temp_content)

                        if temp_data['features']:
                            feature = temp_data['features'][0]

                            # Check if building is in Lebanon bounds
                            # Simple bounding box check (not perfect but fast)
                            if feature['geometry']['type'] == 'Polygon':
                                coords = feature['geometry']['coordinates'][0]
                                # Check if any point is in bounds (simple approximation)
                                in_lebanon = False
                                for coord in coords[:10]:  # Check first 10 points
                                    if point_in_bounds(coord[0], coord[1], LEBANON_BOUNDS):
                                        in_lebanon = True
                                        break

                                if in_lebanon:
                                    lebanon_features.append(feature)
                                    lebanon_count += 1

                    except json.JSONDecodeError:
                        pass  # Not a complete feature yet

                    # Reset content for next feature
                    content = '{"type": "FeatureCollection", "features": [\n'

                feature_count += 1
                if feature_count % 50000 == 0:
                    print(".1f")

        # Save filtered results
        lebanon_data = {
            "type": "FeatureCollection",
            "features": lebanon_features
        }

        # Save the filtered data
        with open("data/processed/buildings_lebanon.geojson", "w") as f:
            json.dump(lebanon_data, f, separators=(',', ':'))  # Compact

        # Also save compressed version
        with gzip.open("data/processed/buildings_lebanon.geojson.gz", "wt") as f:
            json.dump(lebanon_data, f, separators=(',', ':'))

        # File sizes
        uncompressed_size = Path("data/processed/buildings_lebanon.geojson").stat().st_size
        compressed_size = Path("data/processed/buildings_lebanon.geojson.gz").stat().st_size

        print("\n✅ Success!")
        print(f"📊 Found {lebanon_count} buildings in Lebanon area")
        print(f"📁 Saved to: data/processed/buildings_lebanon.geojson")
        print(f"🗜️  Compressed: data/processed/buildings_lebanon.geojson.gz")
        print(f"📏 Uncompressed size: {uncompressed_size:,} bytes")
        print(f"📏 Compressed size: {compressed_size:,} bytes")
        print(".1f")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🏗️  Microsoft Building Footprints - Lebanon, NH (Simple Version)")
    print("=" * 60)

    success = download_and_filter()

    if success:
        print("\n🗺️  To add buildings to map.html, insert this code:")
        print("""
        // Add building footprints layer
        const buildingLayer = L.geoJSON('../data/processed/buildings_lebanon.geojson', {
            style: {
                color: '#666',        // Border color
                weight: 1,            // Border width
                fillColor: '#ccc',    // Fill color
                fillOpacity: 0.3      // Transparency
            }
        }).addTo(map);
        """)
