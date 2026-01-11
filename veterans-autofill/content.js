// Veterans Autofill - Content Script
// Auto-fill SheerID Veterans verification forms

(function () {
    if (!window.location.href.includes('services.sheerid.com')) return;

    console.log('[VeteransAutofill] Content script loaded');

    const monthNames = ['', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'];

    // Set input value with events
    function setInputValue(element, value) {
        if (!element) return;
        element.focus();
        element.value = value;
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
        element.dispatchEvent(new Event('blur', { bubbles: true }));
    }

    // Select dropdown option
    async function selectDropdown(inputId, searchText) {
        const input = document.getElementById(inputId);
        if (!input) {
            console.log('[VeteransAutofill] Dropdown not found:', inputId);
            return false;
        }

        const menuId = inputId + '-menu';
        const container = input.closest('.sid-input-select-list');
        const selectButton = container?.querySelector('.sid-input-select-button');

        // Click dropdown
        if (selectButton) {
            selectButton.click();
        } else {
            input.click();
        }

        // Wait for options
        let options = null;
        for (let i = 0; i < 20; i++) {
            await new Promise(r => setTimeout(r, 100));
            const menu = document.getElementById(menuId);
            options = menu?.querySelectorAll('[role="option"]');
            if (options && options.length > 0) break;
        }

        if (!options || options.length === 0) {
            // Fallback: type to search
            input.focus();
            input.value = searchText;
            input.dispatchEvent(new Event('input', { bubbles: true }));

            for (let i = 0; i < 10; i++) {
                await new Promise(r => setTimeout(r, 100));
                const menu = document.getElementById(menuId);
                options = menu?.querySelectorAll('[role="option"]');
                if (options && options.length > 0) break;
            }
        }

        // Click matching option
        if (options && options.length > 0) {
            const searchLower = searchText.toLowerCase();
            let targetOpt = null;

            for (const opt of options) {
                const optText = opt.textContent.trim().toLowerCase();
                if (optText === searchLower || optText.includes(searchLower) || searchLower.includes(optText)) {
                    targetOpt = opt;
                    break;
                }
            }

            if (!targetOpt) targetOpt = options[0];

            targetOpt.scrollIntoView({ block: 'nearest' });
            await new Promise(r => setTimeout(r, 50));
            targetOpt.click();
            await new Promise(r => setTimeout(r, 200));
            return true;
        }

        return false;
    }

    // Fill the veteran form
    async function fillVeteranForm(data) {
        console.log('[VeteransAutofill] Filling form with:', data);

        // Parse dates
        const dobParts = data.dob ? data.dob.split('-') : [];
        const dodParts = data.dischargeDate ? data.dischargeDate.split('-') : [];

        // 1. Wait for form to load
        let statusInput = null;
        for (let i = 0; i < 50; i++) {
            statusInput = document.getElementById('sid-military-status');
            if (statusInput) break;
            await new Promise(r => setTimeout(r, 200));
        }

        if (!statusInput) {
            console.log('[VeteransAutofill] Form not found');
            return;
        }

        // 2. Select Status: Veteran
        console.log('[VeteransAutofill] Selecting status: Veteran');
        await selectDropdown('sid-military-status', 'Veteran');
        await new Promise(r => setTimeout(r, 1500));

        // 3. Wait for Branch field
        let branchInput = null;
        for (let i = 0; i < 30; i++) {
            branchInput = document.getElementById('sid-branch-of-service');
            if (branchInput) break;
            await new Promise(r => setTimeout(r, 200));
        }

        // 4. Select Branch
        if (branchInput && data.branch) {
            console.log('[VeteransAutofill] Selecting branch:', data.branch);
            await selectDropdown('sid-branch-of-service', data.branch);
            await new Promise(r => setTimeout(r, 500));
        }

        // 5. First Name
        const firstNameInput = document.getElementById('sid-first-name');
        if (firstNameInput && data.firstName) {
            setInputValue(firstNameInput, data.firstName);
        }

        // 6. Last Name
        const lastNameInput = document.getElementById('sid-last-name');
        if (lastNameInput && data.lastName) {
            setInputValue(lastNameInput, data.lastName);
        }

        // 7. Date of Birth
        if (dobParts.length === 3) {
            await selectDropdown('sid-birthdate__month', monthNames[parseInt(dobParts[1])]);
            await new Promise(r => setTimeout(r, 300));

            const dobDay = document.getElementById('sid-birthdate-day');
            if (dobDay) setInputValue(dobDay, parseInt(dobParts[2]).toString());

            const dobYear = document.getElementById('sid-birthdate-year');
            if (dobYear) setInputValue(dobYear, dobParts[0]);
        }

        // 8. Discharge Date
        if (dodParts.length === 3) {
            await selectDropdown('sid-discharge-date__month', monthNames[parseInt(dodParts[1])]);
            await new Promise(r => setTimeout(r, 300));

            const dodDay = document.getElementById('sid-discharge-date-day');
            if (dodDay) setInputValue(dodDay, parseInt(dodParts[2]).toString());

            const dodYear = document.getElementById('sid-discharge-date-year');
            if (dodYear) setInputValue(dodYear, dodParts[0]);
        }

        // 9. Email
        if (data.email) {
            const emailInput = document.getElementById('sid-email');
            if (emailInput) setInputValue(emailInput, data.email);
        }

        console.log('[VeteransAutofill] Form filled!');
    }

    // Listen for messages from popup
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.type === 'FILL_FORM') {
            fillVeteranForm(message.data).then(() => {
                sendResponse({ success: true });
            }).catch(e => {
                console.error('[VeteransAutofill] Fill error:', e);
                sendResponse({ success: false, error: e.message });
            });
            return true; // Keep channel open for async response
        }
    });

    console.log('[VeteransAutofill] Ready');
})();
