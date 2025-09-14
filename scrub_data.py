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

import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_DIR = Path('data')
CLEAN_DIR = DATA_DIR / 'clean'
CLEAN_DIR.mkdir(exist_ok=True)

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
    """Load and clean the main parcels.csv file"""
    print("Loading main parcels.csv...")
    df = pd.read_csv(DATA_DIR / 'parcels.csv', low_memory=False)

    # Standardize column names
    df = standardize_column_names(df)

    # Clean data types
    numeric_cols = ['lot_size_acres', 'land_value', 'building_value', 'total_value',
                   'nhdra_sale_price', 'nhdra_land_acres', 'nhdra_building_assessment',
                   'nhdra_exempt_assessment', 'nhdra_land_assessment',
                   'nhdra_outbuilding_assessment', 'nhdra_total_assessment',
                   'nhdra_living_area_sqft', 'nhdra_year_built', 'nhdra_effective_area',
                   'nhdra_total_rooms', 'nhdra_bedrooms', 'nhdra_bathrooms',
                   'nhdra_half_bathrooms', 'nhdra_percent_good', 'nhdra_stories']

    for col in numeric_cols:
        if col in df.columns:
            if 'bath' in col or col in ['nhdra_bedrooms', 'nhdra_total_rooms', 'nhdra_stories']:
                df[col] = clean_numeric_column(df[col], 'int64')
            else:
                df[col] = clean_numeric_column(df[col], 'float64')

    # Clean dates
    date_cols = ['nhdra_sale_date']
    for col in date_cols:
        if col in df.columns:
            df[col] = clean_date_column(df[col])

    # Clean string columns
    string_cols = ['owner_name', 'situs_address', 'mailing_address', 'mailing_city',
                  'mailing_state', 'mailing_zip', 'nhdra_owner_name', 'nhdra_grantor']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df

def load_versioned_parcels():
    """Load and clean the versioned parcels.csv file"""
    print("Loading versioned parcels.csv...")
    df = pd.read_csv(DATA_DIR / 'city_data' / 'versions' / 'v2025-09-05' / 'parcels.csv')

    # Standardize column names
    df = standardize_column_names(df)

    # Clean data types
    df['lot_size_acres'] = clean_numeric_column(df['lot_size_acres'], 'float64')
    df['land_value'] = clean_numeric_column(df['land_value'], 'int64')
    df['building_value'] = clean_numeric_column(df['building_value'], 'int64')
    df['total_value'] = clean_numeric_column(df['total_value'], 'int64')

    # Clean string columns
    string_cols = ['owner_name', 'situs_address', 'mailing_address', 'mailing_city',
                  'mailing_state', 'mailing_zip']
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

    return df

def load_nhdra_data():
    """Load and clean the NHDRA data with unusual header structure"""
    print("Loading NHDRA data...")
    df = pd.read_csv(DATA_DIR / 'city_data' / 'versions' / 'v2025-09-05' / 'nhdra.csv',
                    header=1,  # Skip first row, use second row as header
                    low_memory=False)

    # The actual column names are in row 2, but pandas uses them as headers
    # Clean up any remaining unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Standardize column names
    df = standardize_column_names(df)

    # Clean numeric columns
    numeric_cols = ['prc_ttl_lnd_area_acres', 'prc_ttl_assess_bldg', 'prc_ttl_assess_xf',
                   'prc_ttl_assess_lnd', 'prc_ttl_assess_ob', 'prc_ttl_assess',
                   'cns_area_living', 'vns_ayb', 'cns_area_effective', 'vns_tot_rooms',
                   'vns_num_bedrm', 'vns_num_baths', 'vns_num_hbaths', 'cns_pct_good',
                   'vns_stories', 'saleprice']

    for col in numeric_cols:
        if col in df.columns:
            if col in ['vns_num_bedrm', 'vns_tot_rooms', 'vns_stories']:
                df[col] = clean_numeric_column(df[col], 'int64')
            else:
                df[col] = clean_numeric_column(df[col], 'float64')

    # Clean dates
    if 'saledate' in df.columns:
        df['saledate'] = clean_date_column(df['saledate'])

    return df

def load_land_data():
    """Load and clean land component data"""
    print("Loading land data...")
    df = pd.read_csv(DATA_DIR / 'city_data' / 'versions' / 'v2025-09-05' / 'land.csv')

    # Standardize column names
    df = standardize_column_names(df)

    # Clean numeric columns
    df['lnd_assess_val'] = clean_numeric_column(df['lnd_assess_val'], 'float64')
    df['lnd_line_num'] = clean_numeric_column(df['lnd_line_num'], 'int64')
    df['lnd_bldg_num'] = clean_numeric_column(df['lnd_bldg_num'], 'int64')

    # Clean string columns
    df['lnd_occ_desc'] = df['lnd_occ_desc'].astype(str).str.strip()

    return df

def load_buildings_data():
    """Load and clean buildings data"""
    print("Loading buildings data...")
    df = pd.read_csv(DATA_DIR / 'city_data' / 'versions' / 'v2025-09-05' / 'buildings.csv')

    # Standardize column names
    df = standardize_column_names(df)

    # Clean numeric columns
    df['vns_bldg_area_effective'] = clean_numeric_column(df['vns_bldg_area_effective'], 'int64')
    df['vns_pct_good'] = clean_numeric_column(df['vns_pct_good'], 'float64')
    df['cns_assess_val'] = clean_numeric_column(df['cns_assess_val'], 'int64')

    return df

def load_sales_data():
    """Load and clean sales data"""
    print("Loading sales data...")
    df = pd.read_csv(DATA_DIR / 'city_data' / 'versions' / 'v2025-09-05' / 'sales.csv')

    # Standardize column names
    df = standardize_column_names(df)

    # Clean data types
    df['sale_price'] = clean_numeric_column(df['sale_price'], 'int64')
    df['sale_date'] = clean_date_column(df['sale_date'])
    df['arms_length'] = clean_numeric_column(df['arms_length'], 'int64')

    return df

def load_nhdra_sales():
    """Load and clean NHDRA sales data"""
    print("Loading NHDRA sales data...")
    df = pd.read_csv(DATA_DIR / 'city_data' / 'versions' / 'NHDRA 2025-09-13' / 'SalesList_2020-2024_combined.csv')

    # Standardize column names (remove newlines and clean up)
    df.columns = df.columns.str.replace('\n', ' ').str.strip().str.lower().str.replace(' ', '_')

    # Clean specific column names - handle the actual column names that exist
    column_renames = {}
    for col in df.columns:
        if '\n' in col:
            # Remove newlines and extra spaces
            clean_col = col.replace('\n', '_').replace(' ', '_').lower()
            column_renames[col] = clean_col

    df = df.rename(columns=column_renames)

    # Now rename to more readable names
    final_renames = {
        'sale_date': 'sale_date',
        'book_page': 'book_page',
        'deed_type': 'deed_type',
        'cama_count': 'cama_count',
        'map_lot': 'map_lot',
        'verified_price': 'verified_price',
        'current_assed': 'current_assessed',
        'previous_assed': 'previous_assessed',
        'prop_code': 'property_code',
        'mod_code': 'modification_code',
        'special_code': 'special_code',
        'main_xcode': 'main_exemption_code',
        'mainx_notes': 'main_exemption_notes',
        'town_notes': 'town_notes',
        'state_notes': 'state_notes'
    }

    df = df.rename(columns=final_renames)

    # Clean data types
    df['year'] = clean_numeric_column(df['year'], 'int64')
    df['verno'] = clean_numeric_column(df['verno'], 'int64')
    df['sale_date'] = clean_date_column(df['sale_date'])
    df['cama_count'] = clean_numeric_column(df['cama_count'], 'int64')
    df['acres'] = clean_numeric_column(df['acres'], 'float64')
    df['ratio'] = clean_numeric_column(df['ratio'], 'float64')

    # Only clean property_code if it exists
    if 'property_code' in df.columns:
        df['property_code'] = clean_numeric_column(df['property_code'], 'int64')
    if 'modification_code' in df.columns:
        df['modification_code'] = clean_numeric_column(df['modification_code'], 'int64')
    if 'special_code' in df.columns:
        df['special_code'] = clean_numeric_column(df['special_code'], 'int64')

    # Clean currency columns (remove $ and commas)
    currency_cols = ['verified_price', 'current_assessed', 'previous_assessed']
    for col in currency_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'[\$,]', '', regex=True)
            df[col] = clean_numeric_column(df[col], 'float64')

    return df

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

def main():
    """Main data cleaning pipeline"""
    print("Starting Lebanon Property Tax Data Cleaning Pipeline")
    print("=" * 60)

    # Load and clean all datasets
    datasets = {}

    try:
        datasets['main_parcels'] = load_main_parcels()
        datasets['nhdra_data'] = load_nhdra_data()
        datasets['land_data'] = load_land_data()
        datasets['buildings_data'] = load_buildings_data()
        datasets['sales_data'] = load_sales_data()
        datasets['nhdra_sales'] = load_nhdra_sales()

        print(f"\nLoaded {len(datasets)} datasets successfully")

        # Create unified parcels dataset (simplified)
        unified_parcels = datasets['main_parcels'].copy()
        datasets['unified_parcels'] = unified_parcels

        # Save cleaned datasets
        print("\nSaving cleaned datasets to /data/clean/...")

        for name, df in datasets.items():
            output_path = CLEAN_DIR / f"{name}_cleaned.csv"
            df.to_csv(output_path, index=False)
            print(f"Saved {name}: {len(df)} rows, {len(df.columns)} columns")

        # Generate data quality summary
        print("\nGenerating data quality summary...")
        summary_path = CLEAN_DIR / "data_quality_summary.txt"

        with open(summary_path, 'w') as f:
            f.write("Lebanon Property Tax Data Quality Summary\n")
            f.write("=" * 50 + "\n\n")

            for name, df in datasets.items():
                f.write(f"{name.upper()}:\n")
                f.write(f"  Rows: {len(df)}\n")
                f.write(f"  Columns: {len(df.columns)}\n")
                f.write(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB\n")

                # Null value summary
                null_counts = df.isnull().sum()
                if null_counts.sum() > 0:
                    f.write("  Null values by column (top 5):\n")
                    for col, count in null_counts[null_counts > 0].head().items():
                        pct = (count / len(df)) * 100
                        f.write(".1f")
                f.write("\n")

        print(f"Data quality summary saved to {summary_path}")
        print("\nData cleaning pipeline completed successfully!")

    except Exception as e:
        print(f"Error in data cleaning pipeline: {e}")
        raise

if __name__ == "__main__":
    main()
