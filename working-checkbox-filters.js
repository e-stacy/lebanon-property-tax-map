/**
 * Working Checkbox Filter System
 * Provides mobile-friendly checkbox filters with proper property class names
 */

// Property class hierarchy with parent-child relationships
const PROPERTY_CLASS_HIERARCHY = {
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
        name: 'Condominium',
        primary: true,
        subclasses: ['103V']
    },
    '103V': { name: 'Condo Village', parent: '1030' },
    
    '1040': { name: 'Multi-Family 2-4 Units', primary: true },
    '1050': { name: 'Multi-Family 5+ Units', primary: true },
    '1060': { name: 'Multi-Family Other', primary: true },
    '1090': { name: 'Residential Other', primary: true },
    
    '1100': { name: 'Dormitory', primary: true },
    '1110': { name: 'Hotel/Motel', primary: true },
    '111C': { name: 'Hotel Commercial', primary: true },
    '1120': { name: 'Resort', primary: true },
    '112C': { name: 'Resort Commercial', primary: true },
    
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

class WorkingCheckboxFilters {
    constructor() {
        this.selectedClasses = new Set();
        this.allSelected = true;
        this.yearHierarchy = null;
    }

    // Create checkbox filter UI
    createPropertyClassFilter(containerId, propertyData) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('FILTER ERROR: Container element not found:', containerId);
            return;
        }
        console.log('FILTER DEBUG: Container found, creating filter for', containerId);

        // Count occurrences of each property class
        const classCounts = {};
        if (Array.isArray(propertyData)) {
            // For array data (index page)
            propertyData.forEach(property => {
                const classCode = property.class_code;
                if (classCode) {
                    classCounts[classCode] = (classCounts[classCode] || 0) + 1;
                }
            });
        } else {
            // For Map data (map page)
            propertyData.forEach(property => {
                const classCode = property.class_code;
                if (classCode) {
                    classCounts[classCode] = (classCounts[classCode] || 0) + 1;
                }
            });
        }

        // Create the filter HTML - Force left alignment with aggressive inline styles
        const filterHtml = `
            <div class="working-checkbox-filter">
                <div class="filter-label">Property Class:</div>
                <div class="checkbox-dropdown">
                    <div class="dropdown-button" onclick="toggleWorkingDropdown('${containerId}')" style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; border: 1px solid #ddd; background: white; cursor: pointer; border-radius: 4px; width: 100%; box-sizing: border-box;">
                        <span class="dropdown-text" style="text-align: left; flex-grow: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin: 0; padding: 0;">All Classes</span>
                        <span class="dropdown-arrow" style="font-size: 0.8em; margin-left: 8px; flex-shrink: 0;">▼</span>
                    </div>
                    <div class="checkbox-list" id="${containerId}-checkboxes">
                        <label class="checkbox-item">
                            <input type="checkbox" value="all" checked onchange="updateWorkingFilter('${containerId}', this)" onclick="console.log('All checkbox clicked')">
                            <span>All Classes</span>
                        </label>
                        ${this.generateClassCheckboxes(classCounts, containerId)}
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = filterHtml;
        console.log('FILTER DEBUG: HTML inserted into container', containerId);
        
        // Force alignment after DOM insertion
        setTimeout(() => {
            const dropdownButton = container.querySelector('.dropdown-button');
            const dropdownText = container.querySelector('.dropdown-text');
            if (dropdownButton && dropdownText) {
                // Nuclear option: Force styles that cannot be overridden
                dropdownButton.style.cssText = 'display: flex !important; justify-content: space-between !important; align-items: center !important; padding: 8px 12px !important; border: 1px solid #ddd !important; background: white !important; cursor: pointer !important; border-radius: 4px !important; width: 100% !important; box-sizing: border-box !important;';
                dropdownText.style.cssText = 'text-align: left !important; flex-grow: 1 !important; overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; margin: 0 !important; padding: 0 !important;';
                console.log('NUCLEAR: Forced dropdown alignment for', containerId);
            } else {
                console.error('FILTER ERROR: Dropdown elements not found after insertion');
            }
        }, 100);
    }

    generateClassCheckboxes(classCounts, containerId) {
        let html = '';
        
        // Get primary classes that exist in data, sorted by count
        const primaryClasses = Object.entries(classCounts)
            .filter(([code]) => PROPERTY_CLASS_HIERARCHY[code]?.primary)
            .sort((a, b) => b[1] - a[1])
            .map(([code, count]) => ({
                code,
                count,
                info: PROPERTY_CLASS_HIERARCHY[code]
            }));

        primaryClasses.forEach(({ code, count, info }) => {
            // Add primary class
            html += `
                <div class="checkbox-item primary-class">
                    <label>
                        <input type="checkbox" value="${code}" onchange="updateWorkingFilter('${containerId}', this)" onclick="console.log('Primary checkbox clicked:', '${code}')">
                        <span>${code} - ${info.name} (${count})</span>
                    </label>
                </div>
            `;
            
            // Add subclasses if they exist in data
            if (info.subclasses) {
                info.subclasses.forEach(subcode => {
                    if (classCounts[subcode]) {
                        const subInfo = PROPERTY_CLASS_HIERARCHY[subcode];
                        const subCount = classCounts[subcode];
                        html += `
                            <div class="checkbox-item sub-class">
                                <label>
                                    <input type="checkbox" value="${subcode}" onchange="updateWorkingFilter('${containerId}', this)" onclick="console.log('Sub checkbox clicked:', '${subcode}')">
                                    <span>${subcode} - ${subInfo.name} (${subCount})</span>
                                </label>
                            </div>
                        `;
                    }
                });
            }
        });

        return html;
    }

    // Create Year Built filter (hierarchical by decade)
    createYearBuiltFilter(containerId, propertyData) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('FILTER ERROR: Container element not found:', containerId);
            return;
        }
        console.log('FILTER DEBUG: Creating Year Built filter for', containerId);

        // Extract and clean year data
        const years = [];
        if (Array.isArray(propertyData)) {
            propertyData.forEach(property => {
                const yearValue = property['nhdra_vns ayb'];
                if (yearValue && yearValue !== '0' && yearValue !== '') {
                    const year = parseFloat(yearValue);
                    if (year >= 1800 && year <= 2029) {
                        years.push(Math.floor(year));
                    }
                }
            });
        } else {
            propertyData.forEach(property => {
                const yearValue = property['nhdra_vns ayb'];
                if (yearValue && yearValue !== '0' && yearValue !== '') {
                    const year = parseFloat(yearValue);
                    if (year >= 1800 && year <= 2029) {
                        years.push(Math.floor(year));
                    }
                }
            });
        }

        if (years.length === 0) {
            container.innerHTML = '<div>No year data available</div>';
            return;
        }

        // Count years
        const yearCounts = {};
        years.forEach(year => {
            yearCounts[year] = (yearCounts[year] || 0) + 1;
        });

        // Define decade groups
        const decadeGroups = [
            { label: '2020s', range: [2020, 2029], id: '2020s' },
            { label: '2010s', range: [2010, 2019], id: '2010s' },
            { label: '2000s', range: [2000, 2009], id: '2000s' },
            { label: '1990s', range: [1990, 1999], id: '1990s' },
            { label: '1980s', range: [1980, 1989], id: '1980s' },
            { label: '1970s', range: [1970, 1979], id: '1970s' },
            { label: '1960s', range: [1960, 1969], id: '1960s' },
            { label: '1950s', range: [1950, 1959], id: '1950s' },
            { label: '1900-1940s', range: [1900, 1949], id: '1900-1940s' },
            { label: '1850-1890s', range: [1850, 1899], id: '1850-1890s' },
            { label: '1800-1840s', range: [1800, 1849], id: '1800-1840s' }
        ];

        // Build hierarchy structure
        const hierarchy = [];
        
        decadeGroups.forEach(decade => {
            const yearsInDecade = [];
            let decadeCount = 0;
            
            for (let year = decade.range[0]; year <= decade.range[1]; year++) {
                if (yearCounts[year]) {
                    yearsInDecade.push({ year, count: yearCounts[year] });
                    decadeCount += yearCounts[year];
                }
            }
            
            if (decadeCount > 0) {
                hierarchy.push({
                    id: decade.id,
                    label: decade.label,
                    count: decadeCount,
                    children: yearsInDecade.sort((a, b) => b.year - a.year) // Newest first
                });
            }
        });

        // Generate HTML
        const allYearsCount = years.length;
        const filterHtml = `
            <div class="working-checkbox-filter">
                <div class="filter-label">Year Built:</div>
                <div class="checkbox-dropdown">
                    <div class="dropdown-button" onclick="toggleWorkingDropdown('${containerId}')" style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; border: 1px solid #ddd; background: white; cursor: pointer; border-radius: 4px; width: 100%; box-sizing: border-box;">
                        <span class="dropdown-text" style="text-align: left; flex-grow: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin: 0; padding: 0;">All Years</span>
                        <span class="dropdown-arrow" style="font-size: 0.8em; margin-left: 8px; flex-shrink: 0;">▼</span>
                    </div>
                    <div class="checkbox-list" id="${containerId}-checkboxes">
                        <label class="checkbox-item">
                            <input type="checkbox" value="all" checked onchange="updateWorkingYearFilter('${containerId}', this)">
                            <span>All Years (${allYearsCount})</span>
                        </label>
                        ${this.generateYearCheckboxes(hierarchy, containerId)}
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = filterHtml;
        console.log('FILTER DEBUG: Year filter HTML inserted');
        
        // Store hierarchy for filtering logic
        this.yearHierarchy = hierarchy;
        
        // Force alignment
        setTimeout(() => {
            const dropdownButton = container.querySelector('.dropdown-button');
            const dropdownText = container.querySelector('.dropdown-text');
            if (dropdownButton && dropdownText) {
                dropdownButton.style.cssText = 'display: flex !important; justify-content: space-between !important; align-items: center !important; padding: 8px 12px !important; border: 1px solid #ddd !important; background: white !important; cursor: pointer !important; border-radius: 4px !important; width: 100% !important; box-sizing: border-box !important;';
                dropdownText.style.cssText = 'text-align: left !important; flex-grow: 1 !important; overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; margin: 0 !important; padding: 0 !important;';
                console.log('NUCLEAR: Forced dropdown alignment for', containerId);
            }
        }, 100);
    }

    generateYearCheckboxes(hierarchy, containerId) {
        let html = '';
        
        hierarchy.forEach(decade => {
            // Add decade (parent)
            html += `
                <div class="checkbox-item primary-class">
                    <label>
                        <input type="checkbox" value="${decade.id}" onchange="updateWorkingYearFilter('${containerId}', this)">
                        <span>${decade.label} (${decade.count})</span>
                    </label>
                </div>
            `;
            
            // Add individual years (children)
            decade.children.forEach(yearData => {
                html += `
                    <div class="checkbox-item sub-class">
                        <label>
                            <input type="checkbox" value="${yearData.year}" onchange="updateWorkingYearFilter('${containerId}', this)">
                            <span>${yearData.year} (${yearData.count})</span>
                        </label>
                    </div>
                `;
            });
        });

        return html;
    }

    getSelectedYears(containerId) {
        const checkboxes = document.querySelectorAll(`#${containerId}-checkboxes input[type="checkbox"]:checked`);
        const selected = Array.from(checkboxes).map(cb => cb.value);
        
        console.log('DEBUG: All checked year boxes:', selected);
        
        if (selected.includes('all')) {
            console.log('DEBUG: All years selected, returning empty array');
            return []; // Empty array means "all"
        }
        
        // Expand decade selections to individual years
        const expandedYears = new Set();
        
        selected.forEach(value => {
            if (this.yearHierarchy) {
                // Check if this is a decade ID
                const decade = this.yearHierarchy.find(d => d.id === value);
                if (decade) {
                    // Add all years in this decade
                    decade.children.forEach(yearData => {
                        expandedYears.add(yearData.year.toString());
                    });
                } else {
                    // It's an individual year
                    expandedYears.add(value);
                }
            } else {
                expandedYears.add(value);
            }
        });
        
        console.log('DEBUG: Expanded selected years:', Array.from(expandedYears));
        return Array.from(expandedYears);
    }

    getSelectedClasses(containerId) {
        const checkboxes = document.querySelectorAll(`#${containerId}-checkboxes input[type="checkbox"]:checked`);
        const selected = Array.from(checkboxes).map(cb => cb.value);
        
        console.log('DEBUG: All checked boxes:', selected);
        
        if (selected.includes('all')) {
            console.log('DEBUG: All is included, returning empty array');
            return []; // Empty array means "all"
        }
        console.log('DEBUG: Returning specific selections:', selected);
        return selected;
    }
}

// Global instance
const workingFilters = new WorkingCheckboxFilters();

// UI interaction functions
function toggleWorkingDropdown(containerId) {
    const dropdown = document.getElementById(`${containerId}-checkboxes`);
    const isVisible = dropdown.style.display === 'block';
    
    // Close all dropdowns first
    document.querySelectorAll('.checkbox-list').forEach(list => {
        list.style.display = 'none';
    });
    
    // Toggle this one
    dropdown.style.display = isVisible ? 'none' : 'block';
}

// Track which checkbox was clicked to handle hierarchical behavior
let lastClickedCheckbox = null;

function updateWorkingFilter(containerId, clickedElement = null) {
    const allCheckbox = document.querySelector(`#${containerId}-checkboxes input[value="all"]`);
    const otherCheckboxes = document.querySelectorAll(`#${containerId}-checkboxes input[type="checkbox"]:not([value="all"])`);
    const dropdownText = document.querySelector(`#${containerId}-checkboxes`).parentNode.querySelector('.dropdown-text');
    
    console.log('updateWorkingFilter called for:', containerId);
    
    // HIERARCHICAL BEHAVIOR: Handle parent-child relationships
    if (clickedElement && clickedElement !== allCheckbox) {
        const clickedCode = clickedElement.value;
        const clickedInfo = PROPERTY_CLASS_HIERARCHY[clickedCode];
        
        if (clickedInfo && clickedInfo.primary && clickedInfo.subclasses) {
            // This is a parent class
            if (clickedElement.checked) {
                // Parent was checked - check all children
                console.log('DEBUG: Parent checked, auto-checking children for', clickedCode);
                clickedInfo.subclasses.forEach(subcode => {
                    const subCheckbox = document.querySelector(`#${containerId}-checkboxes input[value="${subcode}"]`);
                    if (subCheckbox) {
                        subCheckbox.checked = true;
                        console.log('DEBUG: Auto-checked child', subcode);
                    }
                });
            } else {
                // Parent was unchecked - uncheck all children
                console.log('DEBUG: Parent unchecked, clearing children for', clickedCode);
                clickedInfo.subclasses.forEach(subcode => {
                    const subCheckbox = document.querySelector(`#${containerId}-checkboxes input[value="${subcode}"]`);
                    if (subCheckbox) {
                        subCheckbox.checked = false;
                        console.log('DEBUG: Unchecked child', subcode);
                    }
                });
            }
        } else {
            // This might be a child class - check if we need to uncheck its parent
            if (!clickedElement.checked) {
                // Child was unchecked - find and uncheck its parent
                for (const [parentCode, parentInfo] of Object.entries(PROPERTY_CLASS_HIERARCHY)) {
                    if (parentInfo.primary && parentInfo.subclasses && parentInfo.subclasses.includes(clickedCode)) {
                        const parentCheckbox = document.querySelector(`#${containerId}-checkboxes input[value="${parentCode}"]`);
                        if (parentCheckbox && parentCheckbox.checked) {
                            parentCheckbox.checked = false;
                            console.log('DEBUG: Child unchecked, so unchecked parent', parentCode);
                        }
                        break;
                    }
                }
            }
        }
    }
    
    // Check how many specific checkboxes are checked (after hierarchical changes)
    const checkedOthers = Array.from(otherCheckboxes).filter(cb => cb.checked);
    console.log('DEBUG: Found', checkedOthers.length, 'specific checkboxes checked');
    
    if (checkedOthers.length > 0) {
        // If any specific boxes are checked, uncheck "All"
        if (allCheckbox) {
            allCheckbox.checked = false;
            console.log('DEBUG: Unchecked All checkbox');
        }
        
        // Update text to show selection
        if (checkedOthers.length === 1) {
            const selectedText = checkedOthers[0].nextElementSibling.textContent;
            dropdownText.textContent = selectedText.length > 30 
                ? selectedText.substring(0, 27) + '...' 
                : selectedText;
        } else {
            dropdownText.textContent = `${checkedOthers.length} classes selected`;
        }
    } else {
        // If no specific boxes are checked, check "All"
        if (allCheckbox) {
            allCheckbox.checked = true;
            console.log('DEBUG: Checked All checkbox');
        }
        dropdownText.textContent = 'All Classes';
    }
    
    // Apply filters for the specific page
    if (containerId === 'class-filter') {
        // Get selected classes using the working filter system
        const selectedClasses = workingFilters.getSelectedClasses(containerId);
        console.log('Selected classes:', selectedClasses);
        
        // Call the appropriate filter function based on which page we're on
        if (typeof applyFilters === 'function') {
            applyFilters();
        }
    }
}

// Year filter update function with hierarchical behavior
function updateWorkingYearFilter(containerId, clickedElement = null) {
    const allCheckbox = document.querySelector(`#${containerId}-checkboxes input[value="all"]`);
    const otherCheckboxes = document.querySelectorAll(`#${containerId}-checkboxes input[type="checkbox"]:not([value="all"])`);
    const dropdownText = document.querySelector(`#${containerId}-checkboxes`).parentNode.querySelector('.dropdown-text');
    
    console.log('updateWorkingYearFilter called for:', containerId);
    
    // HIERARCHICAL BEHAVIOR: Handle decade-year relationships
    if (clickedElement && clickedElement !== allCheckbox && workingFilters.yearHierarchy) {
        const clickedValue = clickedElement.value;
        
        // Check if clicked value is a decade
        const decade = workingFilters.yearHierarchy.find(d => d.id === clickedValue);
        if (decade) {
            // This is a decade - handle parent behavior
            if (clickedElement.checked) {
                // Decade was checked - check all its years
                console.log('DEBUG: Decade checked, auto-checking years for', clickedValue);
                decade.children.forEach(yearData => {
                    const yearCheckbox = document.querySelector(`#${containerId}-checkboxes input[value="${yearData.year}"]`);
                    if (yearCheckbox) {
                        yearCheckbox.checked = true;
                        console.log('DEBUG: Auto-checked year', yearData.year);
                    }
                });
            } else {
                // Decade was unchecked - uncheck all its years
                console.log('DEBUG: Decade unchecked, clearing years for', clickedValue);
                decade.children.forEach(yearData => {
                    const yearCheckbox = document.querySelector(`#${containerId}-checkboxes input[value="${yearData.year}"]`);
                    if (yearCheckbox) {
                        yearCheckbox.checked = false;
                        console.log('DEBUG: Unchecked year', yearData.year);
                    }
                });
            }
        } else {
            // This is an individual year - check if we need to uncheck its decade
            if (!clickedElement.checked) {
                // Year was unchecked - find and uncheck its decade
                for (const decade of workingFilters.yearHierarchy) {
                    const yearExists = decade.children.some(yearData => yearData.year.toString() === clickedValue);
                    if (yearExists) {
                        const decadeCheckbox = document.querySelector(`#${containerId}-checkboxes input[value="${decade.id}"]`);
                        if (decadeCheckbox && decadeCheckbox.checked) {
                            decadeCheckbox.checked = false;
                            console.log('DEBUG: Year unchecked, so unchecked decade', decade.id);
                        }
                        break;
                    }
                }
            }
        }
    }
    
    // Check how many specific checkboxes are checked (after hierarchical changes)
    const checkedOthers = Array.from(otherCheckboxes).filter(cb => cb.checked);
    console.log('DEBUG: Found', checkedOthers.length, 'specific year checkboxes checked');
    
    if (checkedOthers.length > 0) {
        // If any specific boxes are checked, uncheck "All"
        if (allCheckbox) {
            allCheckbox.checked = false;
            console.log('DEBUG: Unchecked All years checkbox');
        }
        
        // Update text to show selection
        if (checkedOthers.length === 1) {
            const selectedText = checkedOthers[0].nextElementSibling.textContent;
            dropdownText.textContent = selectedText.length > 30 
                ? selectedText.substring(0, 27) + '...' 
                : selectedText;
        } else {
            dropdownText.textContent = `${checkedOthers.length} years selected`;
        }
    } else {
        // If no specific boxes are checked, check "All"
        if (allCheckbox) {
            allCheckbox.checked = true;
            console.log('DEBUG: Checked All years checkbox');
        }
        dropdownText.textContent = 'All Years';
    }
    
    // Apply filters
    if (typeof applyFilters === 'function') {
        applyFilters();
    }
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(e) {
    if (!e.target.closest('.checkbox-dropdown')) {
        document.querySelectorAll('.checkbox-list').forEach(list => {
            list.style.display = 'none';
        });
    }
});

// Initialize functions for each page
function initializeWorkingFilters() {
    // For index page
    if (typeof allParcels !== 'undefined' && allParcels.length > 0) {
        workingFilters.createPropertyClassFilter('class-filter', allParcels);
        workingFilters.createYearBuiltFilter('year-filter', allParcels);
    }
    
    // For map page  
    if (typeof propertyData !== 'undefined' && propertyData.size > 0) {
        workingFilters.createPropertyClassFilter('class-filter', propertyData);
        workingFilters.createYearBuiltFilter('year-filter', propertyData);
    }
}

// Helper function to get selected values for existing code
function getSelectedValues(containerId) {
    if (containerId === 'year-filter') {
        return workingFilters.getSelectedYears(containerId);
    }
    return workingFilters.getSelectedClasses(containerId);
}