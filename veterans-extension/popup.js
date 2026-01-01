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
        importBtn: document.getElementById('importBtn')
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
});
