#!/usr/bin/env python3
"""
Download and process Microsoft Building Footprints for Lebanon, NH

Microsoft US Building Footprints: https://github.com/Microsoft/USBuildingFootprints
New Hampshire data: https://usbuildingdata.blob.core.windows.net/usbuildings-v2/NewHampshire.geojson

This script:
1. Downloads NH building footprints
2. Filters to Lebanon area (approximate bounding box)
3. Simplifies geometry for web performance
4. Saves as optimized GeoJSON for mapping
"""

import requests
import json
import gzip
from shapely.geometry import shape, Polygon
from shapely.ops import unary_union
import geopandas as gpd
from pathlib import Path

# Lebanon, NH approximate bounding box (WGS84)
LEBANON_BOUNDS = {
    'west': -72.35,
    'east': -72.15,
    'south': 43.55,
    'north': 43.75
}

def download_nh_buildings():
    """Download New Hampshire building footprints from Microsoft"""
    url = "https://usbuildingdata.blob.core.windows.net/usbuildings-v2/NewHampshire.geojson"

    print("Downloading New Hampshire building footprints...")
    print("This may take a few minutes (NH has ~500MB of building data)")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Save compressed version
        with open("data/raw/buildings/nh-buildings-raw.geojson.gz", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("✅ Downloaded and saved to data/raw/buildings/nh-buildings-raw.geojson.gz")
        return True

    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def extract_lebanon_buildings():
    """Extract only Lebanon buildings from NH dataset"""

    print("Extracting Lebanon buildings...")

    try:
        # Load the compressed GeoJSON
        with gzip.open("data/raw/buildings/nh-buildings-raw.geojson.gz", "rt", encoding="utf-8") as f:
            data = json.load(f)

        # Create bounding box polygon for Lebanon
        bounds_poly = Polygon([
            (LEBANON_BOUNDS['west'], LEBANON_BOUNDS['south']),
            (LEBANON_BOUNDS['east'], LEBANON_BOUNDS['south']),
            (LEBANON_BOUNDS['east'], LEBANON_BOUNDS['north']),
            (LEBANON_BOUNDS['west'], LEBANON_BOUNDS['north'])
        ])

        lebanon_features = []
        total_buildings = len(data['features'])
        lebanon_count = 0

        print(f"Processing {total_buildings} buildings in New Hampshire...")

        for i, feature in enumerate(data['features']):
            if i % 10000 == 0:  # Progress update
                print(".1f")

            try:
                # Check if building intersects Lebanon bounds
                geom = shape(feature['geometry'])
                if geom.intersects(bounds_poly):
                    lebanon_features.append(feature)
                    lebanon_count += 1

            except Exception as e:
                # Skip invalid geometries
                continue

        # Create filtered GeoJSON
        lebanon_data = {
            "type": "FeatureCollection",
            "features": lebanon_features
        }

        # Save uncompressed version for processing
        with open("data/raw/buildings/lebanon-buildings.geojson", "w") as f:
            json.dump(lebanon_data, f)

        print(f"✅ Extracted {lebanon_count} buildings in Lebanon area")
        return True

    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return False

def optimize_for_web():
    """Optimize building footprints for web mapping"""

    print("Optimizing for web performance...")

    try:
        # Load Lebanon buildings
        with open("data/raw/buildings/lebanon-buildings.geojson", "r") as f:
            data = json.load(f)

        # Simplify geometries (reduce precision for smaller file size)
        # This reduces coordinate precision to ~1 meter accuracy
        for feature in data['features']:
            if feature['geometry']['type'] == 'Polygon':
                # Simplify coordinates to 5 decimal places (~1m precision)
                for ring in feature['geometry']['coordinates']:
                    for coord in ring:
                        coord[0] = round(coord[0], 5)  # longitude
                        coord[1] = round(coord[1], 5)  # latitude

        # Save optimized version for web use
        with open("data/processed/buildings_lebanon.geojson", "w") as f:
            json.dump(data, f, separators=(',', ':'))  # Compact JSON

        # Also save compressed version
        with gzip.open("data/processed/buildings_lebanon.geojson.gz", "wt", encoding="utf-8") as f:
            json.dump(data, f, separators=(',', ':'))

        # Get file sizes
        uncompressed_size = Path("data/processed/buildings_lebanon.geojson").stat().st_size
        compressed_size = Path("data/processed/buildings_lebanon.geojson.gz").stat().st_size

        print("✅ Optimized for web mapping"        print(f"   Uncompressed: {uncompressed_size:,} bytes")
        print(f"   Compressed: {compressed_size:,} bytes")
        print(".1f")

        return True

    except Exception as e:
        print(f"❌ Optimization failed: {e}")
        return False

def main():
    """Main workflow"""
    print("🏗️  Microsoft Building Footprints - Lebanon, NH")
    print("=" * 50)

    # Step 1: Download
    if not download_nh_buildings():
        return False

    # Step 2: Extract Lebanon
    if not extract_lebanon_buildings():
        return False

    # Step 3: Optimize for web
    if not optimize_for_web():
        return False

    print("\n🎉 Success! Building footprints ready for mapping")
    print("📁 Files created:")
    print("   data/raw/buildings/nh-buildings-raw.geojson.gz")
    print("   data/raw/buildings/lebanon-buildings.geojson")
    print("   data/processed/buildings_lebanon.geojson")
    print("   data/processed/buildings_lebanon.geojson.gz")

    print("\n🗺️  To use in map.html, add this layer:")
    print("   const buildingLayer = L.geoJSON('data/processed/buildings_lebanon.geojson', {")
    print("       style: { color: '#666', weight: 1, fillColor: '#ccc', fillOpacity: 0.3 }")
    print("   }).addTo(map);")

    return True

if __name__ == "__main__":
    main()
