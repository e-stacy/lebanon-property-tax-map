# v2025-09-05/parcels.csv Schema Analysis

## File Information
- **File Path**: data/city_data/versions/v2025-09-05/parcels.csv
- **Row Count**: 5,637+ rows (estimated)
- **Data Version**: v2025-09-05

## Column Schema

| Column Name | Data Type | Sample Values | Notes |
|-------------|-----------|---------------|-------|
| parcel_id | string | 1-1, 1-2, 1-3-100 | Primary key, alphanumeric with dashes |
| situs_address | string | 17 FARAWAY LN, 19 FARAWAY LN | Physical property address |
| owner_name | string | "BEATTY, JOHN J ", "LACA, KRISTINE & HERNAN" | Owner names with quotes |
| mailing_address1 | string | 17 FARAWAY LN, PO BOX 533 | Mailing address line 1 |
| mailing_city | string | WEST LEBANON, HANOVER | Mailing city |
| mailing_state | string | NH | Mailing state (2-letter codes) |
| mailing_zip | string | 03784, 03755 | Mailing ZIP codes |
| class_code | string | 1010, 1300, 9090 | Property classification codes |
| lot_size_acres | decimal | 2.340000, 2.290000, 1.560000 | Lot size in acres (6 decimal places) |
| land_value | integer | 163900, 148100, 161800 | Assessed land value |
| building_value | integer | 283100, 467700, 359600 | Assessed building value |
| total_value | integer | 461900, 628600, 521900 | Total assessed value |

## Sample Rows (First 5)

```csv
parcel_id,situs_address,owner_name,mailing_address1,mailing_city,mailing_state,mailing_zip,class_code,lot_size_acres,land_value,building_value,total_value
1-1,17 FARAWAY LN ,"BEATTY, JOHN J ",17 FARAWAY LN,WEST LEBANON,NH,03784,1010,2.340000,163900,283100,461900
1-2,19 FARAWAY LN ,"LACA, KRISTINE & HERNAN",19 FARAWAY LN,WEST LEBANON,NH,03784,1010,2.290000,148100,467700,628600
1-3-100,23 FARAWAY LN,"LUNTER, M & SABOURIN, H CO-TTEES",23 FARAWAY LN,WEST LEBANON,NH,03784,1010,1.560000,161800,359600,521900
1-3-200,25 FARAWAY LN ,"GALBRAITH, M A & M M TTEES",25 FARAWAY LN,WEST LEBANON,NH,03784,1010,6.200000,176200,964300,1140500
1-6,31 FARAWAY LN ,"SOX JR, H C & C H TTEES",31 FARAWAY LN,WEST LEBANON,NH,03784,1010,6.590000,271100,616700,902300
```

## Key Observations
- **Simplified version**: Only 12 columns compared to main parcels.csv (74 columns)
- **Clean data format**: Consistent formatting without NHDRA data integration
- **High precision decimals**: lot_size_acres has 6 decimal places
- **Same core fields**: Contains the essential parcel identification and assessment data
- **No NHDRA integration**: Missing the extensive NHDRA property characteristic data

