# column_mapping_reference.csv Schema Analysis

## File Information
- **File Path**: data/column_mapping_reference.csv
- **File Size**: 8.7KB
- **Row Count**: 41 lines

## Column Schema

| Column Name | Data Type | Sample Values | Notes |
|-------------|-----------|---------------|-------|
| Source | string | City of Lebanon, NHDRA | Data source system |
| Raw_File_Name | string | parcels.csv, nhdra.csv | Source filename |
| Source_Column_Header | string | parcel_id, situs_address | Original column name |
| Mapped_Display_Header | string | Parcel ID, Owner | Clean display name |
| Data_Type | string | string, currency, date | Data type classification |
| Field_Category | string | identifier, location, assessment | Functional category |
| Processing_Notes | string | none, excluded_privacy, format_number | Processing instructions |
| Description | string | Unique property identifier | Field description |
| Required | string | yes, no | Whether field is required |
| Last_Updated | date | 2025-09-08 | Last update date |
| Validation_Rules | string | alphanumeric, text, positive_number | Validation constraints |
| Source_Contact | string | City Assessor, NHDRA Data Unit | Contact for source data |
| Import_Priority | string | HIGH, MED, LOW | Import priority level |
| Business_Rules | string | primary_key, display_required | Business logic rules |
| Legacy_Mappings | string | pid\|prop_id\|parcel_number | Alternative field names |

## Sample Rows (First 10)

```csv
Source,Raw_File_Name,Source_Column_Header,Mapped_Display_Header,Data_Type,Field_Category,Processing_Notes,Description,Required,Last_Updated,Validation_Rules,Source_Contact,Import_Priority,Business_Rules,Legacy_Mappings
City of Lebanon,parcels.csv,parcel_id,Parcel ID,string,identifier,none,Unique property identifier,yes,2025-09-08,alphanumeric,City Assessor,HIGH,primary_key,pid|prop_id|parcel_number
City of Lebanon,parcels.csv,situs_address,Situs Address,string,location,excluded_privacy,Physical property address,no,2025-09-08,text,City Assessor,LOW,exclude_from_display,property_address|site_address|physical_address
City of Lebanon,parcels.csv,owner_name,Owner,string,ownership,none,Property owner name,yes,2025-09-08,text,City Assessor,HIGH,display_required,owner|property_owner|taxpayer_name
City of Lebanon,parcels.csv,mailing_address1,Mailing Address,string,ownership,excluded_privacy,Owner mailing address,no,2025-09-08,text,City Assessor,LOW,exclude_from_display,mail_addr|billing_address|correspondence_address
City of Lebanon,parcels.csv,class_code,Property Class,string,assessment,none,Property classification code,yes,2025-09-08,alphanumeric,City Assessor,HIGH,filter_enabled,use_code|property_type|land_use
City of Lebanon,parcels.csv,lot_size_acres,Lot Size (acres),decimal,physical,format_number,Property lot size in acres,no,2025-09-08,positive_number,City Assessor,MED,display_with_units,lot_size|acreage|land_area_acres
City of Lebanon,parcels.csv,land_value,Land Value,currency,assessment,format_currency,Assessed land value,yes,2025-09-08,positive_currency,City Assessor,HIGH,currency_display|statistics_enabled,land_val|assessed_land|land_assessment
City of Lebanon,parcels.csv,building_value,Building Value,currency,assessment,format_currency,Assessed building value,yes,2025-09-08,positive_currency,City Assessor,HIGH,currency_display|statistics_enabled,bldg_val|building_assessment|improvement_value
City of Lebanon,parcels.csv,total_value,Total Value,currency,assessment,format_currency,Total assessed property value,yes,2025-09-08,positive_currency,City Assessor,HIGH,currency_display|statistics_enabled|filter_enabled,total_val|assessed_value|total_assessment
NHDRA,nhdra.csv,nhdra_rem prcl locn street,NHDRA Street,string,location,excluded_privacy,Street address from state records,no,2025-09-08,text,NHDRA Data Unit,LOW,exclude_from_display,location_street|parcel_street|property_street
```

## Key Observations
- **Metadata table**: Contains mapping information for data integration
- **Structured format**: Well-organized with clear field definitions
- **Privacy considerations**: Some fields marked as excluded_privacy
- **Data quality rules**: Includes validation rules and processing notes
- **Source tracking**: Maintains source system and contact information
- **Business rules**: Defines display and processing requirements

