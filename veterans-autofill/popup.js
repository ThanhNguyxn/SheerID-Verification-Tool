// Veterans Autofill - Popup Script
(function () {
    const $ = id => document.getElementById(id);

    // UI Elements
    const ui = {
        enableToggle: $('enableToggle'),
        indexNum: $('indexNum'),
        indexUp: $('indexUp'),
        indexDown: $('indexDown'),
        currentEntry: $('currentEntry'),
        emailInput: $('emailInput'),
        generateEmailBtn: $('generateEmailBtn'),
        batchData: $('batchData'),
        fillFormBtn: $('fillFormBtn'),
        nextEntryBtn: $('nextEntryBtn'),
        openChatGPTBtn: $('openChatGPTBtn'),
        statusBar: $('statusBar'),
        statusText: $('statusText')
    };

    // State
    let state = {
        enabled: false,
        currentIndex: 0,
        email: '',
        mailtmToken: null,
        batchData: ''
    };

    // Status helpers
    function setStatus(text, type = 'ready') {
        ui.statusBar.className = `status-bar status-${type}`;
        if (type === 'loading') {
            ui.statusText.innerHTML = `<span class="spinner"></span> ${text}`;
        } else {
            ui.statusText.textContent = text;
        }
    }

    // Parse batch data lines
    function getDataLines() {
        return state.batchData.trim().split('\n').filter(line =>
            line.trim() && !line.toLowerCase().startsWith('first|')
        );
    }

    // Get current entry based on index
    function getCurrentEntryData() {
        const lines = getDataLines();
        const idx = state.currentIndex;
        if (idx < 0 || idx >= lines.length) return null;

        const parts = lines[idx].split('|');
        if (parts.length < 5) return null;

        return {
            firstName: parts[0].trim(),
            lastName: parts[1].trim(),
            branch: parts[2].trim(),
            dob: parts[3].trim(),
            dischargeDate: parts[4].trim(),
            email: parts[5]?.includes('@') ? parts[5].trim() : state.email
        };
    }

    // Update current entry display
    function updateCurrentEntryDisplay() {
        const lines = getDataLines();
        const idx = state.currentIndex;

        if (lines.length === 0) {
            ui.currentEntry.textContent = 'No data loaded';
            ui.indexNum.textContent = '-';
            return;
        }

        if (idx >= lines.length) {
            state.currentIndex = 0;
        }

        ui.indexNum.textContent = state.currentIndex + 1;
        ui.currentEntry.textContent = lines[state.currentIndex] || 'No data';
    }

    // Load state from storage
    async function loadState() {
        const stored = await chrome.storage.local.get(['veteransAutofill']);
        if (stored.veteransAutofill) {
            state = { ...state, ...stored.veteransAutofill };
        }
        updateUI();
    }

    // Save state to storage
    async function saveState() {
        await chrome.storage.local.set({ veteransAutofill: state });
    }

    // Update UI from state
    function updateUI() {
        ui.enableToggle.checked = state.enabled;
        ui.emailInput.value = state.email;
        ui.batchData.value = state.batchData;
        updateCurrentEntryDisplay();
    }

    // ============ EMAIL GENERATION ============
    async function generateEmail() {
        setStatus('Generating email...', 'loading');

        try {
            const domainResp = await fetch('https://api.mail.tm/domains');
            if (!domainResp.ok) throw new Error('Failed to get domains');

            const domainData = await domainResp.json();
            const domains = domainData['hydra:member'];
            if (!domains || domains.length === 0) throw new Error('No domains available');

            const domain = domains[Math.floor(Math.random() * domains.length)].domain;
            const username = 'veteran' + Math.random().toString(36).substring(2, 10);
            const password = Math.random().toString(36).substring(2) + 'A1!';
            const email = `${username}@${domain}`;

            const accResp = await fetch('https://api.mail.tm/accounts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ address: email, password: password })
            });
            if (!accResp.ok) throw new Error('Failed to create account');

            const tokenResp = await fetch('https://api.mail.tm/token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ address: email, password: password })
            });
            if (!tokenResp.ok) throw new Error('Failed to get token');

            const tokenData = await tokenResp.json();

            state.email = email;
            state.mailtmToken = tokenData.token;
            ui.emailInput.value = email;

            await saveState();
            setStatus('Email generated!', 'ready');

        } catch (e) {
            console.error('Email generation failed:', e);
            setStatus('Failed: ' + e.message, 'error');
        }
    }

    // ============ FILL FORM ============
    async function fillForm() {
        const entryData = getCurrentEntryData();
        if (!entryData) {
            setStatus('No valid data at current index', 'error');
            return;
        }

        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!tab) {
            setStatus('No active tab', 'error');
            return;
        }

        try {
            await chrome.tabs.sendMessage(tab.id, {
                type: 'FILL_FORM',
                data: entryData
            });
            setStatus(`Filled: ${entryData.firstName} ${entryData.lastName}`, 'ready');
        } catch (e) {
            setStatus('Not on SheerID page', 'error');
        }
    }

    // ============ EVENT HANDLERS ============
    ui.enableToggle.addEventListener('change', async () => {
        state.enabled = ui.enableToggle.checked;
        await saveState();
        setStatus(state.enabled ? 'Enabled' : 'Disabled', 'ready');
    });

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

    ui.generateEmailBtn.addEventListener('click', generateEmail);

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

    ui.fillFormBtn.addEventListener('click', fillForm);

    ui.nextEntryBtn.addEventListener('click', async () => {
        const lines = getDataLines();
        if (state.currentIndex < lines.length - 1) {
            state.currentIndex++;
        } else {
            state.currentIndex = 0; // Loop back
        }
        updateCurrentEntryDisplay();
        await saveState();
        setStatus(`Entry ${state.currentIndex + 1}/${lines.length}`, 'ready');
    });

    ui.openChatGPTBtn.addEventListener('click', () => {
        chrome.tabs.create({ url: 'https://chatgpt.com/veterans-claim' });
    });

    // Init
    loadState();
})();
