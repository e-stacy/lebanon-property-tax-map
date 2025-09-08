// CSS Computed Style Debug Logger
// Add this to console to diagnose dropdown text alignment issues

function logDropdownStyles() {
    console.log('=== DROPDOWN CSS COMPUTED STYLES DEBUG ===');
    
    // Find the dropdown elements
    const dropdownButtons = document.querySelectorAll('.dropdown-button');
    const dropdownTexts = document.querySelectorAll('.dropdown-text');
    
    console.log(`Found ${dropdownButtons.length} dropdown buttons`);
    console.log(`Found ${dropdownTexts.length} dropdown texts`);
    
    dropdownButtons.forEach((button, index) => {
        console.log(`\n--- DROPDOWN BUTTON ${index} ---`);
        const computedButton = window.getComputedStyle(button);
        console.log('Display:', computedButton.display);
        console.log('Justify-content:', computedButton.justifyContent);
        console.log('Align-items:', computedButton.alignItems);
        console.log('Text-align:', computedButton.textAlign);
        console.log('Padding:', computedButton.padding);
        console.log('Width:', computedButton.width);
        console.log('Box-sizing:', computedButton.boxSizing);
    });
    
    dropdownTexts.forEach((text, index) => {
        console.log(`\n--- DROPDOWN TEXT ${index} ---`);
        const computedText = window.getComputedStyle(text);
        console.log('Display:', computedText.display);
        console.log('Text-align:', computedText.textAlign);
        console.log('Justify-content:', computedText.justifyContent);
        console.log('Flex-grow:', computedText.flexGrow);
        console.log('Width:', computedText.width);
        console.log('Margin:', computedText.margin);
        console.log('Padding:', computedText.padding);
        console.log('Box-sizing:', computedText.boxSizing);
        console.log('Parent classes:', text.parentElement.className);
        console.log('Element classes:', text.className);
    });
    
    // Check for conflicting CSS rules
    console.log('\n--- CONFLICTING RULES CHECK ---');
    const allStylesheets = Array.from(document.styleSheets);
    allStylesheets.forEach((sheet, sheetIndex) => {
        try {
            const rules = Array.from(sheet.cssRules || sheet.rules || []);
            const textAlignRules = rules.filter(rule => 
                rule.style && rule.style.textAlign && 
                (rule.selectorText?.includes('dropdown') || 
                 rule.selectorText?.includes('control') ||
                 rule.selectorText?.includes('button'))
            );
            if (textAlignRules.length > 0) {
                console.log(`Stylesheet ${sheetIndex} text-align rules:`, textAlignRules.map(r => ({
                    selector: r.selectorText,
                    textAlign: r.style.textAlign
                })));
            }
        } catch (e) {
            console.log(`Cannot access stylesheet ${sheetIndex}:`, e.message);
        }
    });
    
    console.log('=== END DEBUG LOG ===');
}

// Auto-run when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', logDropdownStyles);
} else {
    logDropdownStyles();
}

// Make it available globally
window.logDropdownStyles = logDropdownStyles;