# Lebanon Property Tax Database - Comprehensive Public Records Project

## Project Overview

The Lebanon Property Tax Database is a **public transparency initiative** that provides citizens with comprehensive access to property assessment data for Lebanon, New Hampshire. This project serves the fundamental democratic principle of government transparency by making public records easily searchable and accessible to taxpayers, researchers, and civic organizations.

**Live Database**: https://e-stacy.github.io/lebanon-property-tax-map/  
**Repository**: https://github.com/e-stacy/lebanon-property-tax-map

## Public Interest & Legal Foundation

### Transparency Mission
This project directly serves **New Hampshire's Right-to-Know Law (RSA 91-A)**, which declares that "the public's right of access to governmental proceedings and records shall not be unreasonably restricted." Property tax records are quintessentially public documents that citizens have an absolute right to access.

### Civic Benefits
- **Tax Equity Analysis**: Enables citizens to verify fair and equitable property assessments
- **Market Research**: Provides real estate professionals and citizens with comprehensive market data
- **Government Accountability**: Allows oversight of municipal assessment practices
- **Academic Research**: Supports housing policy research and urban planning studies
- **Economic Development**: Provides developers and businesses with transparent market information

## Current Data Integration Status

### Successfully Integrated Sources ✅
- **Primary Assessment Data**: 5,622 properties with basic valuation information
- **NHDRA Records**: New Hampshire Department of Revenue Administration data including:
  - Building characteristics (style, grade, construction year)
  - Detailed specifications (living area, rooms, bathrooms) 
  - Infrastructure details (heating systems, roofing, exterior materials)
  - Assessment history and condition ratings
- **Zoning Information**: Current zoning classifications for land use analysis
- **Sales History**: Transaction records for market value verification

### Current Dataset Scope
**25 data fields per property** including:
- Parcel identification and ownership
- Land and building valuations
- Physical characteristics (5,000+ sqft of living area data)
- Construction details (year built, architectural style, building grade)
- Infrastructure specifications (heating, roofing, exterior materials)
- Sales history with transaction dates and prices

## Technical Architecture & Data Quality

### Professional Standards
- **Evidence-Based Processing**: SHA-256 file integrity verification
- **Audit Trail**: Complete provenance tracking for all data transformations
- **Standardized Schema**: Normalized database design following GIS best practices
- **Open Source**: Fully transparent methodology available for public inspection
- **Format Compliance**: Industry-standard CSV, GeoJSON, and web formats

### Data Processing Pipeline
The system implements a **two-stage normalization process** that transforms raw municipal data into standardized, publicly accessible formats:

**Stage A - Source Normalization**:
- Converts source columns to snake_case while preserving data provenance  
- Maintains immutable originals in timestamped folders (`data/raw/`)
- All transformations driven by mapping tables stored in CSV format

**Stage B - Canonical Schema Mapping**: 
- Maps normalized data to standardized public schema
- Cross-reference validation between multiple data sources (NHDRA, parcels, sales)
- Automated quality control and error detection

**Evidence Management**:
- SHA-256 file integrity verification for all data transformations
- Complete audit trail with timestamped inventory reports
- PowerShell-based tooling for intake, quality control, and evidence logging

## System Architecture

### Directory Structure & Data Organization
```
lebanon-property-tax-map/
├── data/
│   ├── parcels.csv                    # Current integrated dataset (5,622 properties)
│   └── city_data/
│       ├── versions/
│       │   ├── v2025-09-06/          # Historical data versions
│       │   │   ├── nhdra.csv         # NHDRA building characteristics  
│       │   │   ├── parcels.csv       # Basic assessment data
│       │   │   ├── buildings.csv     # Building details
│       │   │   ├── land.csv          # Land records
│       │   │   └── sales.csv         # Transaction history
│       │   └── v2025-09-05/          # Previous version
│       └── spatial/raw/               # Original shapefiles
├── spatial/
│   ├── parcels_wgs84.geojson         # Web-optimized spatial data
│   └── parcels.geojson               # Original coordinate system
├── index.html                        # Main data explorer interface
├── map.html                          # Interactive mapping interface  
└── sitemap.xml                       # Search engine data discovery
```

### Web Interface Architecture

**Dual-Mode Design Philosophy**:
The system demonstrates **transparent data access** while maintaining usable interfaces:

1. **Interactive JavaScript Interface**: Rich user experience with filtering, search, and visualization
2. **Direct Data Access**: Raw CSV/GeoJSON files accessible to search engines and AI agents
3. **Progressive Enhancement**: Core data always accessible, JavaScript enhances experience

**Frontend Technology Stack**:
- **Leaflet.js**: Interactive mapping with property overlays and popup details
- **PapaParse**: Client-side CSV processing for large datasets  
- **Vanilla JavaScript**: No framework dependencies for maximum compatibility
- **Static Site**: GitHub Pages hosting for reliability and transparency

**Data Loading Strategy**:
- Asynchronous CSV fetch from `/data/parcels.csv` (911KB for 5,622 properties)
- Client-side parsing and filtering for responsive user experience
- Efficient pagination and search without server dependencies

### Database Design & Integration Strategy

**Multi-Source Data Integration**:
The system successfully integrates multiple municipal data sources using **Map-Block-Lot (MBL) identifiers** rather than simple parcel IDs, matching the city's actual property identification system.

**Normalized Schema Design**:
- **25 standardized columns** across integrated dataset
- **Five logical tables**: parcels, buildings, land, sales, nhdra  
- **Header normalization**: Client-side handling accommodates source data variations
- **Type validation**: Automatic data type detection and conversion

**Key Integration Achievement**:
Successfully merged NHDRA dataset (70 original columns) with existing parcels data, expanding from 12 to 25 fields while maintaining data integrity and establishing clear provenance chains.

### Search Engine & AI Agent Accessibility

**Transparency-First Design**:
This project demonstrates how to balance rich user interfaces with open data principles:

**Direct Data Discovery**:
- **Comprehensive sitemap** (`sitemap.xml`) lists all data files for search engines
- **Robots.txt** explicitly encourages crawling of data directories  
- **Prominent access links** on main page point directly to CSV and GeoJSON files
- **SEO optimization** with descriptive meta tags and canonical URLs

**Data Format Standards**:
- **CSV files**: UTF-8 encoding, standardized column naming, proper escaping
- **GeoJSON**: Web Mercator (WGS84) projection for maximum compatibility
- **Semantic HTML**: Accessible table structures with proper headings
- **API-ready**: Direct file access supports programmatic data consumption

## Outstanding Data Requests

### Critical Missing Elements
To fulfill the project's transparency mission, several categories of public records remain needed:

#### 1. **Complete Historical Assessment Data**
- Multi-year assessment records for trend analysis
- Previous valuations to track assessment changes over time
- Historical exemption and abatement records

#### 2. **Enhanced Building Records**
- Detailed building permit history
- Property improvement records
- Code compliance and inspection data
- Variance and zoning decision history

#### 3. **Comprehensive Sales Documentation**
- Complete deed transfer records
- Sales validation documentation
- Market adjustment factors used in assessments

#### 4. **Assessment Methodology Documentation**
- Current assessment practices and procedures
- Comparable sales analysis data
- Assessment appeals and outcomes

### Legal Basis for Additional Data Requests

**RSA 91-A** explicitly states that all government records are presumptively public unless specifically exempted. Property assessment records, building permits, and sales data fall squarely within the scope of records that must be made available to the public.

**Case Law Support**:
- *Mans v. Lebanon School Board* establishes broad interpretation of public records
- *Telegraph Publishing Co. v. Hillsborough County* confirms citizens' right to electronic formats
- *Goode v. N.H. Office of Legislative Budget Assistant* supports requests for database formats

## Technical Specifications for Additional Data

### Preferred Data Formats
- **CSV files** with UTF-8 encoding for tabular data
- **GeoJSON or Shapefile** format for spatial data
- **JSON or XML** for structured metadata
- **Standard relational database exports** (SQL dumps acceptable)

### Required Data Elements
- **Unique identifiers** that link across datasets (Map-Block-Lot preferred)
- **Temporal data** with precise dates for historical analysis
- **Categorical data** with consistent coding schemes
- **Geospatial references** where applicable

### Integration Capabilities
The existing system can process and integrate:
- Multi-table relational data with foreign key relationships
- Time-series data for historical trend analysis  
- Spatial data for geographic visualization
- Large datasets (currently processing 5,600+ records efficiently)

## Evidence of Public Use & Impact

### Current Public Access
- **Web Interface**: Real-time property lookup and comparison tools
- **Interactive Mapping**: Geographic visualization of assessment patterns
- **Statistical Analysis**: Automated calculation of market trends and assessment ratios
- **Export Capabilities**: Citizen access to underlying data for independent analysis

### Demonstrated Public Interest
- Professional real estate and legal community use
- Academic research applications
- Citizen advocacy and civic engagement
- Government accountability and oversight activities

## Compliance History & Good Faith

### Professional Approach
This project has consistently:
- Followed proper legal channels for data acquisition
- Maintained professional correspondence with municipal offices
- Demonstrated technical competence in data handling
- Shown respect for privacy considerations while pursuing public transparency

### Open Source Commitment
All code, methodologies, and processing workflows are published under open-source licenses, ensuring:
- Complete transparency in data handling practices
- Public ability to verify data accuracy and methodology
- Reproducible research supporting civic engagement
- Contribution to the broader civic technology community

## Contact & Legal Framework

This project operates under **New Hampshire Right-to-Know Law (RSA 91-A)** and supports the state's commitment to "open government and the public's right to know." All requests are made in good faith to advance legitimate public interests in government transparency and civic engagement.

For questions about data processing methods, technical specifications, or integration requirements, please refer to the project documentation at the repository listed above.

## Current Features & Functionality

### **Advanced 4-Filter Hierarchical System**
- **Property Class Filter**: 4-tier hierarchy covering residential, commercial, exempt, and agricultural properties
- **Year Built Filter**: Decade-based groupings (1800s-2020s) with comprehensive age analysis
- **Zoning District Filter**: Complete Lebanon zoning coverage (R1-R3, RL1-RL3, CBD, GC, NC, PBD, MC, Industrial)
- **Heating System Filter**: Environmental hierarchy prioritizing renewables (Solar → Wood → Gas → Electric → Oil → Coal)
- **Touch-Friendly**: Mobile-optimized interface works without Ctrl+click requirement

### **Dual Interface System**
- **Data Table Interface**: Ultra-compact layout with 9-row display and interactive column resizing
- **Interactive Map**: Leaflet-based visualization with parcel boundaries and property overlays
- **Statistics Dashboard**: 4-card percentage-based system with real-time filter updates
- **Consistent Experience**: Identical filtering behavior across both interfaces

### **Professional User Experience**
- **Maximum Screen Efficiency**: Aggressive layout optimization for data density
- **Interactive Elements**: Column resizing, filter statistics, map layer controls
- **Data Export**: CSV, GeoJSON, and sitemap generation capabilities
- **Mobile Responsive**: Optimized for desktop, tablet, and mobile viewing

---

*This README serves as supporting documentation for Right-to-Know requests and demonstrates the legitimate public interest, technical capability, and professional standards that underpin this public transparency initiative.*