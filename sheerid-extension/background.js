// SheerID Extension - Background Service Worker
// Handles extension lifecycle and message passing

console.log('[SheerID Background] Service worker started');

// Listen for messages from content scripts and popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('[SheerID Background] Message received:', message);

    if (message.type === 'statsUpdate') {
        // Update stats
        chrome.storage.local.get(['stats'], (result) => {
            const stats = result.stats || { success: 0, fail: 0, skip: 0 };
            stats[message.stat] = (stats[message.stat] || 0) + 1;

            chrome.storage.local.set({ stats }, () => {
                console.log('[SheerID Background] Stats updated:', stats);
            });
        });
    } else if (message.action === 'verificationComplete') {
        // Handle verification completion
        console.log('[SheerID Background] Verification complete:', message.success);

        // Update stats
        const stat = message.success ? 'success' : 'fail';
        chrome.storage.local.get(['stats'], (result) => {
            const stats = result.stats || { success: 0, fail: 0, skip: 0 };
            stats[stat] = (stats[stat] || 0) + 1;
            chrome.storage.local.set({ stats });
        });
    } else if (message.action === 'updateStatus') {
        // Status update from content script
        console.log('[SheerID Background] Status update:', message.status, message.type);
    }

    return true; // Keep message channel open
});

// Handle extension icon click - open side panel
chrome.action.onClicked.addListener(async (tab) => {
    console.log('[SheerID Background] Extension icon clicked');

    try {
        // Open side panel for this tab
        await chrome.sidePanel.open({ tabId: tab.id });
        console.log('[SheerID Background] Side panel opened');
    } catch (err) {
        console.error('[SheerID Background] Failed to open side panel:', err);
    }
});

// Handle installation
chrome.runtime.onInstalled.addListener((details) => {
    console.log('[SheerID Background] Extension installed/updated:', details.reason);

    if (details.reason === 'install') {
        // First time installation
        chrome.storage.local.set({
            pluginEnabled: true,
            serviceType: 'spotify',
            stats: { success: 0, fail: 0, skip: 0 }
        }, () => {
            console.log('[SheerID Background] Default settings initialized');
        });

        // Open welcome page
        chrome.tabs.create({
            url: 'https://github.com/ThanhNguyxn/SheerID-Verification-Tool'
        });
    } else if (details.reason === 'update') {
        console.log('[SheerID Background] Extension updated to version:', chrome.runtime.getManifest().version);
    }
});

// Handle browser startup
chrome.runtime.onStartup.addListener(() => {
    console.log('[SheerID Background] Browser started with extension');
});

// Keep service worker alive
let keepAliveInterval;

function keepAlive() {
    keepAliveInterval = setInterval(() => {
        chrome.runtime.getPlatformInfo(() => {
            // This will keep the service worker alive
        });
    }, 20000); // Every 20 seconds
}

keepAlive();
