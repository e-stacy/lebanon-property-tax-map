#!/usr/bin/env python3
"""
Script to merge NHDRA comprehensive data with the current parcels.csv file
"""

import pandas as pd
import numpy as np

def load_and_process_files():
    """Load both CSV files and process them for merging"""
    
    # Load current parcels.csv
    print("Loading current parcels.csv...")
    parcels_df = pd.read_csv('data/parcels.csv')
    print(f"Loaded {len(parcels_df)} parcels from current file")
    
    # Load NHDRA comprehensive data
    print("Loading NHDRA comprehensive data...")
    nhdra_df = pd.read_csv('data/city_data/versions/v2025-09-06/nhdra.csv', header=1)  # Skip first row with "Unnamed" headers
    print(f"Loaded {len(nhdra_df)} records from NHDRA file")
    
    return parcels_df, nhdra_df

def map_records(parcels_df, nhdra_df):
    """Map records between the two files using multiple matching strategies"""
    
    # Create mapping keys for both datasets
    print("Creating mapping keys...")
    
    # For parcels.csv, use owner name and total value as key
    parcels_df['map_key'] = parcels_df['owner_name'].str.strip().str.upper() + '_' + parcels_df['total_value'].astype(str)
    
    # For NHDRA, use owner name and total assessment as key  
    nhdra_df['map_key'] = nhdra_df['own name'].str.strip().str.upper() + '_' + nhdra_df['prc ttl assess'].astype(str)
    
    # Try to match on owner name + total value first
    print("Mapping records by owner name and total value...")
    merged_df = parcels_df.merge(nhdra_df, on='map_key', how='left', suffixes=('', '_nhdra'))
    
    # Count successful matches
    matched = merged_df['own name'].notna().sum()
    print(f"Successfully matched {matched} out of {len(parcels_df)} records ({matched/len(parcels_df)*100:.1f}%)")
    
    return merged_df

def add_useful_columns(merged_df):
    """Add the most useful columns from NHDRA to enhance the parcels data"""
    
    print("Adding useful columns from NHDRA data...")
    
    # Building characteristics
    merged_df['year_built'] = merged_df['vns ayb'].fillna('')
    merged_df['building_style'] = merged_df['vns style desc'].fillna('')
    merged_df['building_grade'] = merged_df['vns grade desc'].fillna('')
    merged_df['living_area_sqft'] = merged_df['cns area living'].fillna(0)
    
    # Room information
    merged_df['total_rooms'] = merged_df['vns tot rooms'].fillna(0)
    merged_df['bedrooms'] = merged_df['vns num bedrm'].fillna(0)
    merged_df['full_baths'] = merged_df['vns num baths'].fillna(0)
    merged_df['half_baths'] = merged_df['vns num hbaths'].fillna(0)
    
    # Construction details
    merged_df['heating_type'] = merged_df['vns heat type desc'].fillna('')
    merged_df['heating_fuel'] = merged_df['vns heat fuel desc'].fillna('')
    merged_df['ac_type'] = merged_df['vns ac type desc'].fillna('')
    merged_df['roof_material'] = merged_df['vns roof cover desc'].fillna('')
    merged_df['exterior_walls'] = merged_df['vns ext wall1 desc'].fillna('')
    merged_df['stories'] = merged_df['vns stories'].fillna('')
    
    # Sale information
    merged_df['last_sale_price'] = merged_df['saleprice'].fillna(0)
    merged_df['last_sale_date'] = merged_df['saledate'].fillna('')
    
    # Zoning and condition
    merged_df['zoning'] = merged_df['lnd zone'].fillna('')
    merged_df['condition_percent'] = merged_df['cns pct good'].fillna('')
    
    return merged_df

def create_enhanced_parcels_csv(merged_df):
    """Create the enhanced parcels.csv with additional columns"""
    
    print("Creating enhanced parcels.csv...")
    
    # Select the columns we want in the final file
    enhanced_columns = [
        'parcel_id', 'owner_name', 'class_code', 'lot_size_acres',
        'land_value', 'building_value', 'total_value',
        'year_built', 'building_style', 'building_grade', 'living_area_sqft',
        'total_rooms', 'bedrooms', 'full_baths', 'half_baths',
        'heating_type', 'heating_fuel', 'ac_type', 'roof_material', 'exterior_walls', 'stories',
        'zoning', 'last_sale_price', 'last_sale_date', 'condition_percent'
    ]
    
    # Create the enhanced dataframe
    enhanced_df = merged_df[enhanced_columns].copy()
    
    # Clean up data types
    enhanced_df['year_built'] = pd.to_numeric(enhanced_df['year_built'], errors='coerce')
    enhanced_df['living_area_sqft'] = pd.to_numeric(enhanced_df['living_area_sqft'], errors='coerce')
    enhanced_df['total_rooms'] = pd.to_numeric(enhanced_df['total_rooms'], errors='coerce')
    enhanced_df['bedrooms'] = pd.to_numeric(enhanced_df['bedrooms'], errors='coerce')
    enhanced_df['full_baths'] = pd.to_numeric(enhanced_df['full_baths'], errors='coerce')
    enhanced_df['half_baths'] = pd.to_numeric(enhanced_df['half_baths'], errors='coerce')
    enhanced_df['last_sale_price'] = pd.to_numeric(enhanced_df['last_sale_price'], errors='coerce')
    enhanced_df['condition_percent'] = pd.to_numeric(enhanced_df['condition_percent'], errors='coerce')
    
    return enhanced_df

def main():
    """Main function to merge and enhance parcels data"""
    
    # Load the files
    parcels_df, nhdra_df = load_and_process_files()
    
    # Map records between files
    merged_df = map_records(parcels_df, nhdra_df)
    
    # Add useful columns
    enhanced_df = add_useful_columns(merged_df)
    
    # Create enhanced parcels.csv
    final_df = create_enhanced_parcels_csv(enhanced_df)
    
    # Save the enhanced file
    output_file = 'data/parcels_enhanced.csv'
    final_df.to_csv(output_file, index=False)
    print(f"Enhanced parcels data saved to {output_file}")
    print(f"Final dataset has {len(final_df)} records with {len(final_df.columns)} columns")
    
    # Show sample of the enhanced data
    print("\nSample of enhanced data:")
    print(final_df.head(3).to_string())
    
    # Show column summary
    print(f"\nColumns added from NHDRA:")
    new_columns = ['year_built', 'building_style', 'building_grade', 'living_area_sqft',
                   'total_rooms', 'bedrooms', 'full_baths', 'half_baths',
                   'heating_type', 'heating_fuel', 'ac_type', 'roof_material', 
                   'exterior_walls', 'stories', 'zoning', 'last_sale_price', 
                   'last_sale_date', 'condition_percent']
    for col in new_columns:
        non_empty = final_df[col].notna().sum() if col in final_df.columns else 0
        print(f"  {col}: {non_empty}/{len(final_df)} records have data")

if __name__ == "__main__":
    main()