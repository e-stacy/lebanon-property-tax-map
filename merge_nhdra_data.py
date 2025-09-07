#!/usr/bin/env python3

import csv
import pandas as pd
import sys
import os

def load_nhdra_data():
    """Load NHDRA data with proper header handling"""
    nhdra_path = 'city_data/versions/v2025-09-06/nhdra.csv'
    
    # Read the file with headers in the second row
    df = pd.read_csv(nhdra_path, skiprows=1)  # Skip first row with "Unnamed:" columns
    
    print(f"Loaded NHDRA data: {len(df)} records, {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)[:10]}...")  # Show first 10 columns
    
    return df

def map_nhdra_to_parcels(nhdra_df):
    """Map NHDRA columns to more user-friendly names and select key fields"""
    
    # Create Map-Block-Lot identifier from components
    nhdra_df['parcel_id'] = (
        nhdra_df['rem mblu map'].astype(str) + '-' + 
        nhdra_df['rem mblu block'].astype(str) + '-' + 
        nhdra_df['rem mblu lot'].astype(str)
    )
    
    # Clean up parcel_id formatting (remove extra spaces, handle NaN, remove trailing dashes)
    nhdra_df['parcel_id'] = (nhdra_df['parcel_id']
                            .str.replace(' ', '')
                            .str.replace('nan', '')
                            .str.replace('-$', '', regex=True)  # Remove trailing dash
                            .str.replace('--', '-', regex=True)  # Remove double dashes
                            )
    
    # Map to standardized column names (excluding address data per user request)
    column_mapping = {
        'parcel_id': 'parcel_id',
        'own name': 'owner_name', 
        'rem use code': 'class_code',
        'prc ttl lnd area acres': 'lot_size_acres',
        'prc ttl assess lnd': 'land_value',
        'prc ttl assess bldg': 'building_value', 
        'prc ttl assess': 'total_value',
        'vns ayb': 'year_built',
        'vns style desc': 'building_style',
        'vns grade desc': 'building_grade',
        'cns area living': 'living_area_sqft',
        'vns tot rooms': 'total_rooms',
        'vns num bedrm': 'bedrooms',
        'vns num baths': 'full_baths',
        'vns num hbaths': 'half_baths',
        'vns heat type desc': 'heating_type',
        'vns heat fuel desc': 'heating_fuel',
        'vns ac type desc': 'ac_type',
        'vns roof cover desc': 'roof_material',
        'vns ext wall1 desc': 'exterior_walls',
        'vns stories': 'stories',
        'lnd zone': 'zoning',
        'saleprice': 'last_sale_price',
        'saledate': 'last_sale_date',
        'cns pct good': 'condition_percent'
    }
    
    # Select and rename columns
    expanded_df = pd.DataFrame()
    for nhdra_col, new_col in column_mapping.items():
        if nhdra_col in nhdra_df.columns:
            expanded_df[new_col] = nhdra_df[nhdra_col]
        else:
            print(f"Warning: Column '{nhdra_col}' not found in NHDRA data")
            expanded_df[new_col] = None
    
    # Clean and format data
    # Convert numeric columns
    numeric_cols = ['lot_size_acres', 'land_value', 'building_value', 'total_value', 
                   'year_built', 'living_area_sqft', 'total_rooms', 'bedrooms', 
                   'full_baths', 'half_baths', 'stories', 'last_sale_price', 'condition_percent']
    
    for col in numeric_cols:
        if col in expanded_df.columns:
            expanded_df[col] = pd.to_numeric(expanded_df[col], errors='coerce')
    
    # Format monetary values as integers
    for col in ['land_value', 'building_value', 'total_value', 'last_sale_price']:
        if col in expanded_df.columns:
            expanded_df[col] = expanded_df[col].fillna(0).astype(int)
    
    # Clean text fields
    text_cols = ['owner_name', 'building_style', 'building_grade', 'heating_type', 
                'heating_fuel', 'ac_type', 'roof_material', 'exterior_walls', 'zoning']
    
    for col in text_cols:
        if col in expanded_df.columns:
            expanded_df[col] = expanded_df[col].astype(str).str.strip().replace('nan', '')
    
    # Format class_code as string to preserve leading zeros
    if 'class_code' in expanded_df.columns:
        expanded_df['class_code'] = expanded_df['class_code'].astype(str).str.zfill(4)
    
    print(f"Mapped to {len(expanded_df)} records with {len(expanded_df.columns)} columns")
    
    return expanded_df

def save_expanded_parcels(expanded_df):
    """Save the expanded dataset as the new parcels.csv"""
    
    # Remove rows where parcel_id is invalid
    expanded_df = expanded_df[expanded_df['parcel_id'].notna()]
    expanded_df = expanded_df[expanded_df['parcel_id'] != '']
    expanded_df = expanded_df[~expanded_df['parcel_id'].str.contains('nan')]
    
    print(f"Final dataset: {len(expanded_df)} valid parcels")
    print(f"Sample parcel IDs: {list(expanded_df['parcel_id'].head())}")
    
    # Save to data/parcels.csv
    expanded_df.to_csv('data/parcels.csv', index=False)
    print("Saved expanded parcels.csv with NHDRA data")
    
    # Show summary of key new columns
    print("\nSample of expanded data:")
    sample_cols = ['parcel_id', 'owner_name', 'total_value', 'year_built', 'living_area_sqft', 'bedrooms']
    if all(col in expanded_df.columns for col in sample_cols):
        print(expanded_df[sample_cols].head().to_string())

def main():
    """Main processing function"""
    try:
        print("Loading and processing NHDRA data...")
        nhdra_df = load_nhdra_data()
        
        print("Mapping NHDRA columns to parcels format...")
        expanded_df = map_nhdra_to_parcels(nhdra_df)
        
        print("Saving expanded parcels dataset...")
        save_expanded_parcels(expanded_df)
        
        print("✅ Successfully created expanded parcels.csv with NHDRA data!")
        
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()