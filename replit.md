# Lebanon Property Tax Database II

## Overview

This is a property tax database and data explorer for Lebanon, New Hampshire. The project provides a comprehensive system for processing, normalizing, and visualizing property assessment data from the city. It includes normalized CSV datasets for parcels, buildings, land, sales, and NHDRA data, along with a web-based data explorer interface that displays property information in both tabular and map formats. The system follows a "Clerk mode" approach that prioritizes evidence-based processing and maintains clear data provenance throughout the transformation pipeline.

## Current Status (September 2025)

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

**STATUS NOTE**: Lebanon Property Tax Database is now publicly accessible with enhanced NHDRA integration (5,622 properties, 25 columns). All systems operational and ready for expansion with additional city data.

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