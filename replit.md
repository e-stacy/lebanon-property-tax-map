# Lebanon Property Tax Database II

## Overview

This is a property tax database and data explorer for Lebanon, New Hampshire. The project provides a comprehensive system for processing, normalizing, and visualizing property assessment data from the city. It now uses NHDRA (New Hampshire Department of Revenue Administration) data as the primary data source, providing expanded property information including building characteristics, year built, living area, bedrooms, heating systems, and construction details. The web-based data explorer interface displays this rich property information in both tabular and map formats. The system follows a "Clerk mode" approach that prioritizes evidence-based processing and maintains clear data provenance throughout the transformation pipeline.

## Recent Changes

**September 2025**: Successfully integrated comprehensive NHDRA data as the primary data source, expanding from 12 basic property fields to 25 detailed property characteristics. The new dataset includes building specifications (year built, style, living area, bedrooms, bathrooms), construction details (roofing, exterior walls, heating systems), assessment values, and sales history while maintaining existing filtering and visualization capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The project uses a file-based architecture with multiple processing stages and output formats:

**Data Processing Pipeline**: Two-stage normalization process that transforms raw city data into standardized formats. Stage A converts source columns to snake_case while preserving provenance, and Stage B maps to canonical schema for public consumption. All transformations are driven by mapping tables stored in CSV format.

**Directory Structure**: Canonical layout separating concerns - raw data in timestamped folders under `data/raw/`, immutable originals in `data/originals/`, normalized outputs in `outputs/normalized_csvs/`, and web assets in `docs/site/`. Evidence logs and alignment reports stored in `outputs/alignment_report/`.

**Web Interface**: Static site served from `docs/site/` with dual hosting support - GitHub Pages for public access and local Node.js/Express server for development. JavaScript-based data explorer loads CSV files via fetch API and renders interactive tables with filtering and summary statistics.

**Data Joining Strategy**: Uses Map-Block-Lot (MBL) keys rather than simple parcel IDs for accurate data relationships, as this matches the city's actual property identification system.

**Evidence Management**: SHA-256 manifesting system tracks all file changes with timestamped inventory reports. PowerShell-based tooling for intake, quality control, and evidence logging maintains audit trail.

**Schema Design**: Primary parcels dataset merged from NHDRA source containing 25 standardized columns including basic parcel information (ID, owner, class, values) and expanded building characteristics (year built, style, living area, bedrooms, bathrooms, heating systems, construction details). Header normalization handled client-side to accommodate variations in source data while maintaining consistent UI expectations.

## External Dependencies

**Frontend Libraries**: Leaflet for mapping functionality, PapaParse for CSV processing, Express.js for local development server

**Development Tools**: Node.js runtime with npm package management, PowerShell for Windows-based scripting and data processing workflows

**Hosting Platform**: GitHub Pages for static site deployment, GitHub repository for version control and collaboration

**Data Sources**: City of Lebanon property assessment files, NHDRA (New Hampshire Department of Revenue Administration) data, property sales records, and spatial data (shapefiles/GeoJSON)

**Processing Requirements**: Python for normalization scripts, Windows environment for PowerShell-based tooling, UTF-8 text encoding throughout pipeline