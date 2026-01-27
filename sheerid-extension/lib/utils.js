// Utility Functions

const Utils = {
    // Sleep/delay function
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    // Set input value and trigger events
    setInputValue(element, value) {
        if (!element) return false;

        element.focus();
        element.value = value;

        // Trigger all necessary events
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
        element.dispatchEvent(new Event('blur', { bubbles: true }));

        return true;
    },

    // Select dropdown option by text
    async selectDropdown(inputId, searchText, maxAttempts = 20) {
        const input = document.getElementById(inputId);
        if (!input) {
            console.log('[SheerID] Dropdown not found:', inputId);
            return false;
        }

        const menuId = inputId + '-menu';
        const container = input.closest('.sid-input-select-list');
        const selectButton = container?.querySelector('.sid-input-select-button');

        // Click dropdown button
        if (selectButton) {
            selectButton.click();
        } else {
            input.click();
        }

        // Wait for options
        let options = null;
        for (let i = 0; i < maxAttempts; i++) {
            await this.sleep(100);
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
                await this.sleep(100);
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
            await this.sleep(50);
            targetOpt.click();
            await this.sleep(200);
            return true;
        }

        return false;
    },

    // Parse date string to components
    parseDate(dateStr) {
        const parts = dateStr.split('-');
        return {
            year: parts[0],
            month: parseInt(parts[1]),
            day: parseInt(parts[2])
        };
    },

    // Get month name from number
    getMonthName(monthNum) {
        const months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'];
        return months[monthNum];
    },

    // Match military branch to valid option
    matchBranch(input) {
        const validBranches = ['Army', 'Air Force', 'Navy', 'Marine Corps', 'Coast Guard', 'Space Force'];
        const normalized = input.toUpperCase().replace(/^US\s+/, '').trim();

        for (const branch of validBranches) {
            if (branch.toUpperCase() === normalized ||
                branch.toUpperCase().includes(normalized) ||
                normalized.includes(branch.toUpperCase())) {
                return branch;
            }
        }

        if (normalized.includes('MARINE')) return 'Marine Corps';
        if (normalized.includes('ARMY')) return 'Army';
        if (normalized.includes('NAVY')) return 'Navy';
        if (normalized.includes('AIR') && normalized.includes('FORCE')) return 'Air Force';
        if (normalized.includes('COAST')) return 'Coast Guard';
        if (normalized.includes('SPACE')) return 'Space Force';

        return 'Army'; // Default
    },

    // Wait for element to appear
    async waitForElement(selector, timeout = 30000) {
        const startTime = Date.now();

        while (Date.now() - startTime < timeout) {
            const element = document.querySelector(selector);
            if (element) return element;
            await this.sleep(100);
        }

        return null;
    },

    // Check if current page has error
    detectError() {
        const pageText = (document.body?.innerText || '').toLowerCase();
        const pageHtml = (document.body?.innerHTML || '').toLowerCase();

        return pageText.includes('verification limit exceeded') ||
            pageText.includes('we are unable to verify you') ||
            pageText.includes('unable to verify') ||
            pageText.includes('too many attempts') ||
            pageText.includes('try again later') ||
            pageText.includes('information does not match') ||
            pageText.includes('already been used') ||
            pageText.includes('limit exceeded') ||
            pageText.includes('not approved') ||
            pageHtml.includes('sid-error') ||
            pageHtml.includes('error-message') ||
            document.querySelector('.sid-error-message') !== null;
    },

    // Check if verification succeeded
    detectSuccess() {
        const pageText = (document.body?.innerText || '').toLowerCase();

        return pageText.includes('claim your offer') ||
            pageText.includes('claim offer') ||
            pageText.includes('verification successful') ||
            pageText.includes('you have been verified') ||
            pageText.includes('successfully verified');
    },

    // Extract verification ID from URL
    extractVerificationId(url) {
        const match = url.match(/verificationId=([a-f0-9]+)/i);
        return match ? match[1] : null;
    },

    // Extract program ID from URL
    extractProgramId(url) {
        const match = url.match(/verify\/([a-f0-9]+)/i);
        return match ? match[1] : null;
    },

    // Log with timestamp
    log(message, ...args) {
        console.log(`[SheerID ${new Date().toLocaleTimeString()}]`, message, ...args);
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Utils;
}
