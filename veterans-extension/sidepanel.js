// Veterans Extension - Side Panel Script
// Handles UI interactions and communicates with content.js

(function () {
    const $ = id => document.getElementById(id);

    // UI Elements
    const ui = {
        successCount: $('successCount'),
        failCount: $('failCount'),
        skipCount: $('skipCount'),
        indexNum: $('indexNum'),
        indexUp: $('indexUp'),
        indexDown: $('indexDown'),
        currentEntry: $('currentEntry'),
        emailProvider: $('emailProvider'),
        emailInput: $('emailInput'),
        genEmailBtn: $('genEmailBtn'),
        batchData: $('batchData'),
        startBtn: $('startBtn'),
        stopBtn: $('stopBtn'),
        skipBtn: $('skipBtn'),
        fillBtn: $('fillBtn'),
        clearCookiesBtn: $('clearCookiesBtn'),
        downloadLogBtn: $('downloadLogBtn'),
        statusBar: $('statusBar'),
        statusText: $('statusText')
    };

    // State
    let state = {
        isRunning: false,
        currentIndex: 0,
        email: '',
        mailtmToken: null,
        batchData: '',
        stats: { success: 0, fail: 0, skip: 0 }
    };

    // ============ STATUS HELPERS ============
    function setStatus(text, type = 'ready') {
        ui.statusBar.className = `status-bar status-${type}`;
        if (type === 'loading') {
            ui.statusText.innerHTML = `<span class="spinner"></span> ${text}`;
        } else {
            ui.statusText.textContent = text;
        }
    }

    // ============ DATA HELPERS ============
    function getDataLines() {
        return state.batchData.trim().split('\n').filter(line =>
            line.trim() && !line.toLowerCase().startsWith('first|')
        );
    }

    function getCurrentEntryData() {
        const lines = getDataLines();
        const idx = state.currentIndex;
        if (idx < 0 || idx >= lines.length) return null;

        const parts = lines[idx].split('|');
        if (parts.length < 5) return null;

        // Parse DOB: could be YYYY-MM-DD or Month Day Year
        let dobMonth, dobDay, dobYear;
        const dob = parts[3].trim();
        if (dob.includes('-')) {
            const [y, m, d] = dob.split('-');
            dobYear = y; dobMonth = m; dobDay = d;
        } else {
            // Assume "January 15 1985" format
            const dobParts = dob.split(' ');
            dobMonth = dobParts[0];
            dobDay = dobParts[1];
            dobYear = dobParts[2];
        }

        return {
            firstName: parts[0].trim(),
            lastName: parts[1].trim(),
            branch: parts[2].trim(),
            dobMonth, dobDay, dobYear,
            dischargeDate: parts[4].trim(),
            email: parts[5]?.includes('@') ? parts[5].trim() : state.email,
            original: lines[idx]
        };
    }

    function updateCurrentEntryDisplay() {
        const lines = getDataLines();
        const idx = state.currentIndex;

        if (lines.length === 0) {
            ui.currentEntry.textContent = 'No data loaded';
            ui.indexNum.textContent = '0';
            return;
        }

        if (idx >= lines.length) state.currentIndex = 0;

        ui.indexNum.textContent = state.currentIndex + 1;
        ui.currentEntry.textContent = lines[state.currentIndex] || 'No data';
    }

    function updateStatsDisplay() {
        ui.successCount.textContent = state.stats.success;
        ui.failCount.textContent = state.stats.fail;
        ui.skipCount.textContent = state.stats.skip;
    }

    function updateButtonStates() {
        ui.startBtn.disabled = state.isRunning;
        ui.stopBtn.disabled = !state.isRunning;
        ui.skipBtn.disabled = state.isRunning;
    }

    // ============ STORAGE ============
    async function loadState() {
        const stored = await chrome.storage.local.get([
            'veterans-state', 'veterans-stats', 'veterans-is-running'
        ]);

        if (stored['veterans-state']) {
            state = { ...state, ...stored['veterans-state'] };
        }
        if (stored['veterans-stats']) {
            state.stats = stored['veterans-stats'];
        }
        state.isRunning = stored['veterans-is-running'] || false;

        updateUI();
    }

    async function saveState() {
        await chrome.storage.local.set({
            'veterans-state': {
                currentIndex: state.currentIndex,
                email: state.email,
                mailtmToken: state.mailtmToken,
                batchData: state.batchData
            },
            'veterans-stats': state.stats,
            'veterans-is-running': state.isRunning
        });
    }

    function updateUI() {
        ui.emailInput.value = state.email;
        ui.batchData.value = state.batchData;
        updateCurrentEntryDisplay();
        updateStatsDisplay();
        updateButtonStates();
    }

    // ============ EMAIL GENERATION ============
    async function generateEmail() {
        const provider = ui.emailProvider.value;
        setStatus('Generating email...', 'loading');

        try {
            if (provider === 'tinyhost') {
                // tinyhost.shop - no account needed
                const username = 'veteran' + Math.random().toString(36).substring(2, 10);
                const email = `${username}@tinyhost.shop`;

                state.email = email;
                state.mailtmToken = null;
                ui.emailInput.value = email;

                setStatus(`Generated: ${email}`, 'ready');
            } else {
                // mail.tm - create account
                const domainResp = await fetch('https://api.mail.tm/domains');
                if (!domainResp.ok) throw new Error('Failed to get domains');

                const domainData = await domainResp.json();
                const domains = domainData['hydra:member'];
                if (!domains || domains.length === 0) throw new Error('No domains');

                const domain = domains[Math.floor(Math.random() * domains.length)].domain;
                const username = 'veteran' + Math.random().toString(36).substring(2, 10);
                const password = Math.random().toString(36).substring(2) + 'A1!';
                const email = `${username}@${domain}`;

                // Create account
                const accResp = await fetch('https://api.mail.tm/accounts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ address: email, password })
                });
                if (!accResp.ok) throw new Error('Failed to create account');

                // Get token
                const tokenResp = await fetch('https://api.mail.tm/token', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ address: email, password })
                });
                if (!tokenResp.ok) throw new Error('Failed to get token');

                const tokenData = await tokenResp.json();

                state.email = email;
                state.mailtmToken = tokenData.token;
                ui.emailInput.value = email;

                setStatus(`Generated: ${email}`, 'ready');
            }

            await saveState();
        } catch (e) {
            console.error('Email generation failed:', e);
            setStatus('Failed: ' + e.message, 'error');
        }
    }

    // ============ START/STOP/SKIP ============
    async function startVerification() {
        const lines = getDataLines();
        if (lines.length === 0) {
            setStatus('No data loaded', 'error');
            return;
        }

        state.isRunning = true;
        updateButtonStates();
        await saveState();

        setStatus('Starting verification...', 'loading');

        // Send message to content script
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!tab) {
            setStatus('No active tab', 'error');
            state.isRunning = false;
            updateButtonStates();
            return;
        }

        const entryData = getCurrentEntryData();
        if (!entryData) {
            setStatus('Invalid entry data', 'error');
            state.isRunning = false;
            updateButtonStates();
            return;
        }

        try {
            await chrome.tabs.sendMessage(tab.id, {
                action: 'startVerification',
                data: entryData,
                mailtmToken: state.mailtmToken
            });
            setStatus(`Processing: ${entryData.firstName} ${entryData.lastName}`, 'loading');
        } catch (e) {
            setStatus('Failed to start. Open SheerID page first.', 'error');
            state.isRunning = false;
            updateButtonStates();
        }
    }

    async function stopVerification() {
        state.isRunning = false;
        updateButtonStates();
        await saveState();

        // Send stop message
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (tab) {
            try {
                await chrome.tabs.sendMessage(tab.id, { action: 'stopVerification' });
            } catch (e) { }
        }

        setStatus('Stopped', 'ready');
    }

    async function skipEntry() {
        if (state.isRunning) {
            setStatus('Stop first before skipping', 'error');
            return;
        }

        const lines = getDataLines();
        if (state.currentIndex >= lines.length) {
            setStatus('No more entries', 'error');
            return;
        }

        state.stats.skip++;
        state.currentIndex++;
        updateCurrentEntryDisplay();
        updateStatsDisplay();
        await saveState();

        setStatus(`Skipped. Next: ${state.currentIndex + 1}/${lines.length}`, 'ready');
    }

    async function fillNow() {
        const entryData = getCurrentEntryData();
        if (!entryData) {
            setStatus('No valid entry', 'error');
            return;
        }

        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!tab) {
            setStatus('No active tab', 'error');
            return;
        }

        try {
            await chrome.tabs.sendMessage(tab.id, {
                action: 'fillForm',
                data: entryData
            });
            setStatus(`Filled: ${entryData.firstName} ${entryData.lastName}`, 'ready');
        } catch (e) {
            setStatus('Failed. Open SheerID page first.', 'error');
        }
    }

    // ============ UTILITIES ============
    async function clearCookies() {
        setStatus('Clearing cookies...', 'loading');

        try {
            const allCookies = await chrome.cookies.getAll({});
            const cookiesToDelete = allCookies.filter(c =>
                c.domain.includes('chatgpt.com') || c.domain.includes('sheerid.com')
            );

            for (const cookie of cookiesToDelete) {
                const protocol = cookie.secure ? 'https' : 'http';
                const domain = cookie.domain.startsWith('.') ? cookie.domain.substring(1) : cookie.domain;
                const url = `${protocol}://${domain}${cookie.path || '/'}`;

                await chrome.cookies.remove({ url, name: cookie.name });
            }

            setStatus(`Cleared ${cookiesToDelete.length} cookies`, 'ready');
        } catch (e) {
            setStatus('Error: ' + e.message, 'error');
        }
    }

    async function downloadLog() {
        setStatus('Downloading log...', 'loading');

        const stored = await chrome.storage.local.get(['veterans-success-log']);
        const log = stored['veterans-success-log'] || [];

        if (log.length === 0) {
            setStatus('No success log yet', 'error');
            return;
        }

        let content = '=== VETERANS VERIFIED ACCOUNTS ===\n';
        content += `Generated: ${new Date().toLocaleString()}\n`;
        content += `Total: ${log.length}\n\n`;

        log.forEach((item, i) => {
            content += `[${i + 1}] ${item.email}\n`;
            content += `Data: ${item.data}\n`;
            content += `Time: ${item.time}\n\n`;
        });

        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const filename = `veterans-log-${new Date().toISOString().split('T')[0]}.txt`;

        chrome.downloads.download({ url, filename, saveAs: true });
        setStatus(`Downloaded ${log.length} records`, 'ready');
    }

    // ============ EVENT HANDLERS ============
    ui.indexUp.addEventListener('click', async () => {
        const lines = getDataLines();
        if (state.currentIndex < lines.length - 1) {
            state.currentIndex++;
            updateCurrentEntryDisplay();
            await saveState();
        }
    });

    ui.indexDown.addEventListener('click', async () => {
        if (state.currentIndex > 0) {
            state.currentIndex--;
            updateCurrentEntryDisplay();
            await saveState();
        }
    });

    ui.genEmailBtn.addEventListener('click', generateEmail);

    ui.batchData.addEventListener('change', async () => {
        state.batchData = ui.batchData.value;
        state.currentIndex = 0;
        updateCurrentEntryDisplay();
        await saveState();
    });

    ui.emailInput.addEventListener('change', async () => {
        state.email = ui.emailInput.value.trim();
        await saveState();
    });

    ui.startBtn.addEventListener('click', startVerification);
    ui.stopBtn.addEventListener('click', stopVerification);
    ui.skipBtn.addEventListener('click', skipEntry);
    ui.fillBtn.addEventListener('click', fillNow);
    ui.clearCookiesBtn.addEventListener('click', clearCookies);
    ui.downloadLogBtn.addEventListener('click', downloadLog);

    // Listen for messages from content script
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.action === 'updateStatus') {
            setStatus(message.status, message.type || 'ready');
        } else if (message.action === 'verificationComplete') {
            if (message.success) {
                state.stats.success++;
            } else {
                state.stats.fail++;
            }
            state.currentIndex++;
            updateCurrentEntryDisplay();
            updateStatsDisplay();
            saveState();

            // Auto continue if running
            if (state.isRunning && state.currentIndex < getDataLines().length) {
                setTimeout(startVerification, 2000);
            } else if (state.isRunning) {
                state.isRunning = false;
                updateButtonStates();
                setStatus('All entries processed!', 'ready');
            }
        }
        return true;
    });

    // Listen for storage changes
    chrome.storage.onChanged.addListener((changes, areaName) => {
        if (areaName === 'local') {
            if (changes['veterans-is-running']) {
                state.isRunning = changes['veterans-is-running'].newValue || false;
                updateButtonStates();
            }
            if (changes['veterans-stats']) {
                state.stats = changes['veterans-stats'].newValue;
                updateStatsDisplay();
            }
        }
    });

    // Init
    loadState();
})();
