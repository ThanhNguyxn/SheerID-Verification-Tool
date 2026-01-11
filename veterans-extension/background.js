// Background service worker for Veterans Extension
// Handles side panel opening

chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'updateStatus') {
        // Forward status updates to side panel
        chrome.runtime.sendMessage(message);
    }
    return true;
});
