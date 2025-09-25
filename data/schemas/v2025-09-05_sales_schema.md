# v2025-09-05/sales.csv Schema Analysis

## File Information
- **File Path**: data/city_data/versions/v2025-09-05/sales.csv
- **Row Count**: 4 rows
- **Data Version**: v2025-09-05

## Column Schema

| Column Name | Data Type | Sample Values | Notes |
|-------------|-----------|---------------|-------|
| parcel_id | string | PID-001, PID-002, PID-003 | Parcel identifier (anonymized format) |
| sale_price | integer | 360000, 330000, 700000 | Sale price in dollars |
| sale_date | date | 9/15/2024, 6/1/2024, 12/10/2024 | Sale date (MM/DD/YYYY format) |
| arms_length | integer | 1, 1, 1 | Arms-length indicator (1=yes, likely 0=no) |

## Sample Rows (All rows)

```csv
parcel_id,sale_price,sale_date,arms_length
PID-001,360000,9/15/2024,1
PID-002,330000,6/1/2024,1
PID-003,700000,12/10/2024,1
```

## Key Observations
- **Small sample dataset**: Only 3 actual data rows
- **Anonymized parcel IDs**: Uses PID-XXX format instead of actual parcel identifiers
- **Clean data format**: Consistent date format and numeric values
- **Limited scope**: Only recent sales data (2024 dates)
- **Quality indicator**: arms_length field suggests data quality filtering

