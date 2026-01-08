// Veterans Extension - Content Script
// Auto-fill SheerID Veterans verification forms for ChatGPT Plus

(function () {
    const PROGRAM_ID = '690415d58971e73ca187d8c9';
    const currentUrl = window.location.href;
    let isRunning = false;
    let currentMailtmToken = null;

    // ============ MESSAGE LISTENER FOR SIDE PANEL ============
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.action === 'startVerification') {
            isRunning = true;
            currentMailtmToken = message.mailtmToken;
            handleStartVerification(message.data);
            sendResponse({ success: true });
        } else if (message.action === 'stopVerification') {
            isRunning = false;
            sendResponse({ success: true });
        } else if (message.action === 'fillForm') {
            fillVeteranFormWithData(message.data);
            sendResponse({ success: true });
        }
        return true;
    });

    // Handle start verification from side panel
    async function handleStartVerification(data) {
        try {
            sendStatusUpdate('Filling form...', 'loading');
            await fillVeteranFormWithData(data);

            // Wait for form to be submitted and poll for email
            if (data.email && TempMailAPI.getService(data.email)) {
                sendStatusUpdate('Waiting for verification email...', 'loading');
                const token = await TempMailAPI.pollForEmail(data.email, currentMailtmToken, 20, 5000);

                if (token) {
                    sendStatusUpdate('Got token! Verifying...', 'loading');
                    // Click verify link or submit token
                    const verifyUrl = window.location.href.replace(/emailToken=\d+/, `emailToken=${token}`);
                    if (!window.location.href.includes(`emailToken=${token}`)) {
                        window.location.href = verifyUrl + (verifyUrl.includes('?') ? '&' : '?') + `emailToken=${token}`;
                    }

                    // Notify success
                    chrome.runtime.sendMessage({ action: 'verificationComplete', success: true });
                } else {
                    sendStatusUpdate('No verification email found', 'error');
                    chrome.runtime.sendMessage({ action: 'verificationComplete', success: false });
                }
            }
        } catch (e) {
            console.error('[Veterans] Error:', e);
            sendStatusUpdate('Error: ' + e.message, 'error');
            chrome.runtime.sendMessage({ action: 'verificationComplete', success: false });
        }
    }

    // Fill form with data from side panel
    async function fillVeteranFormWithData(data) {
        const fillData = {
            firstName: data.firstName,
            lastName: data.lastName,
            branch: data.branch,
            dobMonth: data.dobMonth,
            dobDay: data.dobDay,
            dobYear: data.dobYear,
            email: data.email
        };
        await fillVeteranForm(fillData);
    }

    // Send status update to side panel
    function sendStatusUpdate(status, type = 'ready') {
        try {
            chrome.runtime.sendMessage({ action: 'updateStatus', status, type });
        } catch (e) { }
    }


    // ============ TEMPMAIL API HELPERS ============
    const TempMailAPI = {
        // Detect which tempmail service based on email domain
        getService(email) {
            if (!email) return null;
            const domain = email.split('@')[1]?.toLowerCase();
            if (!domain) return null;

            // Mail.tm domains (common ones + airsworld.net)
            const mailtmDomains = ['mail.tm', 'mail.gw', 'sharklasers.com', 'guerrillamail.com', 'airsworld.net'];
            // 1secmail domains
            const secmailDomains = ['1secmail.com', '1secmail.org', '1secmail.net', 'wwjmp.com', 'esiix.com', 'xojxe.com', 'yoggm.com'];
            // tinyhost.shop domains
            const tinyhostDomains = ['tinyhost.shop', 'smartnomad.net', 'memsg.net', 'mailinator.com'];

            if (mailtmDomains.some(d => domain.includes(d))) return 'mailtm';
            if (secmailDomains.some(d => domain === d)) return '1secmail';
            if (tinyhostDomains.some(d => domain === d || domain.endsWith('.' + d))) return 'tinyhost';
            return null;
        },

        // Fetch emails from 1secmail
        async fetch1secmail(email) {
            try {
                const [login, domain] = email.split('@');
                const resp = await fetch(`https://www.1secmail.com/api/v1/?action=getMessages&login=${login}&domain=${domain}`);
                if (!resp.ok) return [];
                const messages = await resp.json();

                // Get full content of latest messages
                const emails = [];
                for (const msg of messages.slice(0, 5)) {
                    const msgResp = await fetch(`https://www.1secmail.com/api/v1/?action=readMessage&login=${login}&domain=${domain}&id=${msg.id}`);
                    if (msgResp.ok) {
                        const data = await msgResp.json();
                        emails.push({
                            id: msg.id,
                            from: data.from,
                            subject: data.subject,
                            content: data.htmlBody || data.body || ''
                        });
                    }
                }
                return emails;
            } catch (e) {
                console.error('[TempMail] 1secmail error:', e);
                if (e.message.includes('403')) {
                    console.log('[TempMail] 1secmail blocked. Please use mail.tm (Generate Email button in popup).');
                }
                return [];
            }
        },

        // Fetch emails from Mail.tm (requires account token)
        async fetchMailtm(email, token) {
            try {
                const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
                const resp = await fetch('https://api.mail.tm/messages', { headers });
                if (!resp.ok) return [];
                const data = await resp.json();
                const messages = data['hydra:member'] || [];

                const emails = [];
                for (const msg of messages.slice(0, 5)) {
                    const msgResp = await fetch(`https://api.mail.tm/messages/${msg.id}`, { headers });
                    if (msgResp.ok) {
                        const msgData = await msgResp.json();
                        let content = msgData.html || [];
                        if (Array.isArray(content)) content = content.join('');
                        emails.push({
                            id: msg.id,
                            from: msg.from?.address || '',
                            subject: msg.subject,
                            content: content
                        });
                    }
                }
                return emails;
            } catch (e) {
                console.error('[TempMail] Mail.tm error:', e);
                return [];
            }
        },

        // Fetch emails from tinyhost.shop
        async fetchTinyhost(email) {
            try {
                // tinyhost.shop API: GET /api/inbox/{email}/
                const resp = await fetch(`https://tinyhost.shop/api/inbox/${encodeURIComponent(email)}/`);
                if (!resp.ok) {
                    console.log('[TempMail] tinyhost.shop API error:', resp.status);
                    return [];
                }
                const data = await resp.json();
                const messages = data.emails || data.messages || data || [];

                const emails = [];
                for (const msg of (Array.isArray(messages) ? messages : []).slice(0, 5)) {
                    // Try to get full message content
                    let content = msg.body || msg.html || msg.text || msg.content || '';

                    // If there's a message ID, try to fetch full content
                    if (msg.id && !content) {
                        try {
                            const msgResp = await fetch(`https://tinyhost.shop/api/inbox/${encodeURIComponent(email)}/${msg.id}/`);
                            if (msgResp.ok) {
                                const msgData = await msgResp.json();
                                content = msgData.body || msgData.html || msgData.text || msgData.content || '';
                            }
                        } catch (e) {
                            console.log('[TempMail] Failed to fetch tinyhost message:', e);
                        }
                    }

                    emails.push({
                        id: msg.id || msg.uid || Date.now(),
                        from: msg.from || msg.sender || '',
                        subject: msg.subject || '',
                        content: content
                    });
                }
                return emails;
            } catch (e) {
                console.error('[TempMail] tinyhost.shop error:', e);
                return [];
            }
        },

        // Extract SheerID verification token from email content
        extractToken(content) {
            if (!content) return null;
            // Look for emailToken in URL
            const tokenMatch = content.match(/emailToken=(\d+)/i);
            if (tokenMatch) return tokenMatch[1];
            // Look for verification link
            const linkMatch = content.match(/href="([^"]*sheerid[^"]*emailToken=\d+[^"]*)"/i);
            if (linkMatch) {
                const tokenMatch2 = linkMatch[1].match(/emailToken=(\d+)/i);
                if (tokenMatch2) return tokenMatch2[1];
            }
            return null;
        },

        // Poll for verification email
        async pollForEmail(email, token, maxAttempts = 20, interval = 5000) {
            // Check storage for provider hint
            let storedProvider = null;
            try {
                const stored = await chrome.storage.local.get(['emailProvider']);
                storedProvider = stored.emailProvider;
            } catch (e) { }

            // If we have a token, it's definitely mail.tm (regardless of domain)
            // If stored provider is tinyhost, use that
            let service = token ? 'mailtm' : (storedProvider === 'tinyhost' ? 'tinyhost' : this.getService(email));

            if (!service) {
                console.log('[TempMail] Email domain not supported:', email);
                return null;
            }

            console.log(`[TempMail] Polling ${service} for verification email...`);

            for (let i = 0; i < maxAttempts; i++) {
                console.log(`[TempMail] Check ${i + 1}/${maxAttempts}...`);

                let emails = [];
                if (service === '1secmail') {
                    emails = await this.fetch1secmail(email);
                } else if (service === 'mailtm') {
                    emails = await this.fetchMailtm(email, token);
                } else if (service === 'tinyhost') {
                    emails = await this.fetchTinyhost(email);
                }

                // Look for SheerID email
                for (const mail of emails) {
                    if (mail.from?.toLowerCase().includes('sheerid') ||
                        mail.subject?.toLowerCase().includes('verification') ||
                        mail.subject?.toLowerCase().includes('openai') ||
                        mail.content?.toLowerCase().includes('sheerid')) {
                        const emailToken = this.extractToken(mail.content);
                        if (emailToken) {
                            console.log('[TempMail] Found verification token:', emailToken);
                            return emailToken;
                        }
                    }
                }

                if (i < maxAttempts - 1) {
                    await new Promise(r => setTimeout(r, interval));
                }
            }

            console.log('[TempMail] No verification email found');
            return null;
        }
    };

    // ============ EMAIL GENERATOR ============
    const EmailGenerator = {
        async generate(provider = 'mailtm') {
            try {
                if (provider === 'tinyhost') {
                    const domainResp = await fetch('https://tinyhost.shop/api/random-domains/?limit=5');
                    if (!domainResp.ok) throw new Error('Failed to get tinyhost domains');
                    const domainData = await domainResp.json();
                    const domains = domainData.domains || ['tinyhost.shop'];
                    const domain = domains[Math.floor(Math.random() * domains.length)];
                    const username = 'user' + Math.random().toString(36).substring(2, 10);
                    const email = `${username}@${domain}`;

                    return {
                        email,
                        provider: 'tinyhost',
                        tinyhostDomain: domain,
                        tinyhostUser: username
                    };
                } else {
                    // mail.tm
                    const domainResp = await fetch('https://api.mail.tm/domains');
                    if (!domainResp.ok) throw new Error('Failed to get mail.tm domains');
                    const domainData = await domainResp.json();
                    const domains = domainData['hydra:member'];
                    if (!domains || domains.length === 0) throw new Error('No mail.tm domains available');
                    const domain = domains[Math.floor(Math.random() * domains.length)].domain;

                    const username = 'user' + Math.random().toString(36).substring(7);
                    const password = Math.random().toString(36).substring(2) + 'A1!';
                    const email = `${username}@${domain}`;

                    const accResp = await fetch('https://api.mail.tm/accounts', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ address: email, password: password })
                    });
                    if (!accResp.ok) throw new Error('Failed to create mail.tm account');

                    const tokenResp = await fetch('https://api.mail.tm/token', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ address: email, password: password })
                    });
                    if (!tokenResp.ok) throw new Error('Failed to get mail.tm token');
                    const tokenData = await tokenResp.json();

                    return {
                        email,
                        provider: 'mailtm',
                        mailtmToken: tokenData.token
                    };
                }
            } catch (e) {
                console.error('[Veterans] Email generation failed:', e);
                return null;
            }
        }
    };

    // Check if plugin is enabled
    async function isPluginEnabled() {
        const stored = await chrome.storage.local.get(['pluginEnabled']);
        return stored.pluginEnabled !== false;
    }

    // ============ VETERANS-CLAIM PAGE ============
    if (window.location.pathname.includes('veterans-claim')) {
        console.log('[Veterans] Detected veterans-claim page');

        let called = false;

        async function startVerification() {
            if (called) return;
            called = true;

            if (!await isPluginEnabled()) {
                console.log('[Veterans] Extension disabled');
                return;
            }

            console.log('[Veterans] Starting verification...');

            try {
                // Get program ID from storage or use default
                const stored = await chrome.storage.local.get(['programId']);
                const programId = stored.programId || PROGRAM_ID;

                console.log('[Veterans] Using program ID:', programId);

                // Extract accessToken from page
                let accessToken = null;
                try {
                    const html = document.documentElement.innerHTML;
                    const match = html.match(/"accessToken"\s*:\s*"([^"]+)"/);
                    if (match) {
                        accessToken = match[1];
                        console.log('[Veterans] Got accessToken');
                    }
                } catch (e) {
                    console.error('[Veterans] Failed to extract accessToken:', e);
                }

                if (!accessToken) {
                    console.error('[Veterans] No accessToken found');
                    alert('Please make sure you are logged in to ChatGPT');
                    return;
                }

                // Call create_verification API
                const response = await fetch('https://chatgpt.com/backend-api/veterans/create_verification', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + accessToken
                    },
                    credentials: 'include',
                    body: JSON.stringify({ program_id: programId })
                });

                console.log('[Veterans] API response:', response.status);

                if (!response.ok) {
                    console.error('[Veterans] API failed:', response.status);
                    return;
                }

                const data = await response.json();
                const verificationId = data.verification_id;

                console.log('[Veterans] Got verification_id:', verificationId);

                if (!verificationId) {
                    console.error('[Veterans] No verification_id');
                    return;
                }

                // Redirect to SheerID
                const sheerIdUrl = `https://services.sheerid.com/verify/${programId}/?verificationId=${verificationId}`;
                console.log('[Veterans] Redirecting to:', sheerIdUrl);
                window.location.href = sheerIdUrl;

            } catch (err) {
                console.error('[Veterans] Error:', err);
            }
        }

        // Wait for page to load
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            setTimeout(startVerification, 200);
        } else {
            document.addEventListener('DOMContentLoaded', () => setTimeout(startVerification, 200));
        }
    }

    // ============ SHEERID VERIFICATION PAGE ============
    if (currentUrl.includes('services.sheerid.com/verify/')) {
        console.log('[Veterans] Detected SheerID page');

        let retrying = false;

        // Check for errors and retry
        async function checkForErrorAndRetry() {
            if (retrying) return false;

            if (!await isPluginEnabled()) {
                console.log('[Veterans] Extension disabled');
                return false;
            }

            const pageText = (document.body?.innerText || '').toLowerCase();
            const pageHtml = (document.body?.innerHTML || '').toLowerCase();

            // Check for success
            if (pageText.includes('claim your offer') ||
                pageText.includes('claim offer') ||
                pageText.includes('verification successful')) {
                console.log('[Veterans] ✅ Verification successful! Disabling extension.');
                await chrome.storage.local.set({ pluginEnabled: false });
                // Update stats
                try { chrome.runtime.sendMessage({ type: 'statsUpdate', stat: 'success' }); } catch (e) { }
                return true;
            }

            // Enhanced error detection (more patterns like eztg)
            const hasError =
                pageText.includes('verification limit exceeded') ||
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

            if (hasError) {
                retrying = true;
                console.log('[Veterans] ❌ Error detected! Moving to next entry...');
                // Update stats
                try { chrome.runtime.sendMessage({ type: 'statsUpdate', stat: 'fail' }); } catch (e) { }

                // 1. Increment Index
                const stored = await chrome.storage.local.get(['currentIndex', 'email', 'emailProvider']);
                const nextIndex = (stored.currentIndex || 0) + 1;

                // 2. Generate New Email if using TempMail
                let updates = { currentIndex: nextIndex };

                // Check if current email is temp mail
                const currentEmail = stored.email;
                const isTemp = TempMailAPI.getService(currentEmail) !== null;

                if (isTemp) {
                    console.log('[Veterans] Generating new temp email for next attempt...');
                    const provider = stored.emailProvider || 'mailtm';
                    const newEmailData = await EmailGenerator.generate(provider);
                    if (newEmailData) {
                        updates = { ...updates, ...newEmailData };
                        console.log('[Veterans] New email generated:', newEmailData.email);
                    }
                }

                await chrome.storage.local.set(updates);

                // 3. Try to click "Try Again" button first (sometimes it resets state)
                const tryAgainBtn = document.querySelector('button[type="button"]') ||
                    document.querySelector('[class*="try-again"]') ||
                    Array.from(document.querySelectorAll('button')).find(btn =>
                        btn.textContent.toLowerCase().includes('try again'));

                if (tryAgainBtn) {
                    console.log('[Veterans] Clicking Try Again button...');
                    tryAgainBtn.click();
                    await new Promise(r => setTimeout(r, 2000));
                }

                // 4. Redirect back to veterans-claim
                console.log('[Veterans] Redirecting to veterans-claim...');
                window.location.href = 'https://chatgpt.com/veterans-claim';
                return true;
            }

            return false;
        }


        // Auto-fill the form
        async function autoFillForm() {
            if (!await isPluginEnabled()) {
                console.log('[Veterans] Extension disabled');
                return;
            }

            // Wait for page to fully load before processing
            console.log('[Veterans] Waiting 1.5s for page to stabilize...');
            await new Promise(r => setTimeout(r, 1500));

            // Check for errors first
            if (await checkForErrorAndRetry()) return;

            // Get data from storage
            const stored = await chrome.storage.local.get(['inputData', 'currentIndex', 'email']);

            if (!stored.inputData) {
                console.log('[Veterans] No data saved');
                return;
            }

            const lines = stored.inputData.trim().split('\n').filter(line =>
                line.trim() && !line.toLowerCase().startsWith('first|')
            );
            const idx = stored.currentIndex || 0;

            if (!lines[idx]) {
                console.log('[Veterans] No data at index', idx);
                return;
            }

            const parts = lines[idx].split('|');
            if (parts.length < 5) {
                console.log('[Veterans] Invalid data format');
                return;
            }

            const [firstName, lastName, branch, dob, dod, batchEmail] = parts;
            const dobParts = dob.split('-');
            const dodParts = dod.split('-');

            const fillData = {
                firstName: firstName.trim(),
                lastName: lastName.trim(),
                branch: branch.trim(),
                dobMonth: parseInt(dobParts[1]),
                dobDay: parseInt(dobParts[2]),
                dobYear: dobParts[0],
                dodMonth: parseInt(dodParts[1]),
                dodDay: parseInt(dodParts[2]),
                dodYear: dodParts[0],
                email: (batchEmail && batchEmail.includes('@')) ? batchEmail.trim() : (stored.email || '')
            };

            console.log('[Veterans] Filling data:', fillData);

            // Wait for form to load
            await waitForForm();

            // Check again after form loads
            if (await checkForErrorAndRetry()) return;

            // Fill the form
            await fillVeteranForm(fillData);

            // Update index and used list
            const usedItem = `[${idx}] ${firstName} ${lastName}`;
            const usedStored = await chrome.storage.local.get(['usedItems']);
            const usedItems = usedStored.usedItems || [];
            usedItems.push(usedItem);

            // Prepare updates for NEXT successful iteration
            let updates = {
                usedItems,
                currentIndex: idx + 1
            };

            await chrome.storage.local.set(updates);
        }

        function waitForForm() {
            return new Promise((resolve) => {
                let attempts = 0;
                const maxAttempts = 100;

                const check = () => {
                    attempts++;
                    const statusInput = document.getElementById('sid-military-status');

                    if (statusInput || attempts >= maxAttempts) {
                        resolve();
                    } else {
                        setTimeout(check, 100);
                    }
                };
                check();
            });
        }

        async function fillVeteranForm(data) {
            const monthNames = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'];

            const validBranches = ['Army', 'Air Force', 'Navy', 'Marine Corps', 'Coast Guard', 'Space Force'];

            function matchBranch(input) {
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
            }

            function setInputValue(element, value) {
                element.focus();
                element.value = value;
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                element.dispatchEvent(new Event('blur', { bubbles: true }));
            }

            async function selectDropdown(inputId, searchText) {
                const input = document.getElementById(inputId);
                if (!input) {
                    console.log('[Veterans] Dropdown not found:', inputId);
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

            // 1. Select Status: Veteran
            const statusInput = document.getElementById('sid-military-status');
            if (statusInput) {
                console.log('[Veterans] Selecting status: Veteran');
                await selectDropdown('sid-military-status', 'Veteran');
                await new Promise(r => setTimeout(r, 1500));
            }

            // 2. Wait for Branch field
            let branchInput = null;
            for (let i = 0; i < 30; i++) {
                branchInput = document.getElementById('sid-branch-of-service');
                if (branchInput) break;
                await new Promise(r => setTimeout(r, 200));
            }

            // 3. Select Branch
            if (branchInput) {
                const branchValue = matchBranch(data.branch);
                console.log('[Veterans] Selecting branch:', branchValue);
                await selectDropdown('sid-branch-of-service', branchValue);
                await new Promise(r => setTimeout(r, 500));
            }

            // 4. First Name
            const firstNameInput = document.getElementById('sid-first-name');
            if (firstNameInput) setInputValue(firstNameInput, data.firstName);

            // 5. Last Name
            const lastNameInput = document.getElementById('sid-last-name');
            if (lastNameInput) setInputValue(lastNameInput, data.lastName);

            // 6. Date of Birth
            await selectDropdown('sid-birthdate__month', monthNames[data.dobMonth]);
            await new Promise(r => setTimeout(r, 300));

            const dobDay = document.getElementById('sid-birthdate-day');
            if (dobDay) setInputValue(dobDay, data.dobDay.toString());

            const dobYear = document.getElementById('sid-birthdate-year');
            if (dobYear) setInputValue(dobYear, data.dobYear);

            // 7. Discharge Date
            await selectDropdown('sid-discharge-date__month', monthNames[data.dodMonth]);
            await new Promise(r => setTimeout(r, 300));

            const dodDay = document.getElementById('sid-discharge-date-day');
            if (dodDay) setInputValue(dodDay, data.dodDay.toString());

            const dodYear = document.getElementById('sid-discharge-date-year');
            if (dodYear) setInputValue(dodYear, data.dodYear);

            // 8. Email
            if (data.email) {
                const emailInput = document.getElementById('sid-email');
                if (emailInput) setInputValue(emailInput, data.email);
            }

            // 9. Submit
            await new Promise(r => setTimeout(r, 1000));
            const submitBtn = document.getElementById('sid-submit-btn-collect-info');
            if (submitBtn) {
                console.log('[Veterans] Clicking submit...');
                submitBtn.click();

                // 10. Check if TempMail is being used - start polling for verification email
                if (data.email && TempMailAPI.getService(data.email)) {
                    console.log('[Veterans] TempMail detected, starting email poll...');

                    // Wait for page to transition to emailLoop step
                    await new Promise(r => setTimeout(r, 5000));

                    // Get Mail.tm token if stored
                    const tempMailStored = await chrome.storage.local.get(['mailtmToken']);

                    // Poll for verification email
                    const emailToken = await TempMailAPI.pollForEmail(data.email, tempMailStored.mailtmToken);

                    if (emailToken) {
                        console.log('[Veterans] Auto-submitting email token:', emailToken);

                        // Find and fill the token input
                        const tokenInput = document.querySelector('input[name*="token"], input[id*="token"], input[type="text"]');
                        if (tokenInput) {
                            setInputValue(tokenInput, emailToken);
                            await new Promise(r => setTimeout(r, 500));

                            // Click verify button
                            const verifyBtn = document.querySelector('button[type="submit"], button[id*="submit"], button[class*="submit"]');
                            if (verifyBtn) {
                                verifyBtn.click();
                                console.log('[Veterans] Token submitted!');
                            }
                        }
                    } else {
                        console.log('[Veterans] Could not find verification email. Manual check required.');
                    }
                }
            }
        }

        // Listen for manual fill command from popup
        window.addEventListener('veteransFillForm', () => {
            autoFillForm();
        });

        // Error monitoring
        function startMonitoring() {
            let lastCheck = 0;

            const observer = new MutationObserver(async () => {
                const now = Date.now();
                if (now - lastCheck < 500) return;
                lastCheck = now;

                if (!await isPluginEnabled()) {
                    observer.disconnect();
                    return;
                }

                await checkForErrorAndRetry();
            });

            if (document.body) {
                observer.observe(document.body, { childList: true, subtree: true });
            }

            setTimeout(() => observer.disconnect(), 60000);
        }

        // Start auto-fill
        if (document.readyState === 'complete') {
            setTimeout(autoFillForm, 500);
            setTimeout(startMonitoring, 1000);
        } else {
            window.addEventListener('load', () => {
                setTimeout(autoFillForm, 500);
                setTimeout(startMonitoring, 1000);
            });
        }
    }
})();
