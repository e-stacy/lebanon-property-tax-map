#!/usr/bin/env python3
"""
Manual Building Footprints Download for Lebanon, NH

Since the Microsoft Azure blob storage has access restrictions,
this script provides instructions and alternative approaches.
"""

def main():
    print("🏗️  Microsoft Building Footprints - Lebanon, NH")
    print("=" * 50)
    print()
    print("📋 MANUAL DOWNLOAD REQUIRED")
    print("The Microsoft Azure storage has access restrictions.")
    print()
    print("🔗 Download New Hampshire building data from:")
    print("https://github.com/Microsoft/USBuildingFootprints")
    print()
    print("📁 Look for files like:")
    print("   - NewHampshire.geojson")
    print("   - NewHampshire.geojson.gz")
    print("   - Or state-by-state downloads")
    print()
    print("💾 Save the downloaded file as:")
    print("   data/raw/buildings/nh-buildings-raw.geojson")
    print("   (or .geojson.gz if compressed)")
    print()
    print("🚀 Then run this script again to process:")
    print("   python scripts/download_buildings_manual.py --process")
    print()

def process_existing_data():
    """Process already downloaded NH building data"""

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
        return (bounds['west'] <= lon <= bounds['east'] and
                bounds['south'] <= lat <= bounds['north'])

    print("🔍 Looking for downloaded building data...")

    data_file = None
    if Path("../data/raw/buildings/nh-buildings-raw.geojson.gz").exists():
        data_file = "../data/raw/buildings/nh-buildings-raw.geojson.gz"
        print("📁 Found compressed file")
    elif Path("../data/raw/buildings/nh-buildings-raw.geojson").exists():
        data_file = "../data/raw/buildings/nh-buildings-raw.geojson"
        print("📁 Found uncompressed file")
    else:
        print("❌ No building data file found!")
        print("Please download from Microsoft first.")
        return False

    print("📥 Processing and filtering to Lebanon...")

    try:
        # Load the data
        if data_file.endswith('.gz'):
            with gzip.open(data_file, 'rt', encoding='utf-8') as f:
                data = json.load(f)
        else:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

        lebanon_features = []
        total_buildings = len(data['features'])
        lebanon_count = 0

        print(f"🔍 Processing {total_buildings} buildings in New Hampshire...")

        for i, feature in enumerate(data['features']):
            if i % 50000 == 0 and i > 0:
                print(".1f")

            try:
                # Simple bounding box check
                if feature['geometry']['type'] == 'Polygon':
                    coords = feature['geometry']['coordinates'][0]
                    # Check if building intersects Lebanon bounds
                    in_lebanon = False
                    for coord in coords[:20]:  # Check more points for accuracy
                        if point_in_bounds(coord[0], coord[1], LEBANON_BOUNDS):
                            in_lebanon = True
                            break

                    if in_lebanon:
                        lebanon_features.append(feature)
                        lebanon_count += 1

            except Exception as e:
                continue

        # Create filtered GeoJSON
        lebanon_data = {
            "type": "FeatureCollection",
            "features": lebanon_features
        }

        # Save processed versions
        output_file = "../data/processed/buildings_lebanon.geojson"
        with open(output_file, "w") as f:
            json.dump(lebanon_data, f, separators=(',', ':'))  # Compact

        # Compressed version
        with gzip.open("../data/processed/buildings_lebanon.geojson.gz", "wt") as f:
            json.dump(lebanon_data, f, separators=(',', ':'))

        # File sizes
        uncompressed_size = Path(output_file).stat().st_size
        compressed_size = Path("../data/processed/buildings_lebanon.geojson.gz").stat().st_size

        print("\n✅ Success!")
        print(f"🏙️  Found {lebanon_count} buildings in Lebanon area")
        print(f"📁 Saved to: data/processed/buildings_lebanon.geojson")
        print(f"📏 File size: {uncompressed_size:,} bytes")
        print(".1f")

        print("\n🗺️  To add to map.html, insert:")
        print("""
        // Add building footprints layer
        const buildingLayer = L.geoJSON('../data/processed/buildings_lebanon.geojson', {
            style: {
                color: '#666',
                weight: 1,
                fillColor: '#ccc',
                fillOpacity: 0.3
            }
        }).addTo(map);
        """)

        return True

    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return False

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--process':
        process_existing_data()
    else:
        main()
