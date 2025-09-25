# column_mapping_template.csv Schema Analysis

## File Information
- **File Path**: data/column_mapping_template.csv
- **File Size**: 388B
- **Row Count**: 2 lines

## Column Schema

| Column Name | Data Type | Sample Values | Notes |
|-------------|-----------|---------------|-------|
| Source | string | [NEW_SOURCE] | Placeholder for data source |
| Raw_File_Name | string | [FILE_NAME] | Placeholder for filename |
| Source_Column_Header | string | [ORIGINAL_HEADER] | Placeholder for original column |
| Mapped_Display_Header | string | [CLEAN_HEADER] | Placeholder for clean header |
| Data_Type | string | [TYPE] | Placeholder for data type |
| Field_Category | string | [CATEGORY] | Placeholder for category |
| Processing_Notes | string | [PROCESSING] | Placeholder for processing notes |
| Description | string | [DESCRIPTION] | Placeholder for description |
| Required | string | [Y/N] | Placeholder for required flag |
| Last_Updated | date | [DATE] | Placeholder for update date |
| Validation_Rules | string | [RULES] | Placeholder for validation rules |
| Source_Contact | string | [CONTACT] | Placeholder for contact info |
| Import_Priority | string | [HIGH/MED/LOW] | Placeholder for priority |
| Business_Rules | string | [RULES] | Placeholder for business rules |
| Legacy_Mappings | string | [OLD_NAMES] | Placeholder for legacy names |

## Sample Rows (All rows)

```csv
Source,Raw_File_Name,Source_Column_Header,Mapped_Display_Header,Data_Type,Field_Category,Processing_Notes,Description,Required,Last_Updated,Validation_Rules,Source_Contact,Import_Priority,Business_Rules,Legacy_Mappings
[NEW_SOURCE],[FILE_NAME],[ORIGINAL_HEADER],[CLEAN_HEADER],[TYPE],[CATEGORY],[PROCESSING],[DESCRIPTION],[Y/N],[DATE],[RULES],[CONTACT],[HIGH/MED/LOW],[RULES],[OLD_NAMES]
```

## Key Observations
- **Template file**: Contains placeholder values for creating new mapping entries
- **Single data row**: Only one template row with bracketed placeholders
- **Reference structure**: Mirrors the column_mapping_reference.csv structure
- **Documentation purpose**: Used as a template for adding new field mappings

