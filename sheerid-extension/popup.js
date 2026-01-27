// SheerID Extension - Popup Script
// Unified service selector and configuration

const SERVICE_INFO = {
    spotify: {
        name: "Spotify Premium",
        type: "Student",
        description: "Auto-generates university student data",
        programId: "67c8c14f5f17a83b745e3f82"
    },
    youtube: {
        name: "YouTube Premium",
        type: "Student",
        description: "Auto-generates university student data",
        programId: "6743b9d64f90de1ff8a82c44"
    },
    googleone: {
        name: "Google One / Gemini Advanced",
        type: "Student",
        description: "Auto-generates university student data (US only)",
        programId: "6751c5cb22c30b9a1e8f8f29"
    },
    perplexity: {
        name: "Perplexity",
        type: "Student",
        description: "Auto-generates university student data",
        programId: "677cb53ce7f5e51e7ac74732"
    },
    cursor: {
        name: "Cursor IDE",
        type: "Student",
        description: "Auto-generates university student data (.edu email required)",
        programId: "681044b7729fba7beccd3565"
    },
    boltnew: {
        name: "Bolt.new",
        type: "Teacher",
        description: "Auto-generates teacher data (University)",
        programId: "677a49e7e7f5e51e7ac70c32"
    },
    canva: {
        name: "Canva Education",
        type: "Teacher",
        description: "Auto-generates UK teacher data (K-12)",
        programId: "5dae1055893a5e15eaa1a5b5"
    },
    k12: {
        name: "K12 / ChatGPT Plus",
        type: "Teacher",
        description: "Auto-generates K12 teacher data",
        programId: "67a32bb7225da97e18dca64a"
    },
    veterans: {
        name: "Veterans / ChatGPT Plus",
        type: "Military",
        description: "Requires manual veteran data input",
        programId: "690415d58971e73ca187d8c9"
    }
};

document.addEventListener('DOMContentLoaded', async () => {
    const elements = {
        pluginEnabled: document.getElementById('pluginEnabled'),
        serviceType: document.getElementById('serviceType'),
        serviceInfo: document.getElementById('serviceInfo'),
        email: document.getElementById('email'),
        veteransDataGroup: document.getElementById('veteransDataGroup'),
        veteransData: document.getElementById('veteransData'),
        successCount: document.getElementById('successCount'),
        failCount: document.getElementById('failCount'),
        skipCount: document.getElementById('skipCount'),
        status: document.getElementById('status'),
        saveBtn: document.getElementById('saveBtn'),
        fillBtn: document.getElementById('fillBtn'),
        autoBtn: document.getElementById('autoBtn'),
        clearBtn: document.getElementById('clearBtn'),
        exportBtn: document.getElementById('exportBtn'),
        importBtn: document.getElementById('importBtn')
    };

    // Load saved data
    const stored = await chrome.storage.local.get([
        'pluginEnabled', 'serviceType', 'email', 'veteransData', 'stats'
    ]);

    elements.pluginEnabled.checked = stored.pluginEnabled !== false;
    elements.serviceType.value = stored.serviceType || 'spotify';
    elements.email.value = stored.email || '';
    elements.veteransData.value = stored.veteransData || '';

    // Load statistics
    const stats = stored.stats || { success: 0, fail: 0, skip: 0 };
    elements.successCount.textContent = stats.success;
    elements.failCount.textContent = stats.fail;
    elements.skipCount.textContent = stats.skip;

    // Update service info display
    function updateServiceInfo() {
        const service = SERVICE_INFO[elements.serviceType.value];
        elements.serviceInfo.innerHTML = `
            <strong>Selected: ${service.name}</strong>
            <div>Type: ${service.type} | ${service.description}</div>
        `;

        // Show/hide veterans data input
        if (elements.serviceType.value === 'veterans') {
            elements.veteransDataGroup.style.display = 'block';
        } else {
            elements.veteransDataGroup.style.display = 'none';
        }
    }

    updateServiceInfo();

    // Service type change
    elements.serviceType.addEventListener('change', () => {
        updateServiceInfo();
    });

    // Show status message
    function showStatus(message, type = '') {
        elements.status.textContent = message;
        elements.status.className = `status ${type}`;
        setTimeout(() => {
            elements.status.textContent = '';
            elements.status.className = 'status';
        }, 3000);
    }

    // Save button
    elements.saveBtn.addEventListener('click', async () => {
        const config = {
            pluginEnabled: elements.pluginEnabled.checked,
            serviceType: elements.serviceType.value,
            email: elements.email.value.trim(),
            veteransData: elements.veteransData.value.trim(),
            programId: SERVICE_INFO[elements.serviceType.value].programId
        };

        await chrome.storage.local.set(config);
        showStatus('Configuration saved successfully!', 'success');
    });

    // Toggle change
    elements.pluginEnabled.addEventListener('change', async () => {
        await chrome.storage.local.set({ pluginEnabled: elements.pluginEnabled.checked });
        showStatus(elements.pluginEnabled.checked ? 'Extension enabled' : 'Extension disabled', 'success');
    });

    // Fill button
    elements.fillBtn.addEventListener('click', async () => {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        if (!tab.url.includes('sheerid.com') && !tab.url.includes('chatgpt.com') && !tab.url.includes('openai.com')) {
            showStatus('Please open a SheerID or ChatGPT page first', 'error');
            return;
        }

        try {
            // Save config first
            await chrome.storage.local.set({
                serviceType: elements.serviceType.value,
                email: elements.email.value.trim(),
                veteransData: elements.veteransData.value.trim(),
                programId: SERVICE_INFO[elements.serviceType.value].programId
            });

            await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: () => {
                    window.dispatchEvent(new CustomEvent('sheeridFillForm'));
                }
            });
            showStatus('Filling form...', 'success');
        } catch (err) {
            showStatus('Failed to fill form: ' + err.message, 'error');
        }
    });

    // Auto button
    elements.autoBtn.addEventListener('click', async () => {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        if (!tab.url.includes('sheerid.com') && !tab.url.includes('chatgpt.com') && !tab.url.includes('openai.com')) {
            showStatus('Please open a SheerID or ChatGPT page first', 'error');
            return;
        }

        try {
            // Save config first
            await chrome.storage.local.set({
                serviceType: elements.serviceType.value,
                email: elements.email.value.trim(),
                veteransData: elements.veteransData.value.trim(),
                programId: SERVICE_INFO[elements.serviceType.value].programId,
                autoMode: true
            });

            await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: () => {
                    window.dispatchEvent(new CustomEvent('sheeridAutoRun'));
                }
            });
            showStatus('Auto mode started...', 'success');
        } catch (err) {
            showStatus('Failed to start auto mode: ' + err.message, 'error');
        }
    });

    // Clear button
    elements.clearBtn.addEventListener('click', async () => {
        if (confirm('Clear all statistics?')) {
            await chrome.storage.local.set({ stats: { success: 0, fail: 0, skip: 0 } });
            elements.successCount.textContent = '0';
            elements.failCount.textContent = '0';
            elements.skipCount.textContent = '0';
            showStatus('Statistics cleared', 'success');
        }
    });

    // Export button
    elements.exportBtn.addEventListener('click', async () => {
        const data = await chrome.storage.local.get(null);
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `sheerid-extension-backup-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
        showStatus('Configuration exported!', 'success');
    });

    // Import button
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
                showStatus('Configuration imported! Reloading...', 'success');
                setTimeout(() => location.reload(), 1000);
            } catch (err) {
                showStatus('Invalid backup file', 'error');
            }
        };
        input.click();
    });

    // Listen for stats updates from content script
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.type === 'statsUpdate') {
            updateStats(message.stat);
        }
    });

    // Update stats display
    async function updateStats(type) {
        const stored = await chrome.storage.local.get(['stats']);
        const stats = stored.stats || { success: 0, fail: 0, skip: 0 };
        stats[type] = (stats[type] || 0) + 1;
        await chrome.storage.local.set({ stats });

        elements.successCount.textContent = stats.success;
        elements.failCount.textContent = stats.fail;
        elements.skipCount.textContent = stats.skip;
    }
});
