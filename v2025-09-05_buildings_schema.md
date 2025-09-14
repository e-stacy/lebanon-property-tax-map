# v2025-09-05/buildings.csv Schema Analysis

## File Information
- **File Path**: data/city_data/versions/v2025-09-05/buildings.csv
- **Row Count**: 5,947+ rows (estimated)
- **Data Version**: v2025-09-05

## Column Schema

| Column Name | Data Type | Sample Values | Notes |
|-------------|-----------|---------------|-------|
| parcel_id | string | 1-1, 1-2, 1-3-100 | Primary key linking to parcels |
| vns_bldg_style | string | , , | Building style (mostly empty) |
| vns_bldg_use | string | , , | Building use (mostly empty) |
| vns_gla | string | , , | Gross living area (mostly empty) |
| vns_bldg_area_effective | integer | 2632, 3043, 2266 | Effective building area |
| vns_pct_good | decimal | 79, 86, 83 | Percent good condition |
| cns_assess_val | integer | 283100, 467700, 359600 | Building assessed value |
| bld_year_built | string | , , | Year built (mostly empty) |
| bld_effective_year_built | string | , , | Effective year built (mostly empty) |
| bld_grade | string | , , | Building grade (mostly empty) |
| bld_condition | string | , , | Building condition (mostly empty) |
| bld_units | string | , , | Number of units (mostly empty) |

## Sample Rows (First 10)

```csv
parcel_id,vns_bldg_style,vns_bldg_use,vns_gla,vns_bldg_area_effective,vns_pct_good,cns_assess_val,bld_year_built,bld_effective_year_built,bld_grade,bld_condition,bld_units
1-1,,,,2632,79,283100,,,,,
1-2,,,,3043,86,467700,,,,,
1-3-100,,,,2266,83,359600,,,,,
1-3-200,,,,5242,91,964300,,,,,
1-6,,,,3227,89,616700,,,,,
1-7,,,,3037,88,397200,,,,,
1-8,,,,3943,79,372500,,,,,
1-9,,,,3040,90,634800,,,,,
1-10,,,,2496,90,353900,,,,,
1-11,,,,0,,0,,,,,
```

## Key Observations
- **Sparse data**: Most descriptive columns are empty
- **Assessment focus**: Primarily contains assessment values and condition percentages
- **Linkage table**: parcel_id should match parcels table
- **Data quality**: Significant missing data in building characteristic fields
- **Zero values**: Some parcels have zero building area and value (likely land-only parcels)

