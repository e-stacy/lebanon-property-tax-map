# Lebanon Property Tax Database II

## Overview

This is a property tax database and data explorer for Lebanon, New Hampshire. The project provides a comprehensive system for processing, normalizing, and visualizing property assessment data from the city. It includes normalized CSV datasets for parcels, buildings, land, sales, and NHDRA data, along with a web-based data explorer interface that displays property information in both tabular and map formats. The system follows a "Clerk mode" approach that prioritizes evidence-based processing and maintains clear data provenance throughout the transformation pipeline.

## Current Status (September 2025)

**✅ COMPLETED - Mobile-Friendly Hierarchical Checkbox Filters**
- ✅ **FUNCTIONALITY**: Mobile-friendly checkbox filter system with hierarchical structure
- ✅ **HIERARCHY**: Primary classes (bold) with indented subclasses (1010 → 1012, etc.)
- ✅ **MOBILE SUPPORT**: Touch-friendly checkboxes work without Ctrl+click requirement
- ✅ **CONSISTENT**: Identical behavior on both index.html and map.html pages
- ✅ **VISUAL DESIGN**: Clear parent-child relationships with styling and indentation

**✅ COMPLETED - Interactive Column Resizing**
- ✅ **RESIZE HANDLES**: Blue hover indicators on column borders with cursor change
- ✅ **DRAG FUNCTIONALITY**: Smooth column width adjustment with 80px-400px constraints
- ✅ **RESET BUTTON**: One-click restoration to default 140px column widths
- ✅ **USER EXPERIENCE**: Session-only storage, no persistence required
- ✅ **PRACTICAL**: Addresses wide table navigation by allowing custom column sizing

**✅ COMPLETED - Heating System Hierarchical Filter**
- ✅ **ENVIRONMENTAL FOCUS**: 3-tier hierarchy organized by environmental impact (Solar → Wood → Gas → Electric → Oil → Coal)
- ✅ **COMPREHENSIVE DATA**: 4,805 properties with complete heating information across 8 fuel types and 15+ heating types
- ✅ **HIERARCHICAL STRUCTURE**: All Methods → Heating Fuel → Heating Type combinations
- ✅ **TREE HUGGER FRIENDLY**: Prioritizes renewable fuels (Solar, Wood) and efficient systems (Forced H/W, Radiant)
- ✅ **DUAL INTERFACE**: Consistent behavior across both data table and interactive map views
- ✅ **SMART FILTERING**: Handles fuel-type combinations with parent-child checkbox relationships

**✅ COMPLETED - Zoning District Hierarchical Filter**
- ✅ **COMPREHENSIVE STRUCTURE**: Three-tier hierarchy with Residential (1,380), Commercial (252), and Industrial (182) categories
- ✅ **COMPLETE COVERAGE**: All major Lebanon, NH zoning districts included (R1-R3, RL1-RL3, RO variants, commercial CBD/GC/NC/PBD/MC, industrial INDL/INDH/INDR)
- ✅ **HIERARCHICAL BEHAVIOR**: Parent selection auto-checks children, child deselection unchecks parents
- ✅ **DUAL INTERFACE**: Identical functionality on both index.html (data table) and map.html (interactive map)
- ✅ **VISUAL HIERARCHY**: 4-tier indentation with proper styling for clear structure display

**NEW FILES ENHANCED THIS SESSION:**
- `working-checkbox-filters.js` - Added comprehensive heating system filter with environmental prioritization and zoning filter with 4-tier hierarchy
- Updated `index.html` and `map.html` to include both heating and zoning filters in controls and filtering logic
- Enhanced `working-checkbox-styles.css` with improved 4-tier indentation styling

**FILTER SYSTEM STATUS**: Complete four-filter system deployed
1. ✅ Property Class (hierarchical residential/commercial/exempt/etc.)
2. ✅ Year Built (decade groupings with unknown handling)  
3. ✅ Zoning District (land use hierarchy: residential/commercial/industrial)
4. ✅ Heating System (environmental hierarchy: fuel types and heating methods)

**✅ COMPLETED - 4-Card Statistics Dashboard**  
- ✅ **CARD LAYOUT**: Converted from table format to 4 individual cards for improved readability
- ✅ **STANDARDIZED LABELS**: Consistent "Selected [Category]" format across all middle rows
- ✅ **CLEAN DESIGN**: Uniform font sizing, no colors, description on left, values on right
- ✅ **OPTIMIZED CATEGORIES**: Parcels, Assessed Value, Median Age, Land Area with percentage tracking
- ✅ **ENVIRONMENTAL ANALYSIS READY**: Perfect for heating system impact studies and property filtering
- ✅ **RESPONSIVE GRID**: Cards automatically adjust to screen size for mobile compatibility

**✅ COMPLETED - Enhanced Database Integration**
- Successfully integrated comprehensive NHDRA data from city_data into main parcels dataset
- Expanded from 12 to 25 columns with detailed property information
- Enhanced website interfaces (index.html and map.html) to display new data
- Fixed color overlay system and statistics display on page load
- Repository structure organized and ready for GitHub deployment

**✅ COMPLETED - GitHub Pages Deployment**
- ✅ Enhanced database successfully deployed to GitHub Pages
- ✅ Site live at: https://e-stacy.github.io/lebanon-property-tax-map/
- ✅ Automatic deployment workflow configured for future updates
- ✅ Comprehensive README created for Right-to-Know law support

**STATUS NOTE**: Lebanon Property Tax Database is now publicly accessible with comprehensive NHDRA integration (5,660 properties, 71 columns). Enhanced dataset includes all current city parcels with comprehensive NHDRA detail data where available (5,611 enhanced, 49 city-only). Data table interface with 4-card statistics dashboard and hierarchical filtering is complete. Next phase: implement similar statistics system for map interface.

**✅ COMPLETED - Hierarchical Checkbox Functionality**
- ✅ Touch-friendly checkboxes work without Ctrl+click requirement  
- ✅ Hierarchical behavior: parent selection auto-checks children, child deselection unchecks parent
- ✅ Consistent behavior across both index.html and map.html pages
- ✅ Proper visual hierarchy with 50px subclass indentation
- ✅ Fully functional filtering with accurate property counts

**❌ REMAINING ISSUE - Text Alignment on Index Page Only**
- **Problem**: Dropdown button text "All Classes" appears centered instead of left-aligned on index page
- **Scope**: Issue is specific to index.html only - map.html works correctly
- **Root Cause**: Parent container CSS on index page (.control-row with flex layout) overrides text alignment
- **Impact**: Cosmetic only - all functionality works perfectly

**ATTEMPTED SOLUTIONS (All Failed)**:
1. CSS specificity overrides with !important declarations
2. Inline styles in JavaScript template  
3. Absolute positioning approach
4. Parent container targeting (.controls .control-row)
5. JavaScript force-styling with setProperty('important')

**✅ COMPLETED - 4-Card Statistics System Implementation**
- ✅ **DATA TABLE INTERFACE**: Fully functional 4-card statistics dashboard on index.html
- ✅ **CARD STRUCTURE**: Each card shows percentage, selected value, and total value with clear labels
- ✅ **STANDARDIZED DESCRIPTIONS**: "Selected Parcels %", "Selected Value %", "Ratio of Selected Age", "Selected Land Area %"
- ✅ **UNIFORM STYLING**: Consistent font sizes, no color coding, clean label-value separation
- ✅ **RESPONSIVE DESIGN**: Cards adapt to screen size for optimal mobile experience

**✅ COMPLETED - Ultra-Compact Layout Optimization (September 2025)**
- ✅ **HEADER LAYOUT**: Fixed overlapping elements - moved subtitle box below map button with proper spacing
- ✅ **LEGAL PROTECTION**: Added prominent disclaimer in header for liability protection and data verification requirements
- ✅ **MAXIMUM SPACE OPTIMIZATION**: Achieved ultra-compact design through aggressive padding/margin reduction:
  - Filter controls: 0.75em fonts, 6px padding, 2px margins, line-height: 1
  - Table display: 0.7em fonts, 4px cell padding, 35px header height, line-height: 1.1
  - Footer ultra-minimal: 0px padding, 24px fixed height, no shadows
- ✅ **8-ROW PAGINATION**: Limited table to 8 rows per page for optimal screen fit
- ✅ **FOOTER OPTIMIZATION**: Data export section expanded with no-wrap, matching button sizes

**FILES MODIFIED THIS SESSION**:
- `index.html` - Comprehensive layout optimization for maximum screen real estate
- `working-checkbox-styles.css` - Ultra-compact filter styling with reduced fonts and spacing
- Enhanced mobile responsiveness with ultra-tight spacing throughout

**✅ COMPLETE - LAYOUT & MAP INTERFACE OPTIMIZATION (September 2025)**: 
Lebanon Property Info Repository achieved **absolute maximum screen efficiency** with zero wasted vertical space on data interface and **fully functional map filtering system**. Layout: Perfect 9-row data display with footer fully visible. Map Interface: All four filter types (Property Class, Year Built, Zoning District, Heating System) properly update statistics and map display. Eliminated "na" label values through improved data validation. Both interfaces optimized for 5,660 property records with professional appearance maintained.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The project uses a file-based architecture with multiple processing stages and output formats:

**Data Processing Pipeline**: Two-stage normalization process that transforms raw city data into standardized formats. Stage A converts source columns to snake_case while preserving provenance, and Stage B maps to canonical schema for public consumption. All transformations are driven by mapping tables stored in CSV format.

**Directory Structure**: Canonical layout separating concerns - raw data in timestamped folders under `data/raw/`, immutable originals in `data/originals/`, normalized outputs in `outputs/normalized_csvs/`, and web assets in `docs/site/`. Evidence logs and alignment reports stored in `outputs/alignment_report/`.

**Web Interface**: Static site served from `docs/site/` with dual hosting support - GitHub Pages for public access and local Node.js/Express server for development. JavaScript-based data explorer loads CSV files via fetch API and renders interactive tables with filtering and summary statistics.

**Data Joining Strategy**: Uses Map-Block-Lot (MBL) keys rather than simple parcel IDs for accurate data relationships, as this matches the city's actual property identification system.

**Evidence Management**: SHA-256 manifesting system tracks all file changes with timestamped inventory reports. PowerShell-based tooling for intake, quality control, and evidence logging maintains audit trail.

**Schema Design**: Five normalized tables (parcels, buildings, land, sales, nhdra) with standardized column naming. Header normalization handled client-side to accommodate variations in source data while maintaining consistent UI expectations.

## External Dependencies

**Frontend Libraries**: Leaflet for mapping functionality, PapaParse for CSV processing, Express.js for local development server

**Development Tools**: Node.js runtime with npm package management, PowerShell for Windows-based scripting and data processing workflows

**Hosting Platform**: GitHub Pages for static site deployment, GitHub repository for version control and collaboration

**Data Sources**: City of Lebanon property assessment files, NHDRA (New Hampshire Department of Revenue Administration) data, property sales records, and spatial data (shapefiles/GeoJSON)

**Processing Requirements**: Python for normalization scripts, Windows environment for PowerShell-based tooling, UTF-8 text encoding throughout pipeline