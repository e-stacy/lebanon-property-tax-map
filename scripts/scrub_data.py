#!/usr/bin/env python3
"""
Lebanon Property Tax Data Scrubbing and Cleaning Script

This script loads property tax data from CSV files, applies cleaning and normalization,
and outputs cleaned datasets to /data/clean/ directory.

Issues addressed:
- Column name standardization
- Data type normalization
- Missing value handling
- Date format standardization
- Parcel ID consistency
- Duplicate removal
- Schema unification
"""

import csv
import os
from pathlib import Path
from datetime import datetime

# Configuration
DATA_DIR = Path('data')
CLEAN_DIR = DATA_DIR / 'clean'
DATA_DIR.mkdir(exist_ok=True)
CLEAN_DIR.mkdir(exist_ok=True)

def construct_parcel_id(map_val, block_val, lot_val='', unit_val=''):
    """Construct Map-Block-Lot-Unit parcel ID"""
    parts = []

    # Map - required
    if map_val and str(map_val).strip():
        try:
            parts.append(str(int(float(str(map_val).strip()))))
        except (ValueError, TypeError):
            return ''  # Invalid map means invalid parcel_id

    # Block - required
    if block_val and str(block_val).strip():
        try:
            parts.append(str(int(float(str(block_val).strip()))))
        except (ValueError, TypeError):
            return ''  # Invalid block means invalid parcel_id

    # Lot - optional, only add if numeric
    if lot_val and str(lot_val).strip():
        try:
            parts.append(str(int(float(str(lot_val).strip()))))
        except (ValueError, TypeError):
            pass  # Skip non-numeric lot values

    # Unit - optional, only add if numeric
    if unit_val and str(unit_val).strip():
        try:
            parts.append(str(int(float(str(unit_val).strip()))))
        except (ValueError, TypeError):
            pass  # Skip non-numeric unit values

    return '-'.join(parts) if parts else ''

# Column name mappings for standardization
COLUMN_MAPPINGS = {
    # Parcels columns
    'parcel_id': 'parcel_id',
    'situs_address': 'situs_address',
    'owner_name': 'owner_name',
    'mailing_address1': 'mailing_address',
    'mailing_city': 'mailing_city',
    'mailing_state': 'mailing_state',
    'mailing_zip': 'mailing_zip',
    'class_code': 'class_code',
    'lot_size_acres': 'lot_size_acres',
    'land_value': 'land_value',
    'building_value': 'building_value',
    'total_value': 'total_value',

    # NHDRA columns (standardized)
    'nhdra_rem prcl locn street': 'nhdra_street_location',
    'nhdra_rem prcl locn': 'nhdra_property_location',
    'nhdra_own name': 'nhdra_owner_name',
    'nhdra_co own name': 'nhdra_co_owner_name',
    'nhdra_address1': 'nhdra_mailing_address',
    'nhdra_city': 'nhdra_city',
    'nhdra_state': 'nhdra_state',
    'nhdra_zip': 'nhdra_zip',
    'nhdra_book pg': 'nhdra_book_page',
    'nhdra_saleprice': 'nhdra_sale_price',
    'nhdra_saledate': 'nhdra_sale_date',
    'nhdra_qualified': 'nhdra_qualified_sale',
    'nhdra_grantor': 'nhdra_grantor',
    'nhdra_rem use code': 'nhdra_use_code',
    'nhdra_lnd zone': 'nhdra_zoning_code',
    'nhdra_prc ttl lnd area acres': 'nhdra_land_acres',
    'nhdra_prc ttl assess bldg': 'nhdra_building_assessment',
    'nhdra_prc ttl assess xf': 'nhdra_exempt_assessment',
    'nhdra_prc ttl assess lnd': 'nhdra_land_assessment',
    'nhdra_prc ttl assess ob': 'nhdra_outbuilding_assessment',
    'nhdra_prc ttl assess': 'nhdra_total_assessment',
    'nhdra_cns area living': 'nhdra_living_area_sqft',
    'nhdra_vns ayb': 'nhdra_year_built',
    'nhdra_vns style desc': 'nhdra_building_style',
    'nhdra_rem pid': 'nhdra_property_id',
    'nhdra_vns grade': 'nhdra_grade_code',
    'nhdra_vns grade desc': 'nhdra_grade_description',
    'nhdra_vns roof struct desc': 'nhdra_roof_structure',
    'nhdra_vns roof cover desc': 'nhdra_roof_covering',
    'nhdra_vns int flr1 desc': 'nhdra_floor_covering',
    'nhdra_vns int wall1 desc': 'nhdra_wall_material',
    'nhdra_vns ext wall1 desc': 'nhdra_exterior_wall',
    'nhdra_cns area effective': 'nhdra_effective_area',
    'nhdra_vns tot rooms': 'nhdra_total_rooms',
    'nhdra_vns num bedrm': 'nhdra_bedrooms',
    'nhdra_vns num baths': 'nhdra_bathrooms',
    'nhdra_vns num hbaths': 'nhdra_half_bathrooms',
    'nhdra_vns bathrm style desc': 'nhdra_bathroom_style',
    'nhdra_vns kitchen style desc': 'nhdra_kitchen_style',
    'nhdra_vns heat type desc': 'nhdra_heating_type',
    'nhdra_vns heat fuel desc': 'nhdra_heating_fuel',
    'nhdra_cns pct good': 'nhdra_percent_good',
    'nhdra_cns eyb code': 'nhdra_effective_year_code',
    'nhdra_lnd nbhd': 'nhdra_neighborhood_code',
    'nhdra_vns stories': 'nhdra_stories',
}

def standardize_column_names(df, mappings=None):
    """Standardize column names to snake_case"""
    if mappings is None:
        mappings = COLUMN_MAPPINGS

    df = df.copy()
    df.columns = [mappings.get(col, col.lower().replace(' ', '_').replace('-', '_'))
                  for col in df.columns]
    return df

def clean_date_column(series, date_formats=None):
    """Standardize date formats and handle null dates"""
    if date_formats is None:
        date_formats = ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y', '%Y-%m-%d']

    cleaned = pd.Series([pd.NaT] * len(series), dtype='datetime64[ns]')

    for i, val in enumerate(series):
        if pd.isna(val) or val == '' or str(val).strip() in ['1900-01-01', '1900-01-01 00:00:00']:
            continue

        val_str = str(val).strip()
        for fmt in date_formats:
            try:
                cleaned.iloc[i] = pd.to_datetime(val_str, format=fmt)
                break
            except (ValueError, TypeError):
                continue

    return cleaned

def clean_numeric_column(series, dtype='float64'):
    """Clean numeric columns, handling empty strings and invalid values"""
    cleaned = series.copy()

    # Replace empty strings and non-numeric values with NaN
    cleaned = pd.to_numeric(cleaned, errors='coerce')

    if dtype == 'int64':
        # For integer columns, fill NaN with 0 and convert
        cleaned = cleaned.fillna(0).astype('int64')
    elif dtype == 'float64':
        cleaned = cleaned.astype('float64')

    return cleaned

def load_main_parcels():
    """Load and clean the main parcels.csv file - STUB: Not used in current pipeline"""
    print("⚠️  load_main_parcels() is not used in current pipeline")
    return []

def load_versioned_parcels():
    """Load and clean the versioned parcels.csv file - STUB: Not used in current pipeline"""
    print("⚠️  load_versioned_parcels() is not used in current pipeline")
    return []

def load_nhdra_data():
    """Load and clean the NHDRA data - STUB: Not used in current pipeline"""
    print("⚠️  load_nhdra_data() is not used in current pipeline")
    return []

def load_land_data():
    """Load and clean land component data - STUB: Not used in current pipeline"""
    print("⚠️  load_land_data() is not used in current pipeline")
    return []

def load_buildings_data():
    """Load and clean buildings data - STUB: Not used in current pipeline"""
    print("⚠️  load_buildings_data() is not used in current pipeline")
    return []

def load_sales_data():
    """Load and clean sales data - STUB: Not used in current pipeline"""
    print("⚠️  load_sales_data() is not used in current pipeline")
    return []

def load_nhdra_sales():
    """Load and clean NHDRA sales data - STUB: Not used in current pipeline"""
    print("⚠️  load_nhdra_sales() is not used in current pipeline")
    return []

def create_unified_parcels(main_parcels, versioned_parcels, nhdra_data):
    """Create a unified parcels dataset combining the best of each source"""
    print("Creating unified parcels dataset...")

    # Start with the versioned parcels (cleaner structure)
    unified = versioned_parcels.copy()

    # Add NHDRA data where available - use actual column names from nhdra_data
    available_cols = [col for col in nhdra_data.columns if col != 'rem_pid']
    nhdra_cols_to_add = available_cols[:20]  # Limit to first 20 columns to avoid issues

    # Merge NHDRA data (using rem_pid as parcel_id equivalent)
    if 'rem_pid' in nhdra_data.columns and len(nhdra_cols_to_add) > 0:
        cols_to_select = ['rem_pid'] + nhdra_cols_to_add
        nhdra_merge = nhdra_data[cols_to_select].copy()
        nhdra_merge = nhdra_merge.rename(columns={'rem_pid': 'parcel_id'})

        unified = unified.merge(nhdra_merge, on='parcel_id', how='left')

    # Remove duplicates
    unified = unified.drop_duplicates(subset=['parcel_id'])

    return unified

def clean_numeric_value(value):
    """Clean numeric values, handling empty strings and invalid values"""
    if not value or str(value).strip() in ('', 'nan', 'None'):
        return 0.0
    try:
        return float(str(value).strip().replace(',', '').replace('$', ''))
    except (ValueError, TypeError):
        return 0.0

# Removed duplicate construct_parcel_id function

def load_parcels_data():
    """Load and clean the main parcels.csv file"""
    print("Loading parcels data...")
    parcels_path = Path('RecoveredRawData/RawData/data/Lebanon/parcels.csv')
    if not parcels_path.exists():
        raise FileNotFoundError(f"Parcels data not found at {parcels_path}")

    parcels_data = {}
    with open(parcels_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            parcel_id = row.get('parcel_id', '').strip()
            if parcel_id:
                parcels_data[parcel_id] = {
                    'parcel_id': parcel_id,
                    'situs_address': row.get('situs_address', '').strip(),
                    'owner_name': row.get('owner_name', '').strip(),
                    'mailing_address': row.get('mailing_address1', '').strip(),
                    'mailing_city': row.get('mailing_city', '').strip(),
                    'mailing_state': row.get('mailing_state', '').strip(),
                    'mailing_zip': row.get('mailing_zip', '').strip(),
                    'class_code': row.get('class_code', '').strip(),
                    'lot_size_acres': clean_numeric_value(row.get('lot_size_acres', '')),
                    'land_value': clean_numeric_value(row.get('land_value', '')),
                    'building_value': clean_numeric_value(row.get('building_value', '')),
                    'total_value': clean_numeric_value(row.get('total_value', ''))
                }

    print(f"Loaded {len(parcels_data)} parcel records")
    return parcels_data

def load_nhdra_data():
    """Load and clean the NHDRA data with proper header handling"""
    print("Loading NHDRA data...")
    nhdra_path = Path('RecoveredRawData/RawData/data/Lebanon/nhdra.csv')
    if not nhdra_path.exists():
        raise FileNotFoundError(f"NHDRA data not found at {nhdra_path}")

    nhdra_data = {}
    with open(nhdra_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip first row (Unnamed), use second row as headers
        next(reader)
        headers = next(reader)

        for row in reader:
            if len(row) < len(headers):
                continue

            row_dict = dict(zip(headers, row))

            # Construct parcel_id from Map-Block-Lot-Unit
            map_val = row_dict.get('rem mblu map', '').strip()
            block_val = row_dict.get('rem mblu block', '').strip()
            lot_val = row_dict.get('rem mblu lot', '').strip()
            unit_val = row_dict.get('rem mblu unit', '').strip()

            parcel_id = construct_parcel_id(map_val, block_val, lot_val, unit_val)
            if not parcel_id:
                continue

            nhdra_data[parcel_id] = {
                'nhdra_saleprice': clean_numeric_value(row_dict.get('saleprice', '')),
                'nhdra_saledate': row_dict.get('saledate', '').strip(),
                'nhdra_qualified': row_dict.get('qualified', '').strip(),
                # Historical sales data
                'nhdra_ID1 Prior Sale Price': clean_numeric_value(row_dict.get('ID1 Prior Sale Price', '')),
                'nhdra_ID1 Prior Sale Date': row_dict.get('ID1 Prior Sale Date', '').strip(),
                'nhdra_ID2 Prior Sale Price': clean_numeric_value(row_dict.get('ID2 Prior Sale Price', '')),
                'nhdra_ID2 Prior Sale Date': row_dict.get('ID2 Prior Sale Date', '').strip(),
                'nhdra_ID3 Prior Sale Price': clean_numeric_value(row_dict.get('ID3 Prior Sale Price', '')),
                'nhdra_ID3 Prior Sale Date': row_dict.get('ID3 Prior Sale Date', '').strip(),
                # Assessment history (adjusted/historical values)
                'nhdra_ahd ttl assess bldg': clean_numeric_value(row_dict.get('ahd ttl assess bldg', '')),
                'nhdra_ahd ttl assess lnd': clean_numeric_value(row_dict.get('ahd ttl assess lnd', '')),
                'nhdra_ahd ttl assess xf': clean_numeric_value(row_dict.get('ahd ttl assess xf', '')),
                'nhdra_ahd ttl assess ob': clean_numeric_value(row_dict.get('ahd ttl assess ob', '')),
                'nhdra_ahd ttl assess': clean_numeric_value(row_dict.get('ahd ttl assess', '')),
                'nhdra_vns ayb': clean_numeric_value(row_dict.get('vns ayb', '')),
                'nhdra_vns style desc': row_dict.get('vns style desc', '').strip(),
                'nhdra_cns area living': clean_numeric_value(row_dict.get('cns area living', '')),
                'nhdra_vns num bedrm': clean_numeric_value(row_dict.get('vns num bedrm', '')),
                'nhdra_vns num baths': clean_numeric_value(row_dict.get('vns num baths', '')),
                'nhdra_vns tot rooms': clean_numeric_value(row_dict.get('vns tot rooms', '')),
                'nhdra_vns heat type desc': row_dict.get('vns heat type desc', '').strip(),
                'nhdra_vns heat fuel desc': row_dict.get('vns heat fuel desc', '').strip(),
                'nhdra_lnd zone': row_dict.get('lnd zone', '').strip(),
                'nhdra_rem use code': row_dict.get('rem use code', '').strip(),
                'nhdra_prc ttl lnd area acres': clean_numeric_value(row_dict.get('prc ttl lnd area acres', '')),
                'nhdra_prc ttl assess bldg': clean_numeric_value(row_dict.get('prc ttl assess bldg', '')),
                'nhdra_prc ttl assess lnd': clean_numeric_value(row_dict.get('prc ttl assess lnd', '')),
                'nhdra_prc ttl assess': clean_numeric_value(row_dict.get('prc ttl assess', '')),
                'nhdra_cns pct good': clean_numeric_value(row_dict.get('cns pct good', '')),
                'nhdra_vns grade desc': row_dict.get('vns grade desc', '').strip(),
                'nhdra_vns stories': clean_numeric_value(row_dict.get('vns stories', '')),
                'nhdra_cns area effective': clean_numeric_value(row_dict.get('cns area effective', '')),
                'nhdra_vns roof cover desc': row_dict.get('vns roof cover desc', '').strip(),
                'nhdra_vns grade': clean_numeric_value(row_dict.get('vns grade', '')),
                'nhdra_vns num hbaths': clean_numeric_value(row_dict.get('vns num hbaths', '')),
                'nhdra_cns eyb code': row_dict.get('cns eyb code', '').strip(),
                'nhdra_lnd nbhd': row_dict.get('lnd nbhd', '').strip(),
                'nhdra_prc ttl assess xf': clean_numeric_value(row_dict.get('prc ttl assess xf', '')),
                'nhdra_prc ttl assess ob': clean_numeric_value(row_dict.get('prc ttl assess ob', ''))
            }

    print(f"Loaded {len(nhdra_data)} NHDRA records")
    return nhdra_data

def integrate_datasets():
    """Integrate all datasets into unified property records"""
    print("=== INTEGRATING DATASETS ===")

    # Load base parcels data
    parcels = load_parcels_data()

    # Load NHDRA data
    nhdra = load_nhdra_data()

    # Create enhanced NHDRA lookup that handles key matching variations
    enhanced_nhdra = {}
    for nhdra_id, nhdra_data in nhdra.items():
        # Store with original key
        enhanced_nhdra[nhdra_id] = nhdra_data

        # Also store with simplified keys (remove unit numbers)
        # This handles cases where spatial data has "Map-Block-Unit" but property data only has "Map-Block"
        if nhdra_id.count('-') >= 2:  # Has at least Map-Block-Unit
            parts = nhdra_id.split('-')
            if len(parts) >= 3:
                # Try Map-Block (remove last part)
                simplified = '-'.join(parts[:-1])
                if simplified not in enhanced_nhdra:
                    enhanced_nhdra[simplified] = nhdra_data

    # Integrate NHDRA data into parcels with enhanced matching
    integrated_count = 0
    for parcel_id, parcel_data in parcels.items():
        if parcel_id in enhanced_nhdra:
            parcel_data.update(enhanced_nhdra[parcel_id])
            integrated_count += 1

    print(f"Integrated {integrated_count} parcels with NHDRA data out of {len(parcels)} total parcels")

    # Convert to list for CSV output
    integrated_data = list(parcels.values())

    return integrated_data

def save_csv_data(data, filepath, fieldnames=None):
    """Save list of dictionaries to CSV file"""
    if not data:
        print(f"Warning: No data to save to {filepath}")
        return

    if fieldnames is None:
        fieldnames = list(data[0].keys())

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    """Main data cleaning pipeline"""
    print("Starting Lebanon Property Tax Data Cleaning Pipeline")
    print("=" * 60)

    try:
        # Integrate datasets from source files
        integrated_data = integrate_datasets()

        # Save the integrated dataset to the expected location
        output_path = DATA_DIR / 'parcels.csv'
        save_csv_data(integrated_data, output_path)

        print("\n=== RESULTS ===")
        print(f"✅ Saved integrated parcels.csv: {len(integrated_data)} rows, {len(integrated_data[0]) if integrated_data else 0} columns")

        # Show sample of integrated data
        if integrated_data:
            sample = integrated_data[0]
            print(f"📋 Sample integrated record keys: {list(sample.keys())[:10]}...")
            print(f"📊 Total fields: {len(sample)} (should be 25+ per README)")

        # Verify spatial data matching
        print("\n=== SPATIAL DATA MATCHING ===")
        parcel_ids = set(row['parcel_id'] for row in integrated_data)

        import json
        with open('RecoveredRawData/spatial/parcels_wgs84.geojson', 'r') as f:
            spatial_data = json.load(f)
            spatial_ids = set()
            for feature in spatial_data.get('features', []):
                props = feature.get('properties', {})
                map_lot = props.get('MAP_LOT')
                if map_lot:
                    spatial_ids.add(map_lot)

        matches = parcel_ids & spatial_ids
        print(f"Property parcels: {len(parcel_ids)}")
        print(f"Spatial parcels: {len(spatial_ids)}")
        print(f"Matching parcels: {len(matches)} ({len(matches)/len(parcel_ids)*100:.1f}%)")

        print("\n✅ Data integration completed successfully!")

    except Exception as e:
        print(f"❌ Error in data integration: {e}")
        raise

if __name__ == "__main__":
    main()
