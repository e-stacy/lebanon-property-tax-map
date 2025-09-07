/**
 * Working Checkbox Filter System
 * Provides mobile-friendly checkbox filters with proper property class names
 */

// Property class hierarchy with readable names
const PROPERTY_CLASSES = {
    '1010': 'Residential Single Family',
    '1012': 'Residential Multi-Unit', 
    '101A': 'Residential Accessory',
    '101C': 'Residential Commercial',
    '101T': 'Residential Temp',
    '1020': 'Manufactured Housing',
    '102C': 'Manufactured Commercial',
    '102V': 'Manufactured Village',
    '1030': 'Condominium',
    '103V': 'Condo Village',
    '1040': 'Multi-Family 2-4 Units',
    '1050': 'Multi-Family 5+ Units',
    '1060': 'Multi-Family Other',
    '1090': 'Residential Other',
    '1100': 'Dormitory',
    '1110': 'Hotel/Motel',
    '111C': 'Hotel Commercial',
    '1120': 'Resort',
    '112C': 'Resort Commercial',
    '1300': 'Vacant Residential Land',
    '1310': 'Vacant Commercial Land',
    '1320': 'Vacant Industrial Land',
    '3000': 'Agricultural',
    '3160': 'Forest Land',
    '3250': 'Open Space/Recreation',
    '3400': 'Other Exempt',
    '6231': 'Utility - Gas',
    '9010': 'State Property',
    '9030': 'Municipal Property',
    '9090': 'Other Government'
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
        // Sort by count (descending) then by name
        const sortedClasses = Object.entries(classCounts)
            .sort((a, b) => b[1] - a[1])
            .map(([code, count]) => ({
                code,
                count,
                name: PROPERTY_CLASSES[code] || `Class ${code}`
            }));

        return sortedClasses.map(({code, count, name}) => `
            <label class="checkbox-item">
                <input type="checkbox" value="${code}" onchange="updateWorkingFilter('${containerId}')">
                <span>${code} - ${name} (${count})</span>
            </label>
        `).join('');
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