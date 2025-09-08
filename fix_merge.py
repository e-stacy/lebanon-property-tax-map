#!/usr/bin/env python3
"""
Fix the merge duplication issue and create a clean enhanced parcels.csv
"""

import pandas as pd

def fix_enhanced_parcels():
    """Clean up the enhanced parcels data and remove duplicates"""
    
    print("Loading enhanced parcels data...")
    enhanced_df = pd.read_csv('data/parcels_enhanced.csv')
    print(f"Loaded {len(enhanced_df)} records from enhanced file")
    
    # Remove duplicates based on parcel_id, keeping the first occurrence
    print("Removing duplicates...")
    clean_df = enhanced_df.drop_duplicates(subset=['parcel_id'], keep='first')
    print(f"After removing duplicates: {len(clean_df)} records")
    
    # Save the clean version
    clean_df.to_csv('data/parcels_enhanced_clean.csv', index=False)
    print("Clean enhanced data saved to data/parcels_enhanced_clean.csv")
    
    # Replace the original parcels.csv with the enhanced version
    print("Replacing original parcels.csv with enhanced version...")
    clean_df.to_csv('data/parcels.csv', index=False)
    print("Original parcels.csv updated with enhanced data!")
    
    print(f"\nFinal dataset: {len(clean_df)} records with {len(clean_df.columns)} columns")
    print("\nSample of final enhanced data:")
    print(clean_df[['parcel_id', 'owner_name', 'total_value', 'year_built', 'building_style', 'living_area_sqft', 'bedrooms', 'full_baths']].head(3).to_string())
    
    return clean_df

if __name__ == "__main__":
    clean_df = fix_enhanced_parcels()