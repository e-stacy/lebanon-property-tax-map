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
    }

    // Create checkbox filter UI
    createPropertyClassFilter(containerId, propertyData) {
        const container = document.getElementById(containerId);
        if (!container) return;

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

        // Create the filter HTML
        const filterHtml = `
            <div class="working-checkbox-filter">
                <div class="filter-label">Property Class:</div>
                <div class="checkbox-dropdown">
                    <div class="dropdown-button" onclick="toggleWorkingDropdown('${containerId}')">
                        <span class="dropdown-text">All Classes</span>
                        <span class="dropdown-arrow">▼</span>
                    </div>
                    <div class="checkbox-list" id="${containerId}-checkboxes">
                        <label class="checkbox-item">
                            <input type="checkbox" value="all" checked onchange="updateWorkingFilter('${containerId}')">
                            <span>All Classes</span>
                        </label>
                        ${this.generateClassCheckboxes(classCounts, containerId)}
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = filterHtml;
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
                        <input type="checkbox" value="${code}" onchange="updateWorkingFilter('${containerId}')">
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
                                    <input type="checkbox" value="${subcode}" onchange="updateWorkingFilter('${containerId}')">
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

    getSelectedClasses(containerId) {
        const checkboxes = document.querySelectorAll(`#${containerId}-checkboxes input[type="checkbox"]:checked`);
        const selected = Array.from(checkboxes).map(cb => cb.value);
        
        if (selected.includes('all')) {
            return []; // Empty array means "all"
        }
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

function updateWorkingFilter(containerId) {
    const allCheckbox = document.querySelector(`#${containerId}-checkboxes input[value="all"]`);
    const otherCheckboxes = document.querySelectorAll(`#${containerId}-checkboxes input[type="checkbox"]:not([value="all"])`);
    const dropdownText = document.querySelector(`#${containerId}-checkboxes`).parentNode.querySelector('.dropdown-text');
    
    console.log('updateWorkingFilter called for:', containerId);
    
    if (allCheckbox.checked) {
        // If "All" is checked, uncheck others
        otherCheckboxes.forEach(cb => cb.checked = false);
        dropdownText.textContent = 'All Classes';
    } else {
        // Check if any others are checked
        const checkedOthers = Array.from(otherCheckboxes).filter(cb => cb.checked);
        
        if (checkedOthers.length === 0) {
            // If none are checked, check "All"
            allCheckbox.checked = true;
            dropdownText.textContent = 'All Classes';
        } else {
            // Update text to show selection
            if (checkedOthers.length === 1) {
                const selectedText = checkedOthers[0].nextElementSibling.textContent;
                dropdownText.textContent = selectedText.length > 30 
                    ? selectedText.substring(0, 27) + '...' 
                    : selectedText;
            } else {
                dropdownText.textContent = `${checkedOthers.length} classes selected`;
            }
        }
    }
    
    // Trigger filter application
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
    }
    
    // For map page  
    if (typeof propertyData !== 'undefined' && propertyData.size > 0) {
        workingFilters.createPropertyClassFilter('class-filter', propertyData);
    }
}

// Helper function to get selected values for existing code
function getSelectedValues(containerId) {
    return workingFilters.getSelectedClasses(containerId);
}