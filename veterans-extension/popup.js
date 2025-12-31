// Veterans Extension - Popup Script

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
        clearBtn: document.getElementById('clearBtn')
    };

    // Load saved data
    const stored = await chrome.storage.local.get([
        'pluginEnabled', 'programId', 'inputData', 'currentIndex', 'email', 'usedItems'
    ]);

    elements.pluginEnabled.checked = stored.pluginEnabled !== false;
    elements.programId.value = stored.programId || '690415d58971e73ca187d8c9';
    elements.inputData.value = stored.inputData || '';
    elements.currentIndex.value = stored.currentIndex || 0;
    elements.email.value = stored.email || '';

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
        await chrome.storage.local.set({ usedItems: [] });
        elements.usedList.innerHTML = '';
        showStatus('🗑️ Used list cleared', 'success');
    });
});
