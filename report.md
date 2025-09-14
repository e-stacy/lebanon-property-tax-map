# Lebanon Property Tax Data Quality Analysis Report

## Executive Summary

This report analyzes the property tax data files in the `/data` folder, identifying data quality issues, inconsistencies, and recommendations for data cleaning and normalization. The analysis covers 8 CSV files with varying schemas and data quality levels.

## Data Files Overview

| File | Rows | Columns | Primary Issues |
|------|------|---------|----------------|
| `parcels.csv` | 5,637+ | 74 | Mixed sources, inconsistent naming, null values |
| `column_mapping_reference.csv` | 41 | 15 | Metadata/reference file (good quality) |
| `v2025-09-05/parcels.csv` | 5,637+ | 12 | Clean but simplified version |
| `v2025-09-05/nhdra.csv` | 5,600+ | 70 | Unusual structure, many empty fields |
| `v2025-09-05/land.csv` | 7,741+ | 11 | Sparse data, multi-row per parcel |
| `v2025-09-05/buildings.csv` | 5,947+ | 12 | Sparse descriptive data |
| `v2025-09-05/sales.csv` | 4 | 4 | Sample data only |
| `NHDRA/SalesList_combined.csv` | 1,477+ | 29 | Complex headers, comprehensive data |

## Critical Data Quality Issues

### 1. Schema Inconsistencies

**Problem**: Multiple versions of the same data with different structures
- Main `parcels.csv`: 74 columns with NHDRA integration
- Versioned `parcels.csv`: 12 columns, simplified
- Versioned `nhdra.csv`: 70 columns with unusual header structure

**Impact**: Difficult to determine which version is authoritative

**Recommendation**: Establish single source of truth and deprecate redundant versions

### 2. Column Naming Inconsistencies

**Problem**: Inconsistent naming conventions
- Spaces in column names: `nhdra_rem prcl locn street`
- Mixed prefixes: some columns have `nhdra_` prefix, others don't
- Multi-word headers with embedded newlines in sales data

**Impact**: Difficult to reference columns programmatically

**Recommendation**: Standardize to snake_case: `nhdra_street_location`, `sale_date`

### 3. Missing Data Patterns

**Problem**: Significant missing data across multiple files
- `land.csv`: 7 out of 11 columns mostly empty
- `buildings.csv`: Most descriptive fields empty
- `nhdra.csv`: Many building characteristic fields empty for non-residential parcels

**Impact**: Incomplete property profiles

**Recommendation**: Implement missing data imputation strategies or clearly document data limitations

### 4. Data Type Inconsistencies

**Problem**: Inconsistent data types for same concepts
- Dates: Mix of `MM/DD/YYYY`, `YYYY-MM-DD HH:MM:SS`, and `1900-01-01` for nulls
- Parcel IDs: Some use `1-1` format, others use `PID-XXX` anonymized format
- Numbers: Mix of integers and decimals for same fields

**Impact**: Type conversion errors and analysis complications

**Recommendation**: Standardize date formats and numeric types

### 5. Linkage Issues

**Problem**: Potential linkage problems between related tables
- `parcel_id` as primary key across tables
- Multi-row relationships (land.csv has multiple rows per parcel)
- Version mismatches between parcel tables

**Impact**: Difficulty joining related data

**Recommendation**: Validate foreign key relationships and handle one-to-many relationships properly

### 6. Duplicate Data Risks

**Problem**: Potential duplicates across versions
- Same parcels appear in multiple version folders
- NHDRA data duplicated between main parcels.csv and separate nhdra.csv

**Impact**: Inflated counts and analysis errors

**Recommendation**: Implement deduplication logic with clear precedence rules

### 7. Privacy and Data Sensitivity

**Problem**: Address data mixed with assessment data
- Owner names and addresses in assessment files
- Mailing addresses exposed in non-aggregated data

**Impact**: Privacy concerns for public data sharing

**Recommendation**: Separate PII from assessment data or implement aggregation rules

## Data Quality Assessment by Category

### Completeness: MODERATE
- Core assessment data (values, parcel IDs) is complete
- Building characteristics have significant gaps
- Geographic data is well-populated

### Accuracy: HIGH
- Assessment values appear consistent
- Sale data includes verification ratios
- Geographic identifiers are standardized

### Consistency: LOW
- Multiple schemas for same entities
- Inconsistent naming conventions
- Mixed data type representations

### Timeliness: HIGH
- Recent data versions (2025)
- Multi-year sales history available
- Regular update versioning

## Recommended Data Architecture

### Unified Schema Proposal

```sql
-- Proposed unified parcels table
CREATE TABLE parcels (
    parcel_id VARCHAR PRIMARY KEY,
    situs_address VARCHAR,
    owner_name VARCHAR,
    mailing_address VARCHAR,
    mailing_city VARCHAR,
    mailing_state CHAR(2),
    mailing_zip VARCHAR,
    class_code VARCHAR,
    lot_size_acres DECIMAL(10,6),
    land_value INTEGER,
    building_value INTEGER,
    total_value INTEGER,
    year_built INTEGER,
    living_area_sqft INTEGER,
    bedrooms INTEGER,
    bathrooms DECIMAL(3,1),
    property_type VARCHAR,
    zoning_code VARCHAR,
    neighborhood_code VARCHAR,
    last_sale_date DATE,
    last_sale_price INTEGER,
    assessment_date DATE
);
```

### Data Processing Pipeline

1. **Extract**: Read from source CSVs with appropriate type handling
2. **Transform**:
   - Standardize column names
   - Handle missing values consistently
   - Normalize data types
   - Validate linkages
3. **Load**: Create clean, unified datasets

## Implementation Recommendations

### Immediate Actions (High Priority)
1. Standardize column naming conventions
2. Implement consistent date handling
3. Validate parcel_id linkages across tables
4. Document data quality limitations

### Medium-term Improvements
1. Create unified data schema
2. Implement automated data validation
3. Add data quality monitoring
4. Establish data update procedures

### Long-term Goals
1. Implement master data management
2. Create data quality dashboard
3. Automate data cleaning pipelines
4. Establish data governance policies

## Conclusion

The property tax data shows good coverage of core assessment information but suffers from structural inconsistencies and missing data in descriptive fields. The presence of multiple versions and schemas suggests evolving data management practices. Implementing the recommended standardization and cleaning procedures will significantly improve data usability and analytical value.

**Priority Level**: HIGH - Data cleaning should be implemented before major analytical work
**Estimated Effort**: 2-3 weeks for initial cleaning pipeline
**Business Impact**: Improved analysis accuracy and reduced data maintenance overhead

