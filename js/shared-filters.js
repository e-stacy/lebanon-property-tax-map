// Shared filtering logic for Lebanon Property Tax Database
// Used by both main table page and map page

// Lebanon property class codes and hierarchy
const lebanonClassCodes = ['1010', '1012', '1015', '1020', '1030', '1040', '1050', '1060', '1070', '1080', '1081', '1090', '1100', '1110', '1200', '1300', '1310', '1320', '1330', '1340', '1350', '1360', '1370', '1380', '1390', '1400', '1410', '1420', '1430', '1440', '1450', '1460', '1470', '1480', '1490', '1500', '1510', '1520', '1530', '1540', '1550', '1560', '1570', '1580', '1590', '1600', '1700', '1800', '1900', '3010', '3020', '3100', '3200', '3210', '3220', '3230', '3240', '3250', '3260', '3270', '3280', '3290', '3300', '3310', '3320', '3330', '3340', '3350', '3360', '3370', '3380', '3390', '3400', '3410', '3420', '3430', '3440', '3450', '3460', '3470', '3480', '3490', '3500', '3510', '3520', '3530', '3540', '3550', '3560', '3570', '3580', '3590', '3600', '3610', '3620', '3630', '3640', '3650', '3660', '3670', '3680', '3690', '3700', '3710', '3720', '3730', '3740', '3750', '3760', '3770', '3780', '3790', '3800', '3810', '3820', '3830', '3840', '3850', '3860', '3870', '3880', '3890', '3900', '3910', '3920', '3930', '3940', '3950', '3960', '3970', '3980', '3990', '4000', '4010', '4020', '4030', '4040', '4050', '4060', '4070', '4080', '4090', '4100', '4110', '4120', '4130', '4140', '4150', '4160', '4170', '4180', '4190', '4200', '4210', '4220', '4230', '4240', '4250', '4260', '4270', '4280', '4290', '4300', '4310', '4320', '4330', '4340', '4350', '4360', '4370', '4380', '4390', '4400', '4500', '4600', '4700', '4800', '4900', '5000', '5100', '5200', '5300', '5400', '5500', '5600', '5700', '5800', '5900', '6000', '6100', '6200', '6300', '6400', '6500', '6600', '6700', '6800', '6900', '7000', '7100', '7200', '7300', '7400', '7500', '7600', '7700', '7800', '7900', '8000', '8100', '8200', '8300', '8400', '8500', '8600', '8700', '8800', '8900', '9000', '9100', '9200', '9300', '9400', '9500', '9600', '9700', '9800', '9900', '101A', '101B', '101C', '101T', '105A', '105B'];

// Property class hierarchy with descriptions
const propertyClassHierarchy = {
    '1010': { name: 'Single-Family Res', primary: true, subclasses: ['1012', '101A', '101C', '101T'] },
    '1012': { name: 'Single-Family Res (Low Income)', primary: false },
    '101A': { name: 'Single-Family Res (Accessory Dwelling)', primary: false },
    '101C': { name: 'Single-Family Res (Condo)', primary: false },
    '101T': { name: 'Single-Family Res (Townhouse)', primary: false },
    '1015': { name: 'Single-Family Res (2 Units)', primary: true },
    '1020': { name: 'Multi-Family Res (3-4 Units)', primary: true },
    '1030': { name: 'Multi-Family Res (5+ Units)', primary: true },
    '1040': { name: 'Multi-Family Res (Condo)', primary: true },
    '1050': { name: 'Manufactured Housing', primary: true, subclasses: ['105A', '105B'] },
    '105A': { name: 'Manufactured Housing (on owned land)', primary: false },
    '105B': { name: 'Manufactured Housing (on rented land)', primary: false },
    '1060': { name: 'Rooming/Boarding House', primary: true },
    '1070': { name: 'Hotel/Motel/Inn', primary: true },
    '1080': { name: 'Nursing Home', primary: true },
    '1081': { name: 'Assisted Living', primary: true },
    '1090': { name: 'Other Residential', primary: true },
    '1100': { name: 'Vacant Residential', primary: true },
    '1110': { name: 'Conservation/Recreation', primary: true },
    '1200': { name: 'Neighborhood Commercial', primary: true },
    '1300': { name: 'Retail', primary: true },
    '1310': { name: 'Shopping Center', primary: true },
    '1320': { name: 'Office', primary: true },
    '1330': { name: 'Bank', primary: true },
    '1340': { name: 'Hotel/Motel', primary: true },
    '1350': { name: 'Restaurant', primary: true },
    '1360': { name: 'Auto Sales/Service', primary: true },
    '1370': { name: 'Gas Station', primary: true },
    '1380': { name: 'Parking', primary: true },
    '1390': { name: 'Other Commercial', primary: true },
    '1400': { name: 'Industrial Light', primary: true },
    '1410': { name: 'Industrial Heavy', primary: true },
    '1420': { name: 'Warehouse', primary: true },
    '1430': { name: 'Mill/Factory', primary: true },
    '1440': { name: 'Research/Development', primary: true },
    '1450': { name: 'Mining/Quarrying', primary: true },
    '1460': { name: 'Agricultural Processing', primary: true },
    '1470': { name: 'Utility', primary: true },
    '1480': { name: 'Industrial Condo', primary: true },
    '1490': { name: 'Other Industrial', primary: true }
};

// Global filter state
let selectedFilters = { class: [], year: [], zone: [] };
let openDropdown = null;

// Utility functions
function parseNumber(value) {
    if (value === null || value === undefined || value === '') return 0;
    const parsed = parseFloat(value);
    return isNaN(parsed) ? 0 : parsed;
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(0) + 'K';
    }
    return num.toString();
}

function formatCurrency(value) {
    const num = parseNumber(value);
    if (num === 0) return '$0';
    return '$' + num.toLocaleString();
}

// Get primary property classes
function getPrimaryClasses() {
    return Object.entries(propertyClassHierarchy)
        .filter(([code, info]) => info.primary)
        .map(([code, info]) => ({ code, name: info.name }));
}

// Check if parcel matches hierarchical class filters
function matchesClassFilter(parcel, selectedClasses) {
    if (selectedClasses.length === 0) return true;
    
    const parcelClass = parcel.class_code;
    if (selectedClasses.includes(parcelClass)) return true;
    
    // Check if parcel class is a subclass of any selected primary class
    for (const selectedClass of selectedClasses) {
        const classInfo = propertyClassHierarchy[selectedClass];
        if (classInfo && classInfo.subclasses && classInfo.subclasses.includes(parcelClass)) {
            return true;
        }
    }
    
    return false;
}

// Dropdown functions
function toggleDropdown(type) {
    const menu = document.getElementById(type + '-menu');
    const button = document.querySelector('#' + type + '-dropdown .dropdown-button');
    
    // Close any other open dropdown
    if (openDropdown && openDropdown !== type) {
        closeDropdown(openDropdown);
    }
    
    if (menu.style.display === 'block') {
        closeDropdown(type);
    } else {
        openDropdownMenu(type);
    }
}

function openDropdownMenu(type) {
    const menu = document.getElementById(type + '-menu');
    const button = document.querySelector('#' + type + '-dropdown .dropdown-button');
    const rect = button.getBoundingClientRect();
    const footer = document.querySelector('.pagination');
    const footerRect = footer.getBoundingClientRect();
    
    menu.style.display = 'block';
    menu.style.top = (rect.bottom + window.scrollY) + 'px';
    menu.style.left = rect.left + 'px';
    menu.style.width = rect.width + 'px';
    menu.style.maxHeight = Math.max(200, footerRect.top - rect.bottom - 20) + 'px';
    
    button.classList.add('active');
    openDropdown = type;
}

function closeDropdown(type) {
    const menu = document.getElementById(type + '-menu');
    const button = document.querySelector('#' + type + '-dropdown .dropdown-button');
    
    menu.style.display = 'none';
    button.classList.remove('active');
    if (openDropdown === type) {
        openDropdown = null;
    }
}

// Update dropdown text based on selections
function updateDropdownText(type) {
    const textElement = document.getElementById(type + '-text');
    const selected = selectedFilters[type];
    
    if (selected.length === 0) {
        let defaultText = 'All Classes';
        if (type === 'year') defaultText = 'All Years';
        if (type === 'zone') defaultText = 'All Zones';
        
        textElement.textContent = defaultText;
        textElement.style.color = '#666';
    } else if (selected.length === 1) {
        if (type === 'class' && propertyClassHierarchy[selected[0]]) {
            textElement.textContent = selected[0] + ' - ' + propertyClassHierarchy[selected[0]].name;
        } else {
            textElement.textContent = selected[0];
        }
        textElement.style.color = '#333';
    } else {
        textElement.textContent = selected.length + ' selected';
        textElement.style.color = '#333';
    }
}

// Handle dropdown selection with hierarchical logic
function handleDropdownSelection(type, value, checked) {
    const menu = document.getElementById(type + '-menu');
    const allCheckbox = document.getElementById(type + '-all');
    
    if (value === '') {
        // "All" option selected
        if (checked) {
            // Uncheck all other options and clear the array
            const otherCheckboxes = menu.querySelectorAll('input[type="checkbox"]:not(#' + type + '-all)');
            otherCheckboxes.forEach(cb => cb.checked = false);
            selectedFilters[type] = [];
        } else {
            // "All" unchecked, keep current selections
        }
    } else {
        // Specific option selected
        if (checked) {
            // Uncheck "All" option first
            if (allCheckbox) allCheckbox.checked = false;
            
            // Check if this is a primary class with subclasses
            const classInfo = propertyClassHierarchy[value];
            if (classInfo && classInfo.primary && classInfo.subclasses) {
                // Primary class selected - add it and all its subclasses
                if (!selectedFilters[type].includes(value)) {
                    selectedFilters[type].push(value);
                }
                classInfo.subclasses.forEach(subclass => {
                    if (!selectedFilters[type].includes(subclass)) {
                        selectedFilters[type].push(subclass);
                        // Check the corresponding checkbox
                        const subCheckbox = document.getElementById(type + '-' + subclass);
                        if (subCheckbox) subCheckbox.checked = true;
                    }
                });
            } else {
                // Regular selection or subclass
                if (!selectedFilters[type].includes(value)) {
                    selectedFilters[type].push(value);
                }
            }
        } else {
            // Option unchecked
            const index = selectedFilters[type].indexOf(value);
            if (index > -1) {
                selectedFilters[type].splice(index, 1);
            }
            
            // If this was a primary class, also uncheck its subclasses
            const classInfo = propertyClassHierarchy[value];
            if (classInfo && classInfo.primary && classInfo.subclasses) {
                classInfo.subclasses.forEach(subclass => {
                    const subIndex = selectedFilters[type].indexOf(subclass);
                    if (subIndex > -1) {
                        selectedFilters[type].splice(subIndex, 1);
                        const subCheckbox = document.getElementById(type + '-' + subclass);
                        if (subCheckbox) subCheckbox.checked = false;
                    }
                });
            }
            
            // If this was a subclass and now no subclasses are selected, uncheck the parent
            if (classInfo && !classInfo.primary) {
                const parentClass = Object.entries(propertyClassHierarchy)
                    .find(([code, info]) => info.subclasses && info.subclasses.includes(value));
                if (parentClass) {
                    const [parentCode, parentInfo] = parentClass;
                    const hasSelectedSubclasses = parentInfo.subclasses.some(sub => 
                        selectedFilters[type].includes(sub));
                    
                    if (!hasSelectedSubclasses && selectedFilters[type].includes(parentCode)) {
                        const parentIndex = selectedFilters[type].indexOf(parentCode);
                        selectedFilters[type].splice(parentIndex, 1);
                        const parentCheckbox = document.getElementById(type + '-' + parentCode);
                        if (parentCheckbox) parentCheckbox.checked = false;
                    }
                }
            }
        }
        
        // Check "All" if no items selected
        if (selectedFilters[type].length === 0 && allCheckbox) {
            allCheckbox.checked = true;
        }
    }
    
    updateDropdownText(type);
    // Apply filters will be called by the parent page
    if (typeof applyFilters === 'function') {
        applyFilters();
    }
}

// CSV parsing function for consistency
function parseCSVLine(line) {
    const result = [];
    let current = '';
    let inQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
        const char = line[i];
        
        if (char === '"') {
            inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
            result.push(current.trim());
            current = '';
        } else {
            current += char;
        }
    }
    result.push(current.trim());
    return result;
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(e) {
    if (openDropdown && !e.target.closest('.custom-dropdown')) {
        closeDropdown(openDropdown);
    }
});