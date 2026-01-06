// Veterans Extension - Popup Script
// Enhanced with statistics and export/import

document.addEventListener('DOMContentLoaded', async () => {
    const elements = {
        pluginEnabled: document.getElementById('pluginEnabled'),
        programId: document.getElementById('programId'),
        inputData: document.getElementById('inputData'),
        currentIndex: document.getElementById('currentIndex'),
        email: document.getElementById('email'),
        usedList: document.getElementById('usedList'),
        status: document.getElementById('status'),
        saveBtn: document.getElementById('saveBtn'),
        fillBtn: document.getElementById('fillBtn'),
        clearBtn: document.getElementById('clearBtn'),
        // New elements
        successCount: document.getElementById('successCount'),
        failCount: document.getElementById('failCount'),
        skipCount: document.getElementById('skipCount'),
        exportBtn: document.getElementById('exportBtn'),
        importBtn: document.getElementById('importBtn'),
        genEmailBtn: document.getElementById('genEmailBtn')
    };

    // Load saved data
    const stored = await chrome.storage.local.get([
        'pluginEnabled', 'programId', 'inputData', 'currentIndex', 'email', 'usedItems',
        'stats'
    ]);

    elements.pluginEnabled.checked = stored.pluginEnabled !== false;
    elements.programId.value = stored.programId || '690415d58971e73ca187d8c9';
    elements.inputData.value = stored.inputData || '';
    elements.currentIndex.value = stored.currentIndex || 0;
    elements.email.value = stored.email || '';

    // Load statistics
    const stats = stored.stats || { success: 0, fail: 0, skip: 0 };
    if (elements.successCount) elements.successCount.textContent = stats.success;
    if (elements.failCount) elements.failCount.textContent = stats.fail;
    if (elements.skipCount) elements.skipCount.textContent = stats.skip;

    // Display used items
    const usedItems = stored.usedItems || [];
    elements.usedList.innerHTML = usedItems.map(item => `<div>${item}</div>`).join('') || '';

    // Show status
    function showStatus(message, type = '') {
        elements.status.textContent = message;
        elements.status.className = `status ${type}`;
        setTimeout(() => {
            elements.status.textContent = '';
            elements.status.className = 'status';
        }, 3000);
    }

    // Update stats display
    async function updateStats(type) {
        const stored = await chrome.storage.local.get(['stats']);
        const stats = stored.stats || { success: 0, fail: 0, skip: 0 };
        stats[type] = (stats[type] || 0) + 1;
        await chrome.storage.local.set({ stats });

        if (elements.successCount) elements.successCount.textContent = stats.success;
        if (elements.failCount) elements.failCount.textContent = stats.fail;
        if (elements.skipCount) elements.skipCount.textContent = stats.skip;
    }

    // Save button
    elements.saveBtn.addEventListener('click', async () => {
        await chrome.storage.local.set({
            pluginEnabled: elements.pluginEnabled.checked,
            programId: elements.programId.value.trim() || '690415d58971e73ca187d8c9',
            inputData: elements.inputData.value,
            currentIndex: parseInt(elements.currentIndex.value) || 0,
            email: elements.email.value.trim()
        });
        showStatus('✅ Configuration saved!', 'success');
    });

    // Toggle change
    elements.pluginEnabled.addEventListener('change', async () => {
        await chrome.storage.local.set({ pluginEnabled: elements.pluginEnabled.checked });
        showStatus(elements.pluginEnabled.checked ? '✅ Extension enabled' : '⏸️ Extension disabled', 'success');
    });

    // Fill button
    elements.fillBtn.addEventListener('click', async () => {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        if (!tab.url.includes('sheerid.com')) {
            showStatus('❌ Please open a SheerID page first', 'error');
            return;
        }

        try {
            await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: () => {
                    window.dispatchEvent(new CustomEvent('veteransFillForm'));
                }
            });
            showStatus('📝 Filling form...', 'success');
        } catch (err) {
            showStatus('❌ Failed to fill form', 'error');
        }
    });

    // Clear button
    elements.clearBtn.addEventListener('click', async () => {
        await chrome.storage.local.set({ usedItems: [], stats: { success: 0, fail: 0, skip: 0 } });
        elements.usedList.innerHTML = '';
        if (elements.successCount) elements.successCount.textContent = '0';
        if (elements.failCount) elements.failCount.textContent = '0';
        if (elements.skipCount) elements.skipCount.textContent = '0';
        showStatus('🗑️ Used list and stats cleared', 'success');
    });

    // Export button
    if (elements.exportBtn) {
        elements.exportBtn.addEventListener('click', async () => {
            const data = await chrome.storage.local.get(null);
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `veterans-extension-backup-${Date.now()}.json`;
            a.click();
            URL.revokeObjectURL(url);
            showStatus('📤 Configuration exported!', 'success');
        });
    }

    // Import button
    if (elements.importBtn) {
        elements.importBtn.addEventListener('click', () => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';
            input.onchange = async (e) => {
                const file = e.target.files[0];
                if (!file) return;

                try {
                    const text = await file.text();
                    const data = JSON.parse(text);
                    await chrome.storage.local.set(data);
                    showStatus('📥 Configuration imported! Reloading...', 'success');
                    setTimeout(() => location.reload(), 1000);
                } catch (err) {
                    showStatus('❌ Invalid backup file', 'error');
                }
            };
            input.click();
        });
    }

    // Listen for stats updates from content script
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.type === 'statsUpdate') {
            updateStats(message.stat);
        }
    });

    // Generate Email Button - supports mail.tm and tinyhost.shop
    if (elements.genEmailBtn) {
        elements.genEmailBtn.addEventListener('click', async () => {
            elements.genEmailBtn.textContent = '...';
            elements.genEmailBtn.disabled = true;

            const provider = document.getElementById('emailProvider')?.value || 'mailtm';

            try {
                let email, token;

                if (provider === 'tinyhost') {
                    // ============ tinyhost.shop - simpler API ============
                    // Get random domains
                    const domainResp = await fetch('https://tinyhost.shop/api/random-domains/?limit=5');
                    if (!domainResp.ok) throw new Error('Failed to get tinyhost domains');
                    const domainData = await domainResp.json();
                    const domains = domainData.domains || ['tinyhost.shop'];
                    const domain = domains[Math.floor(Math.random() * domains.length)];

                    // Generate random username
                    const username = 'user' + Math.random().toString(36).substring(2, 10);
                    email = `${username}@${domain}`;

                    // No account creation needed for tinyhost!
                    // Save email and provider info
                    elements.email.value = email;
                    await chrome.storage.local.set({
                        email: email,
                        emailProvider: 'tinyhost',
                        tinyhostDomain: domain,
                        tinyhostUser: username
                    });

                    showStatus(`✅ Generated tinyhost email!`, 'success');

                } else {
                    // ============ mail.tm - original logic ============
                    // 1. Get domains
                    const domainResp = await fetch('https://api.mail.tm/domains');
                    if (!domainResp.ok) throw new Error('Failed to get mail.tm domains');
                    const domainData = await domainResp.json();
                    const domains = domainData['hydra:member'];
                    if (!domains || domains.length === 0) throw new Error('No mail.tm domains available');
                    const domain = domains[Math.floor(Math.random() * domains.length)].domain;

                    // 2. Create account
                    const username = 'user' + Math.random().toString(36).substring(7);
                    const password = Math.random().toString(36).substring(2) + 'A1!';
                    email = `${username}@${domain}`;

                    const accResp = await fetch('https://api.mail.tm/accounts', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ address: email, password: password })
                    });

                    if (!accResp.ok) throw new Error('Failed to create mail.tm account');

                    // 3. Get token
                    const tokenResp = await fetch('https://api.mail.tm/token', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ address: email, password: password })
                    });

                    if (!tokenResp.ok) throw new Error('Failed to get mail.tm token');
                    const tokenData = await tokenResp.json();
                    token = tokenData.token;

                    // 4. Save
                    elements.email.value = email;
                    await chrome.storage.local.set({
                        email: email,
                        emailProvider: 'mailtm',
                        mailtmToken: token
                    });

                    showStatus('✅ Generated mail.tm email!', 'success');
                }
            } catch (err) {
                console.error(err);
                showStatus(`❌ ${err.message || 'Failed to generate email'}`, 'error');
            } finally {
                elements.genEmailBtn.textContent = 'Generate';
                elements.genEmailBtn.disabled = false;
            }
        });
    }
});
