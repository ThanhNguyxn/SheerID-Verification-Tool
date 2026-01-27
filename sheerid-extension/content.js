// SheerID Extension - Content Script
// Unified verification handler for all services

(async function() {
    'use strict';

    const SHEERID_API_URL = "https://services.sheerid.com/rest/v2";
    const currentUrl = window.location.href;
    let isRunning = false;

    Utils.log('Content script loaded');

    // Check if extension is enabled
    async function isPluginEnabled() {
        const stored = await chrome.storage.local.get(['pluginEnabled']);
        return stored.pluginEnabled !== false;
    }

    // Get current configuration
    async function getConfig() {
        return await chrome.storage.local.get([
            'serviceType', 'programId', 'email', 'veteransData', 'autoMode'
        ]);
    }

    // Update statistics
    async function updateStats(type) {
        try {
            chrome.runtime.sendMessage({ type: 'statsUpdate', stat: type });
        } catch (e) {
            Utils.log('Stats update failed:', e);
        }
    }

    // Select random university
    function selectUniversity() {
        if (typeof UNIVERSITIES === 'undefined' || !UNIVERSITIES.length) {
            Utils.log('UNIVERSITIES not loaded');
            return null;
        }

        // Weighted random selection
        const totalWeight = UNIVERSITIES.reduce((sum, uni) => sum + uni.weight, 0);
        let random = Math.random() * totalWeight;

        for (const uni of UNIVERSITIES) {
            random -= uni.weight;
            if (random <= 0) {
                return { ...uni, idExtended: String(uni.id) };
            }
        }

        return { ...UNIVERSITIES[0], idExtended: String(UNIVERSITIES[0].id) };
    }

    // Select random school (K12)
    function selectK12School() {
        if (typeof K12_SCHOOLS === 'undefined' || !K12_SCHOOLS.length) {
            return null;
        }
        return K12_SCHOOLS[Math.floor(Math.random() * K12_SCHOOLS.length)];
    }

    // Generate student verification data
    function generateStudentData(serviceType, customEmail = null) {
        const name = AntiDetect.generateName();
        const university = selectUniversity();

        if (!university) {
            throw new Error('No universities available');
        }

        const email = customEmail || AntiDetect.generateEmail(name.first, name.last, university.domain);
        const birthDate = AntiDetect.generateBirthDate();

        return {
            firstName: name.first,
            lastName: name.last,
            organization: university,
            email: email,
            birthDate: birthDate,
            phoneNumber: ""
        };
    }

    // Generate teacher verification data
    function generateTeacherData(serviceType, customEmail = null) {
        const name = AntiDetect.generateName();
        const university = selectUniversity();

        if (!university) {
            throw new Error('No universities available');
        }

        // Teachers are older (25-55 years)
        const birthDate = AntiDetect.generateBirthDate(25, 55);
        const email = customEmail || AntiDetect.generateEmail(name.first, name.last, university.domain);

        return {
            firstName: name.first,
            lastName: name.last,
            organization: university,
            email: email,
            birthDate: birthDate,
            phoneNumber: ""
        };
    }

    // Generate K12 teacher data
    function generateK12Data(customEmail = null) {
        const name = AntiDetect.generateName();
        const school = selectK12School();

        if (!school) {
            throw new Error('No K12 schools available');
        }

        const birthDate = AntiDetect.generateBirthDate(25, 55);
        const email = customEmail || `${name.first.toLowerCase()}.${name.last.toLowerCase()}@school.edu`;

        return {
            firstName: name.first,
            lastName: name.last,
            organization: school,
            email: email,
            birthDate: birthDate,
            phoneNumber: "",
            jobTitle: "Teacher"
        };
    }

    // Fill SheerID form based on service type
    async function fillSheerIDForm(config) {
        if (!await isPluginEnabled()) {
            Utils.log('Extension disabled');
            return false;
        }

        const serviceType = config.serviceType || 'spotify';
        Utils.log('Filling form for service:', serviceType);

        try {
            // Wait for form to load
            await Utils.sleep(2000);

            // Check for errors first
            if (Utils.detectError()) {
                Utils.log('Error detected on page');
                await handleError();
                return false;
            }

            // Check for success
            if (Utils.detectSuccess()) {
                Utils.log('Already verified!');
                updateStats('success');
                await chrome.storage.local.set({ pluginEnabled: false });
                return true;
            }

            let data;

            // Generate data based on service type
            if (serviceType === 'veterans') {
                // Veterans requires manual data
                return await fillVeteransForm(config);
            } else if (serviceType === 'k12') {
                data = generateK12Data(config.email);
            } else if (serviceType === 'boltnew' || serviceType === 'canva') {
                data = generateTeacherData(serviceType, config.email);
            } else {
                // Student verification (spotify, youtube, googleone, perplexity, cursor)
                data = generateStudentData(serviceType, config.email);
            }

            Utils.log('Generated data:', data);

            // Fill the form based on current step
            await fillFormFields(data, serviceType);

            return true;

        } catch (error) {
            Utils.log('Error filling form:', error);
            updateStats('fail');
            return false;
        }
    }

    // Fill form fields
    async function fillFormFields(data, serviceType) {
        // Wait for form
        await Utils.sleep(1000);

        // Country field (if exists)
        const countryField = document.getElementById('sid-country');
        if (countryField) {
            Utils.log('Selecting country...');
            await Utils.selectDropdown('sid-country', 'United States');
            await Utils.sleep(500);
        }

        // Organization/School search - try multiple selectors
        let orgInput = document.getElementById('sid-organization-search') ||
                       document.getElementById('sid-school-search') ||
                       document.querySelector('input[placeholder*="school" i]') ||
                       document.querySelector('input[placeholder*="university" i]') ||
                       document.querySelector('input[name*="organization"]') ||
                       document.querySelector('input[name*="school"]');

        if (!orgInput) {
            // Try finding by label text
            const labels = Array.from(document.querySelectorAll('label'));
            const schoolLabel = labels.find(label =>
                label.textContent.toLowerCase().includes('school') ||
                label.textContent.toLowerCase().includes('university') ||
                label.textContent.toLowerCase().includes('organization')
            );
            if (schoolLabel) {
                const labelFor = schoolLabel.getAttribute('for');
                if (labelFor) {
                    orgInput = document.getElementById(labelFor);
                } else {
                    orgInput = schoolLabel.nextElementSibling?.querySelector('input');
                }
            }
        }

        if (orgInput && data.organization) {
            Utils.log('Found school field:', orgInput.id || orgInput.name || 'no-id');
            Utils.log('Filling organization:', data.organization.name);

            // Focus and clear first
            orgInput.focus();
            orgInput.value = '';
            await Utils.sleep(200);

            // Type the school name
            orgInput.value = data.organization.name;
            orgInput.dispatchEvent(new Event('input', { bubbles: true }));
            orgInput.dispatchEvent(new Event('change', { bubbles: true }));
            orgInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));

            // Wait for results dropdown to appear
            Utils.log('Waiting for results dropdown...');
            await Utils.sleep(2000);

            // Try multiple selectors for results
            let result = document.querySelector('[role="option"]') ||
                        document.querySelector('.sid-search-result') ||
                        document.querySelector('[class*="option"]') ||
                        document.querySelector('[class*="result"]') ||
                        document.querySelector('li[tabindex]');

            if (result) {
                Utils.log('Found result, clicking...');
                result.click();
                await Utils.sleep(800);
            } else {
                Utils.log('No dropdown results found - field may have autocompleted');
                // Try pressing Enter to confirm
                orgInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
                await Utils.sleep(500);
            }
        } else {
            Utils.log('School field not found or no organization data');
        }

        // First name
        const firstNameInput = document.getElementById('sid-first-name');
        if (firstNameInput) {
            Utils.setInputValue(firstNameInput, data.firstName);
        }

        // Last name
        const lastNameInput = document.getElementById('sid-last-name');
        if (lastNameInput) {
            Utils.setInputValue(lastNameInput, data.lastName);
        }

        // Date of birth
        if (data.birthDate) {
            const dobParts = Utils.parseDate(data.birthDate);

            // Month
            await Utils.selectDropdown('sid-birthdate__month', Utils.getMonthName(dobParts.month));
            await Utils.sleep(300);

            // Day
            const dobDay = document.getElementById('sid-birthdate-day');
            if (dobDay) Utils.setInputValue(dobDay, dobParts.day.toString());

            // Year
            const dobYear = document.getElementById('sid-birthdate-year');
            if (dobYear) Utils.setInputValue(dobYear, dobParts.year);
        }

        // Email
        if (data.email) {
            const emailInput = document.getElementById('sid-email');
            if (emailInput) Utils.setInputValue(emailInput, data.email);
        }

        // Job title (for teachers)
        if (data.jobTitle) {
            const jobInput = document.getElementById('sid-job-title');
            if (jobInput) Utils.setInputValue(jobInput, data.jobTitle);
        }

        // Submit the form
        await Utils.sleep(1000);
        const submitBtn = document.getElementById('sid-submit-btn-collect-info') ||
                         document.querySelector('button[type="submit"]');

        if (submitBtn && !submitBtn.disabled) {
            Utils.log('Submitting form...');
            submitBtn.click();

            // Wait for response
            await Utils.sleep(3000);

            // Check result
            if (Utils.detectSuccess()) {
                Utils.log('Success!');
                updateStats('success');
                return true;
            } else if (Utils.detectError()) {
                Utils.log('Error after submission');
                updateStats('fail');
                await handleError();
                return false;
            } else {
                Utils.log('Form submitted, waiting for review...');
                updateStats('skip');
                return true;
            }
        }
    }

    // Fill veterans form (special handling)
    async function fillVeteransForm(config) {
        if (!config.veteransData) {
            Utils.log('No veterans data provided');
            return false;
        }

        const lines = config.veteransData.trim().split('\n').filter(line =>
            line.trim() && !line.toLowerCase().startsWith('first|')
        );

        if (!lines.length) {
            Utils.log('No valid veterans data');
            return false;
        }

        const parts = lines[0].split('|');
        if (parts.length < 5) {
            Utils.log('Invalid veterans data format');
            return false;
        }

        const [firstName, lastName, branch, dob, dischargeDate] = parts;
        const dobParts = Utils.parseDate(dob);
        const dischargeParts = Utils.parseDate(dischargeDate);

        const data = {
            firstName: firstName.trim(),
            lastName: lastName.trim(),
            branch: Utils.matchBranch(branch.trim()),
            dobMonth: dobParts.month,
            dobDay: dobParts.day,
            dobYear: dobParts.year,
            dodMonth: dischargeParts.month,
            dodDay: dischargeParts.day,
            dodYear: dischargeParts.year,
            email: config.email || parts[5]?.trim() || ''
        };

        Utils.log('Filling veterans form:', data);

        // Select status
        const statusInput = document.getElementById('sid-military-status');
        if (statusInput) {
            Utils.log('Selecting status: Veteran');
            await Utils.selectDropdown('sid-military-status', 'Veteran');
            await Utils.sleep(1500);
        }

        // Wait for branch field
        await Utils.waitForElement('#sid-branch-of-service', 10000);

        // Select branch
        await Utils.selectDropdown('sid-branch-of-service', data.branch);
        await Utils.sleep(500);

        // First name
        const firstNameInput = document.getElementById('sid-first-name');
        if (firstNameInput) Utils.setInputValue(firstNameInput, data.firstName);

        // Last name
        const lastNameInput = document.getElementById('sid-last-name');
        if (lastNameInput) Utils.setInputValue(lastNameInput, data.lastName);

        // Date of birth
        await Utils.selectDropdown('sid-birthdate__month', Utils.getMonthName(data.dobMonth));
        await Utils.sleep(300);

        const dobDay = document.getElementById('sid-birthdate-day');
        if (dobDay) Utils.setInputValue(dobDay, data.dobDay.toString());

        const dobYear = document.getElementById('sid-birthdate-year');
        if (dobYear) Utils.setInputValue(dobYear, data.dobYear);

        // Discharge date
        await Utils.selectDropdown('sid-discharge-date__month', Utils.getMonthName(data.dodMonth));
        await Utils.sleep(300);

        const dodDay = document.getElementById('sid-discharge-date-day');
        if (dodDay) Utils.setInputValue(dodDay, data.dodDay.toString());

        const dodYear = document.getElementById('sid-discharge-date-year');
        if (dodYear) Utils.setInputValue(dodYear, data.dodYear);

        // Email
        if (data.email) {
            const emailInput = document.getElementById('sid-email');
            if (emailInput) Utils.setInputValue(emailInput, data.email);
        }

        // Submit
        await Utils.sleep(1000);
        const submitBtn = document.getElementById('sid-submit-btn-collect-info');
        if (submitBtn) {
            Utils.log('Submitting veterans form...');
            submitBtn.click();
        }

        return true;
    }

    // Handle errors and retry
    async function handleError() {
        Utils.log('Handling error...');

        // Click "Try Again" if available
        const tryAgainBtn = document.querySelector('button[type="button"]') ||
                           document.querySelector('[class*="try-again"]') ||
                           Array.from(document.querySelectorAll('button')).find(btn =>
                               btn.textContent.toLowerCase().includes('try again'));

        if (tryAgainBtn) {
            Utils.log('Clicking Try Again button...');
            tryAgainBtn.click();
            await Utils.sleep(2000);
        }

        // If auto mode, retry
        const config = await getConfig();
        if (config.autoMode) {
            Utils.log('Auto mode: retrying...');
            await Utils.sleep(2000);
            window.location.reload();
        }
    }

    // Handle ChatGPT veterans-claim page
    if (currentUrl.includes('chatgpt.com') && currentUrl.includes('veterans-claim')) {
        Utils.log('Detected ChatGPT veterans-claim page');

        let called = false;

        async function startVeteransVerification() {
            if (called || !await isPluginEnabled()) return;
            called = true;

            Utils.log('Starting veterans verification...');

            try {
                const config = await getConfig();
                const programId = config.programId || '690415d58971e73ca187d8c9';

                // Extract accessToken
                const html = document.documentElement.innerHTML;
                const match = html.match(/"accessToken"\s*:\s*"([^"]+)"/);

                if (!match) {
                    Utils.log('No accessToken found');
                    return;
                }

                const accessToken = match[1];

                // Create verification
                const response = await fetch('https://chatgpt.com/backend-api/veterans/create_verification', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + accessToken
                    },
                    credentials: 'include',
                    body: JSON.stringify({ program_id: programId })
                });

                if (!response.ok) {
                    Utils.log('API failed:', response.status);
                    return;
                }

                const data = await response.json();
                const verificationId = data.verification_id;

                if (!verificationId) {
                    Utils.log('No verification_id');
                    return;
                }

                // Redirect to SheerID
                const sheerIdUrl = `https://services.sheerid.com/verify/${programId}/?verificationId=${verificationId}`;
                Utils.log('Redirecting to:', sheerIdUrl);
                window.location.href = sheerIdUrl;

            } catch (err) {
                Utils.log('Error:', err);
            }
        }

        // Wait for page load
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            setTimeout(startVeteransVerification, 200);
        } else {
            document.addEventListener('DOMContentLoaded', () => setTimeout(startVeteransVerification, 200));
        }
    }

    // Handle SheerID verification page
    if (currentUrl.includes('services.sheerid.com/verify/')) {
        Utils.log('Detected SheerID verification page');

        let autoFillCalled = false;

        async function autoFillForm() {
            if (autoFillCalled || !await isPluginEnabled()) return;
            autoFillCalled = true;

            Utils.log('Auto-filling form...');

            // Wait for page to stabilize
            await Utils.sleep(1500);

            // Get configuration
            const config = await getConfig();

            // Fill form
            await fillSheerIDForm(config);
        }

        // Listen for manual fill command
        window.addEventListener('sheeridFillForm', () => {
            autoFillCalled = false;
            autoFillForm();
        });

        // Listen for auto run command
        window.addEventListener('sheeridAutoRun', async () => {
            await chrome.storage.local.set({ autoMode: true });
            autoFillCalled = false;
            autoFillForm();
        });

        // Start auto-fill on page load
        if (document.readyState === 'complete') {
            setTimeout(autoFillForm, 500);
        } else {
            window.addEventListener('load', () => setTimeout(autoFillForm, 500));
        }

        // Monitor for errors
        const observer = new MutationObserver(async () => {
            if (!await isPluginEnabled()) {
                observer.disconnect();
                return;
            }

            if (Utils.detectError()) {
                Utils.log('Error detected by observer');
                await handleError();
            } else if (Utils.detectSuccess()) {
                Utils.log('Success detected by observer');
                updateStats('success');
                await chrome.storage.local.set({ pluginEnabled: false });
                observer.disconnect();
            }
        });

        if (document.body) {
            observer.observe(document.body, { childList: true, subtree: true });
        }
    }

    Utils.log('Content script ready');

})();
