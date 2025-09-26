#!/usr/bin/env python3
"""
Fix Column Reference Issues in HTML Files

This script documents the common issue that occurs after data structure changes:
JavaScript code still references old column names after CSV headers are standardized.

PROBLEM:
When parcels.csv headers are changed from jargon to plain text (e.g., 'parcel_id' → 'Parcel ID'),
the JavaScript in index.html and map.html must be updated to use bracket notation for column names with spaces.

SOLUTION:
Replace dot notation with bracket notation for column names containing spaces:
- property.parcel_id → property['Parcel ID']
- parcel.class_code → parcel['Property Class Code']

COMMON COLUMN NAME CHANGES:
- parcel_id → Parcel ID
- class_code → Property Class Code
- nhdra_vns ayb → Year Built
- nhdra_lnd zone → Zoning Code
- nhdra_vns heat type desc → Heating Type
- nhdra_vns heat fuel desc → Heating Fuel
- situs_address → Situs Address
- owner_name → Owner Name
- total_value → Total Value
- lot_size_acres → Lot Size (Acres)

RUN THIS SCRIPT:
python scripts/fix_column_references.py

This will automatically fix the most common column reference issues.
"""

import re

def fix_column_references():
    """Apply the standard fixes for column reference issues"""

    # Column mapping: old → new
    column_mapping = {
        'parcel_id': 'Parcel ID',
        'class_code': 'Property Class Code',
        'nhdra_vns ayb': 'Year Built',
        'nhdra_lnd zone': 'Zoning Code',
        'nhdra_vns heat type desc': 'Heating Type',
        'nhdra_vns heat fuel desc': 'Heating Fuel',
        'situs_address': 'Situs Address',
        'owner_name': 'Owner Name',
        'total_value': 'Total Value',
        'lot_size_acres': 'Lot Size (Acres)',
        'nhdra_zoning_code': 'Zoning Code',
        'nhdra_heating_fuel': 'Heating Fuel',
        'nhdra_vns style desc': 'Building Style'
    }

    files_to_fix = ['index.html', 'map.html']

    for filename in files_to_fix:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Fix dot notation references
            for old_col, new_col in column_mapping.items():
                # Pattern: object.old_column
                pattern = r'(\w+)\.' + re.escape(old_col) + r'\b'
                replacement = r'\1[\'' + new_col + '\']'
                content = re.sub(pattern, replacement, content)

            # Fix optional chaining with spaces (property?.Property Class Code)
            for old_col, new_col in column_mapping.items():
                if ' ' in new_col:  # Only for columns with spaces
                    # Pattern: object?.old_column
                    pattern = r'(\w+)\?\.' + re.escape(old_col) + r'\b'
                    replacement = r'\1 && \1[\'' + new_col + '\']'
                    content = re.sub(pattern, replacement, content)

            if content != original_content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed column references in {filename}")
            else:
                print(f"ℹ️  No changes needed in {filename}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

if __name__ == "__main__":
    print("🔧 Fixing column reference issues in HTML files...")
    fix_column_references()
    print("✅ Column reference fixes complete!")
    print("\n📝 Remember to test index.html and map.html locally after fixes.")
