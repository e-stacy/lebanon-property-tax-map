# v2025-09-05/land.csv Schema Analysis

## File Information
- **File Path**: data/city_data/versions/v2025-09-05/land.csv
- **Row Count**: 7,741+ rows (estimated)
- **Data Version**: v2025-09-05

## Column Schema

| Column Name | Data Type | Sample Values | Notes |
|-------------|-----------|---------------|-------|
| parcel_id | string | 1-1, 1-2, 1-3-100 | Primary key linking to parcels |
| lnd_street_frontage | string | , , | Street frontage (mostly empty) |
| lnd_depth | string | , , | Property depth (mostly empty) |
| lnd_site_index | string | , , | Site index (mostly empty) |
| lnd_pricing_code | string | , , | Pricing code (mostly empty) |
| lnd_assess_val | decimal | 4300.00, 159600.00, 4100.00 | Land assessment value |
| lnd_line_num | integer | 2, 1, 2 | Line number for land component |
| lnd_bldg_num | integer | 1, 1, 1 | Building number |
| lnd_occ_desc | string | ONE FAM, RES LAND, OPEN SPACE | Land occupancy description |
| lnd_occ_code | string | , , | Occupancy code (mostly empty) |
| lnd_type | string | , , | Land type (mostly empty) |

## Sample Rows (First 10)

```csv
parcel_id,lnd_street_frontage,lnd_depth,lnd_site_index,lnd_pricing_code,lnd_assess_val,lnd_line_num,lnd_bldg_num,lnd_occ_desc,lnd_occ_code,lnd_type
1-1,,,,,4300.00,2,1,ONE FAM,,
1-1,,,,,159600.00,1,1,ONE FAM,,
1-2,,,,,4100.00,2,1,ONE FAM,,
1-2,,,,,144000.00,1,1,ONE FAM,,
1-3-100,,,,,2200.00,2,1,ONE FAM,,
1-3-100,,,,,159600.00,1,1,ONE FAM,,
1-3-200,,,,,16600.00,2,1,ONE FAM,,
1-3-200,,,,,159600.00,1,1,ONE FAM,,
1-6,,,,,15700.00,2,1,ONE FAM,,
1-6,,,,,255400.00,1,1,ONE FAM,,
```

## Key Observations
- **Sparse data**: Most columns are empty or null
- **Multi-row per parcel**: Multiple land components per parcel_id
- **Assessment breakdown**: Shows how land value is calculated per component
- **Linkage table**: parcel_id should match parcels table
- **Data quality**: Many missing values in descriptive fields

