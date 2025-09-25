#!/usr/bin/env python3
"""
Fix property class issues identified in data quality review.

This script corrects property classification errors in the parcels data.
"""

import csv
import os
from pathlib import Path

def fix_property_classes():
    """Fix property class mappings for specific parcels."""

    # Define the corrections needed
    corrections = {
        '24-1': {
            'old_class': '1120',  # Resort
            'new_class': '1050',  # Multi-Family 5+ Units
            'reason': 'Parcel is a new apartment complex (2023), not a resort'
        }
    }

    # File paths
    input_file = Path('data/processed/parcels.csv')
    output_file = Path('data/processed/parcels_corrected.csv')
    backup_file = Path('data/processed/parcels_backup.csv')

    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return False

    print("🏗️  Property Class Corrections")
    print("=" * 50)

    # Create backup
    print(f"📋 Creating backup: {backup_file}")
    import shutil
    shutil.copy2(input_file, backup_file)

    corrections_made = 0

    # Process the CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Process header
        header = next(reader)
        writer.writerow(header)

        # Find parcel_id column index
        parcel_id_idx = header.index('parcel_id')
        class_idx = header.index('class_code')

        # Process each row
        for row in reader:
            parcel_id = row[parcel_id_idx]
            current_class = row[class_idx]

            if parcel_id in corrections:
                correction = corrections[parcel_id]
                expected_old = correction['old_class']

                if current_class == expected_old:
                    # Apply the correction
                    row[class_idx] = correction['new_class']
                    corrections_made += 1
                    print(f"✅ Fixed {parcel_id}: {expected_old} → {correction['new_class']} ({correction['reason']})")
                else:
                    print(f"⚠️  Warning: {parcel_id} has class {current_class}, expected {expected_old}")

            writer.writerow(row)

    # Replace original file
    if corrections_made > 0:
        print(f"\n🔄 Replacing original file with {corrections_made} corrections")
        shutil.move(output_file, input_file)
        print("✅ Property classes updated successfully!")
    else:
        print("\n❌ No corrections were applied")
        os.remove(output_file)

    return corrections_made > 0

def investigate_parcel_108_14():
    """Investigate the parcel 108-14 subdivision issue."""

    input_file = Path('data/processed/parcels.csv')

    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return

    print("\n🔍 Investigating Parcel 108-14")
    print("=" * 40)

    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            if row['parcel_id'] == '108-14':
                print(f"📍 Parcel ID: {row['parcel_id']}")
                print(f"🏠 Address: {row['situs_address']}")
                print(f"🏷️  Class: {row['class_code']} (Authority/Commission)")
                print(f"📐 Land Area: {row['lot_size_acres']} acres")
                print(f"🏗️  Style: {row['nhdra_vns style desc']}")
                print(f"💰 Total Value: ${float(row['total_value'] or 0):,.0f}")
                print(f"📅 Year Built: {row['nhdra_vns ayb']}")
                print(f"🏢 Owner: {row['owner_name']}")
                print(f"📧 Owner Address: {row['mailing_address']}, {row['mailing_city']}, {row['mailing_state']} {row['mailing_zip']}")

                # Look for similar parcels in the area (108-*)
                print(f"\n🔎 Checking for related parcels (108-*)...")
                break

    # Look for other 108-* parcels
    related_parcels = []
    # Reopen file for second pass
    with open(input_file, 'r', newline='', encoding='utf-8') as infile2:
        reader2 = csv.DictReader(infile2)

        for row in reader2:
            if row['parcel_id'].startswith('108-') and row['parcel_id'] != '108-14':
                related_parcels.append({
                    'id': row['parcel_id'],
                    'class': row['class_code'],
                    'acres': row['lot_size_acres'],
                    'style': row['nhdra_vns style desc']
                })

    if related_parcels:
        print(f"📋 Found {len(related_parcels)} related parcels:")
        for parcel in related_parcels[:10]:  # Show first 10
            print(f"   {parcel['id']}: Class {parcel['class']}, {parcel['acres']} acres, {parcel['style']}")
        if len(related_parcels) > 10:
            print(f"   ... and {len(related_parcels) - 10} more")
    else:
        print("📋 No other 108-* parcels found")

def main():
    print("🔧 Property Data Quality Corrections")
    print("=" * 50)

    # Fix the property classes
    success = fix_property_classes()

    # Investigate the subdivision issue
    investigate_parcel_108_14()

    if success:
        print("\n🎯 Next Steps:")
        print("1. Test the corrected data in index.html and map.html")
        print("2. Verify parcel 24-1 now shows as Multi-Family instead of Resort")
        print("3. For parcel 108-14, this may require manual subdivision data from the city")

if __name__ == '__main__':
    main()
