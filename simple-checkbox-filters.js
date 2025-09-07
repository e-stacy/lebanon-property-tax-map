/**
 * Simple Checkbox Filter System - Non-invasive approach
 * Converts existing dropdowns to checkbox lists
 */

function createCheckboxFilter(selectId, data, labelText) {
    const selectElement = document.getElementById(selectId);
    if (!selectElement) return;
    
    // Create container
    const container = document.createElement('div');
    container.className = 'checkbox-filter';
    container.innerHTML = `
        <div class="filter-label">${labelText}</div>
        <div class="checkbox-dropdown">
            <div class="dropdown-button" onclick="toggleCheckboxDropdown('${selectId}')">
                <span class="dropdown-text">All Classes</span>
                <span class="dropdown-arrow">▼</span>
            </div>
            <div class="checkbox-list" id="${selectId}-checkboxes">
                <label class="checkbox-item">
                    <input type="checkbox" value="" checked onchange="updateCheckboxFilter('${selectId}')">
                    <span>All Classes</span>
                </label>
            </div>
        </div>
    `;
    
    // Replace the select element
    selectElement.parentNode.replaceChild(container, selectElement);
    
    // Add options as checkboxes
    const checkboxList = document.getElementById(`${selectId}-checkboxes`);
    Object.entries(data).forEach(([value, label]) => {
        if (value) { // Skip empty values
            const checkboxItem = document.createElement('label');
            checkboxItem.className = 'checkbox-item';
            checkboxItem.innerHTML = `
                <input type="checkbox" value="${value}" onchange="updateCheckboxFilter('${selectId}')">
                <span>${label}</span>
            `;
            checkboxList.appendChild(checkboxItem);
        }
    });
}

function toggleCheckboxDropdown(selectId) {
    const dropdown = document.getElementById(`${selectId}-checkboxes`);
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    
    // Close other dropdowns
    document.querySelectorAll('.checkbox-list').forEach(list => {
        if (list.id !== `${selectId}-checkboxes`) {
            list.style.display = 'none';
        }
    });
}

function updateCheckboxFilter(selectId) {
    const checkboxes = document.querySelectorAll(`#${selectId}-checkboxes input[type="checkbox"]`);
    const dropdownText = document.querySelector(`#${selectId}-checkboxes`).parentNode.querySelector('.dropdown-text');
    
    // Handle "All" checkbox
    const allCheckbox = checkboxes[0]; // First checkbox is "All"
    const otherCheckboxes = Array.from(checkboxes).slice(1);
    
    if (allCheckbox.checked) {
        // If "All" is checked, uncheck others
        otherCheckboxes.forEach(cb => cb.checked = false);
        dropdownText.textContent = 'All Classes';
    } else {
        // Check if any others are checked
        const checkedOthers = otherCheckboxes.filter(cb => cb.checked);
        if (checkedOthers.length === 0) {
            // If none are checked, check "All"
            allCheckbox.checked = true;
            dropdownText.textContent = 'All Classes';
        } else {
            // Update text to show count
            dropdownText.textContent = checkedOthers.length === 1 
                ? checkedOthers[0].nextElementSibling.textContent
                : `${checkedOthers.length} selected`;
        }
    }
    
    // Trigger existing filter function
    if (typeof applyFilters === 'function') {
        applyFilters();
    }
}

function getSelectedValues(selectId) {
    const checkboxes = document.querySelectorAll(`#${selectId}-checkboxes input[type="checkbox"]:checked`);
    const values = Array.from(checkboxes).map(cb => cb.value).filter(v => v); // Filter out empty values
    return values.length === 0 ? [''] : values; // Return empty array if "All" is selected
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(e) {
    if (!e.target.closest('.checkbox-dropdown')) {
        document.querySelectorAll('.checkbox-list').forEach(list => {
            list.style.display = 'none';
        });
    }
});

// Initialize checkbox filters when called
function initializeCheckboxFilters(propertyClasses) {
    // Convert property classes to simple dropdown data
    const classData = {};
    
    // Add property classes from data
    Object.entries(propertyClasses).forEach(([code, count]) => {
        classData[code] = `${getPropertyClassName(code)} (${count})`;
    });
    
    createCheckboxFilter('class-filter', classData, 'Property Class:');
}

function getPropertyClassName(code) {
    const classNames = {
        '1010': 'Residential Single Family',
        '1020': 'Manufactured Housing',
        '1030': 'Residential Multi-Family',
        '1040': 'Residential Condominium',
        '1050': 'Residential Cooperative',
        '1060': 'Residential Other',
        '1110': 'Commercial Retail',
        '1120': 'Commercial Office',
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
    return classNames[code] || `Class ${code}`;
}