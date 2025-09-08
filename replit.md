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

**✅ COMPLETED - Enhanced Statistics Table with 4-Category Analysis**  
- ✅ **REDESIGNED LAYOUT**: Changed from 5-column to streamlined 4-column statistics table
- ✅ **REMOVED MEDIAN VALUE**: Eliminated redundant median property value tracking  
- ✅ **ADDED MEDIAN AGE RATIO**: Intelligent ratio calculation (selected median age / total median age * 100%)
- ✅ **OPTIMIZED STRUCTURE**: 3 rows × 4 columns for focused data analysis
- ✅ **PERFECT FORMATTING**: Each cell contains descriptive label + data value with pipe separator
- ✅ **ENVIRONMENTAL READY**: Enhanced percentage analysis perfect for heating system impact studies

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

**STATUS NOTE**: Lebanon Property Tax Database is now publicly accessible with comprehensive NHDRA integration (5,660 properties, 71 columns). Enhanced dataset includes all current city parcels with comprehensive NHDRA detail data where available (5,611 enhanced, 49 city-only). Mobile-friendly hierarchical filtering is 95% complete with one remaining CSS alignment issue.

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

**FILES MODIFIED THIS SESSION**:
- `working-checkbox-filters.js` - Complete hierarchical checkbox system
- `working-checkbox-styles.css` - Touch-friendly dropdown styling  
- `index.html` and `map.html` - Updated to use new filter system

**FOR NEXT AGENT**: 
The dropdown text alignment issue appears to be caused by deeply nested CSS inheritance on the index page that's proving resistant to standard override methods. Consider investigating the exact computed style cascade or implementing an entirely different layout approach for the index page dropdown.

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