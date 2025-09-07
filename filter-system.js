/**
 * Dynamic Hierarchical Filter System for Lebanon Property Tax Database
 * Builds filters from actual data and maintains parent-child relationships
 */

class HierarchicalFilterSystem {
    constructor() {
        this.propertyClassHierarchy = {
            '1010': {
                name: 'Residential Single Family',
                primary: true,
                subclasses: ['1012', '101A', '101C', '101T']
            },
            '1012': { name: 'Residential Multi-Unit', parent: '1010' },
            '101A': { name: 'Residential Accessory', parent: '1010' },
            '101C': { name: 'Residential Commercial', parent: '1010' },
            '101T': { name: 'Residential Temp', parent: '1010' },
            
            '1020': {
                name: 'Manufactured Housing',
                primary: true,
                subclasses: ['102C', '102V']
            },
            '102C': { name: 'Manufactured Commercial', parent: '1020' },
            '102V': { name: 'Manufactured Village', parent: '1020' },
            
            '1030': {
                name: 'Residential Multi-Family',
                primary: true,
                subclasses: ['103V']
            },
            '103V': { name: 'Multi-Family Village', parent: '1030' },
            
            '1040': { name: 'Residential Condominium', primary: true },
            '1050': { name: 'Residential Cooperative', primary: true },
            '1060': { name: 'Residential Other', primary: true },
            
            '1110': { name: 'Commercial Retail', primary: true },
            '1120': { name: 'Commercial Office', primary: true },
            
            '1300': { name: 'Vacant Residential Land', primary: true },
            '1310': { name: 'Vacant Commercial Land', primary: true },
            '1320': { name: 'Vacant Industrial Land', primary: true },
            
            '3000': { name: 'Agricultural', primary: true },
            '3160': { name: 'Forest Land', primary: true },
            '3250': { name: 'Open Space/Recreation', primary: true },
            '3400': { name: 'Other Exempt', primary: true },
            
            '6231': { name: 'Utility - Gas', primary: true },
            
            '9010': { name: 'State Property', primary: true },
            '9030': { name: 'Municipal Property', primary: true },
            '9090': { name: 'Other Government', primary: true }
        };
        
        this.filters = {
            propertyClass: new Set(['all']),
            yearBuilt: { min: null, max: null },
            zoning: new Set(['all'])
        };
        
        this.activeFilterData = {
            propertyClasses: new Map(),
            zones: new Map(),
            yearRange: { min: 1800, max: 2025 }
        };
    }

    /**
     * Build filter options from actual data
     */
    buildFiltersFromData(parcelData) {
        // Reset data
        this.activeFilterData.propertyClasses.clear();
        this.activeFilterData.zones.clear();
        
        // Count property classes and zones
        parcelData.forEach(parcel => {
            if (parcel.class_code) {
                const count = this.activeFilterData.propertyClasses.get(parcel.class_code) || 0;
                this.activeFilterData.propertyClasses.set(parcel.class_code, count + 1);
            }
            
            if (parcel.zoning) {
                const count = this.activeFilterData.zones.get(parcel.zoning) || 0;
                this.activeFilterData.zones.set(parcel.zoning, count + 1);
            }
            
            // Track year range
            if (parcel.year_built && !isNaN(parcel.year_built)) {
                const year = parseInt(parcel.year_built);
                if (year >= 1800 && year <= 2025) {
                    this.activeFilterData.yearRange.min = Math.min(this.activeFilterData.yearRange.min, year);
                    this.activeFilterData.yearRange.max = Math.max(this.activeFilterData.yearRange.max, year);
                }
            }
        });
        
        console.log('Filter data built:', {
            propertyClasses: Array.from(this.activeFilterData.propertyClasses.entries()).slice(0, 10),
            zones: Array.from(this.activeFilterData.zones.entries()).slice(0, 10),
            yearRange: this.activeFilterData.yearRange
        });
    }

    /**
     * Create hierarchical property class dropdown
     */
    createPropertyClassFilter(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const dropdown = this.createDropdownStructure(containerId + '-dropdown', 'Property Classes');
        container.appendChild(dropdown);

        const checkboxContainer = dropdown.querySelector('.checkbox-container');
        
        // Add "All Classes" option
        checkboxContainer.appendChild(this.createCheckboxItem('all', 'All Classes', 0, true, false));
        
        // Build hierarchical structure
        const primaryClasses = [];
        
        for (const [classCode, info] of Object.entries(this.propertyClassHierarchy)) {
            if (info.primary && this.activeFilterData.propertyClasses.has(classCode)) {
                primaryClasses.push({
                    code: classCode,
                    info: info,
                    count: this.activeFilterData.propertyClasses.get(classCode)
                });
            }
        }
        
        // Sort by count descending
        primaryClasses.sort((a, b) => b.count - a.count);
        
        primaryClasses.forEach(({ code, info, count }) => {
            // Add primary class
            const parentItem = this.createCheckboxItem(code, info.name, count, false, false);
            checkboxContainer.appendChild(parentItem);
            
            // Add subclasses if they exist
            if (info.subclasses) {
                info.subclasses.forEach(subclass => {
                    if (this.activeFilterData.propertyClasses.has(subclass)) {
                        const subInfo = this.propertyClassHierarchy[subclass];
                        const subCount = this.activeFilterData.propertyClasses.get(subclass);
                        const subItem = this.createCheckboxItem(subclass, subInfo.name, subCount, false, true);
                        checkboxContainer.appendChild(subItem);
                    }
                });
            }
        });
        
        // Add change handlers
        this.addPropertyClassChangeHandlers(checkboxContainer);
    }

    /**
     * Create zoning district filter
     */
    createZoningFilter(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const dropdown = this.createDropdownStructure(containerId + '-dropdown', 'Zoning Districts');
        container.appendChild(dropdown);

        const checkboxContainer = dropdown.querySelector('.checkbox-container');
        
        // Add "All Zones" option
        checkboxContainer.appendChild(this.createCheckboxItem('all', 'All Zoning Districts', 0, true, false));
        
        // Sort zones by count
        const sortedZones = Array.from(this.activeFilterData.zones.entries())
            .sort((a, b) => b[1] - a[1]);
        
        sortedZones.forEach(([zone, count]) => {
            const zoneName = this.getZoneDisplayName(zone);
            checkboxContainer.appendChild(this.createCheckboxItem(zone, zoneName, count, false, false));
        });
        
        // Add change handlers  
        this.addZoningChangeHandlers(checkboxContainer);
    }

    /**
     * Create year built range filter
     */
    createYearBuiltFilter(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const filterDiv = document.createElement('div');
        filterDiv.className = 'filter-group';
        filterDiv.innerHTML = `
            <label>Year Built Range:</label>
            <div style="display: flex; gap: 8px; align-items: center;">
                <input type="number" id="year-min" placeholder="${this.activeFilterData.yearRange.min}" 
                       min="${this.activeFilterData.yearRange.min}" max="${this.activeFilterData.yearRange.max}"
                       style="width: 80px;">
                <span>to</span>
                <input type="number" id="year-max" placeholder="${this.activeFilterData.yearRange.max}"
                       min="${this.activeFilterData.yearRange.min}" max="${this.activeFilterData.yearRange.max}"
                       style="width: 80px;">
            </div>
            <div style="font-size: 0.8em; color: #666; margin-top: 4px;">
                Range: ${this.activeFilterData.yearRange.min} - ${this.activeFilterData.yearRange.max}
            </div>
        `;
        
        container.appendChild(filterDiv);
        
        // Add change handlers
        ['year-min', 'year-max'].forEach(id => {
            document.getElementById(id).addEventListener('change', () => {
                this.updateYearFilter();
                this.applyFilters();
            });
        });
    }

    /**
     * Create dropdown structure
     */
    createDropdownStructure(id, title) {
        const dropdown = document.createElement('div');
        dropdown.className = 'filter-dropdown';
        dropdown.innerHTML = `
            <div class="filter-group">
                <label>${title}:</label>
                <div class="dropdown-header" onclick="this.parentElement.parentElement.classList.toggle('open')">
                    <span class="dropdown-title">All Classes</span>
                    <span class="dropdown-arrow">▼</span>
                </div>
                <div class="checkbox-container"></div>
            </div>
        `;
        dropdown.id = id;
        return dropdown;
    }

    /**
     * Create checkbox item
     */
    createCheckboxItem(value, label, count, checked, isSubclass) {
        const item = document.createElement('div');
        item.className = `checkbox-item ${isSubclass ? 'subclass' : ''}`;
        item.innerHTML = `
            <label>
                <input type="checkbox" value="${value}" ${checked ? 'checked' : ''}>
                <span class="checkbox-label">${label}</span>
                ${count > 0 ? `<span class="count">(${count})</span>` : ''}
            </label>
        `;
        return item;
    }

    /**
     * Add property class change handlers
     */
    addPropertyClassChangeHandlers(container) {
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');
        
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.handlePropertyClassChange(e.target, container);
                this.updateDropdownTitle(container.closest('.filter-dropdown'));
                this.applyFilters();
            });
        });
    }

    /**
     * Handle property class checkbox changes with hierarchy logic
     */
    handlePropertyClassChange(changedCheckbox, container) {
        const value = changedCheckbox.value;
        const isChecked = changedCheckbox.checked;
        
        if (value === 'all') {
            // All classes toggled
            if (isChecked) {
                // Check all, uncheck others
                container.querySelectorAll('input[type="checkbox"]').forEach(cb => {
                    cb.checked = cb.value === 'all';
                });
                this.filters.propertyClass.clear();
                this.filters.propertyClass.add('all');
            }
        } else {
            // Specific class toggled
            const allCheckbox = container.querySelector('input[value="all"]');
            allCheckbox.checked = false;
            this.filters.propertyClass.delete('all');
            
            const classInfo = this.propertyClassHierarchy[value];
            
            if (isChecked) {
                this.filters.propertyClass.add(value);
                
                // If this is a primary class, check all its subclasses
                if (classInfo && classInfo.subclasses) {
                    classInfo.subclasses.forEach(subclass => {
                        const subCheckbox = container.querySelector(`input[value="${subclass}"]`);
                        if (subCheckbox) {
                            subCheckbox.checked = true;
                            this.filters.propertyClass.add(subclass);
                        }
                    });
                }
            } else {
                this.filters.propertyClass.delete(value);
                
                // If this is a subclass, uncheck parent if no other subclasses are checked
                if (classInfo && classInfo.parent) {
                    const parent = classInfo.parent;
                    const parentInfo = this.propertyClassHierarchy[parent];
                    const anySubclassChecked = parentInfo.subclasses.some(sub => 
                        this.filters.propertyClass.has(sub)
                    );
                    
                    if (!anySubclassChecked) {
                        const parentCheckbox = container.querySelector(`input[value="${parent}"]`);
                        if (parentCheckbox) {
                            parentCheckbox.checked = false;
                            this.filters.propertyClass.delete(parent);
                        }
                    }
                }
                
                // If this is a primary class, uncheck all subclasses
                if (classInfo && classInfo.subclasses) {
                    classInfo.subclasses.forEach(subclass => {
                        const subCheckbox = container.querySelector(`input[value="${subclass}"]`);
                        if (subCheckbox) {
                            subCheckbox.checked = false;
                            this.filters.propertyClass.delete(subclass);
                        }
                    });
                }
            }
            
            // If no classes selected, revert to all
            if (this.filters.propertyClass.size === 0) {
                allCheckbox.checked = true;
                this.filters.propertyClass.add('all');
            }
        }
    }

    /**
     * Add zoning change handlers
     */
    addZoningChangeHandlers(container) {
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');
        
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.handleZoningChange(e.target, container);
                this.updateDropdownTitle(container.closest('.filter-dropdown'));
                this.applyFilters();
            });
        });
    }

    /**
     * Handle zoning checkbox changes
     */
    handleZoningChange(changedCheckbox, container) {
        const value = changedCheckbox.value;
        const isChecked = changedCheckbox.checked;
        
        if (value === 'all') {
            if (isChecked) {
                container.querySelectorAll('input[type="checkbox"]').forEach(cb => {
                    cb.checked = cb.value === 'all';
                });
                this.filters.zoning.clear();
                this.filters.zoning.add('all');
            }
        } else {
            const allCheckbox = container.querySelector('input[value="all"]');
            allCheckbox.checked = false;
            this.filters.zoning.delete('all');
            
            if (isChecked) {
                this.filters.zoning.add(value);
            } else {
                this.filters.zoning.delete(value);
            }
            
            if (this.filters.zoning.size === 0) {
                allCheckbox.checked = true;
                this.filters.zoning.add('all');
            }
        }
    }

    /**
     * Update year filter
     */
    updateYearFilter() {
        const minInput = document.getElementById('year-min');
        const maxInput = document.getElementById('year-max');
        
        this.filters.yearBuilt.min = minInput.value ? parseInt(minInput.value) : null;
        this.filters.yearBuilt.max = maxInput.value ? parseInt(maxInput.value) : null;
    }

    /**
     * Update dropdown title based on selections
     */
    updateDropdownTitle(dropdown) {
        const titleElement = dropdown.querySelector('.dropdown-title');
        const checkboxes = dropdown.querySelectorAll('input[type="checkbox"]:checked');
        
        if (checkboxes.length === 0 || checkboxes[0].value === 'all') {
            titleElement.textContent = checkboxes[0].nextElementSibling.textContent;
        } else {
            const count = checkboxes.length;
            titleElement.textContent = `${count} selected`;
        }
    }

    /**
     * Get zone display name
     */
    getZoneDisplayName(zone) {
        const zoneNames = {
            'R1': 'Residential R1',
            'R2': 'Residential R2', 
            'R3': 'Residential R3',
            'RL1': 'Rural Residential RL1',
            'RL2': 'Rural Residential RL2', 
            'RL3': 'Rural Residential RL3',
            'CBD': 'Central Business District',
            'GC': 'General Commercial',
            'INDL': 'Industrial',
            'INDH': 'Industrial Heavy',
            'INDR': 'Industrial Restricted',
            'LD': 'Light Development',
            'MC': 'Medical Center',
            'RO': 'Recreation/Open Space',
            'RO1': 'Recreation/Open Space 1',
            'PBD': 'Planned Business Development'
        };
        return zoneNames[zone] || zone;
    }

    /**
     * Apply filters to data
     */
    applyFilters() {
        // This method will be called by the main application
        // to trigger filter application
        if (window.updateParcelLayer) {
            window.updateParcelLayer();
        }
        if (window.renderTable) {
            window.renderTable();
        }
    }

    /**
     * Check if parcel matches current filters
     */
    matchesFilters(parcel) {
        // Property class filter
        if (!this.filters.propertyClass.has('all')) {
            if (!this.filters.propertyClass.has(parcel.class_code)) {
                return false;
            }
        }
        
        // Zoning filter
        if (!this.filters.zoning.has('all')) {
            if (!this.filters.zoning.has(parcel.zoning)) {
                return false;
            }
        }
        
        // Year built filter
        if (parcel.year_built && !isNaN(parcel.year_built)) {
            const year = parseInt(parcel.year_built);
            if (this.filters.yearBuilt.min && year < this.filters.yearBuilt.min) {
                return false;
            }
            if (this.filters.yearBuilt.max && year > this.filters.yearBuilt.max) {
                return false;
            }
        }
        
        return true;
    }

    /**
     * Get current filter summary
     */
    getFilterSummary() {
        const summary = [];
        
        if (!this.filters.propertyClass.has('all')) {
            summary.push(`${this.filters.propertyClass.size} property classes`);
        }
        
        if (!this.filters.zoning.has('all')) {
            summary.push(`${this.filters.zoning.size} zones`);
        }
        
        if (this.filters.yearBuilt.min || this.filters.yearBuilt.max) {
            const range = `${this.filters.yearBuilt.min || 'earliest'}-${this.filters.yearBuilt.max || 'latest'}`;
            summary.push(`Built ${range}`);
        }
        
        return summary.length > 0 ? summary.join(', ') : 'All Properties';
    }

    /**
     * Clear all filters
     */
    clearAllFilters() {
        this.filters.propertyClass.clear();
        this.filters.propertyClass.add('all');
        this.filters.zoning.clear();
        this.filters.zoning.add('all');
        this.filters.yearBuilt = { min: null, max: null };
        
        // Update UI
        document.querySelectorAll('.filter-dropdown input[type="checkbox"]').forEach(cb => {
            cb.checked = cb.value === 'all';
        });
        
        document.querySelectorAll('.dropdown-title').forEach(title => {
            if (title.closest('.filter-dropdown').id.includes('property-class')) {
                title.textContent = 'All Classes';
            } else if (title.closest('.filter-dropdown').id.includes('zoning')) {
                title.textContent = 'All Zoning Districts';
            }
        });
        
        const yearMin = document.getElementById('year-min');
        const yearMax = document.getElementById('year-max');
        if (yearMin) yearMin.value = '';
        if (yearMax) yearMax.value = '';
        
        this.applyFilters();
    }
}

// Global instance
window.filterSystem = new HierarchicalFilterSystem();