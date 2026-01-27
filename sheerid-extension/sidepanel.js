// SheerID Extension - Side Panel Script
// Modern UI with document generation

const SERVICE_INFO = {
    spotify: { name: "Spotify Premium", type: "Student", description: "Auto-generates university student data", programId: "67c8c14f5f17a83b745e3f82" },
    youtube: { name: "YouTube Premium", type: "Student", description: "Auto-generates university student data", programId: "6743b9d64f90de1ff8a82c44" },
    googleone: { name: "Google One / Gemini Advanced", type: "Student", description: "Auto-generates university student data (US only)", programId: "6751c5cb22c30b9a1e8f8f29" },
    perplexity: { name: "Perplexity", type: "Student", description: "Auto-generates university student data", programId: "677cb53ce7f5e51e7ac74732" },
    cursor: { name: "Cursor IDE", type: "Student", description: "Auto-generates university student data (.edu email required)", programId: "681044b7729fba7beccd3565" },
    boltnew: { name: "Bolt.new", type: "Teacher", description: "Auto-generates teacher data (University)", programId: "677a49e7e7f5e51e7ac70c32" },
    canva: { name: "Canva Education", type: "Teacher", description: "Auto-generates UK teacher data (K-12)", programId: "5dae1055893a5e15eaa1a5b5" },
    k12: { name: "K12 / ChatGPT Plus", type: "Teacher", description: "Auto-generates K12 teacher data", programId: "67a32bb7225da97e18dca64a" },
    veterans: { name: "Veterans / ChatGPT Plus", type: "Military", description: "Requires manual veteran data input", programId: "690415d58971e73ca187d8c9" }
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
        generateDocBtn: document.getElementById('generateDocBtn'),
        docPreview: document.getElementById('docPreview'),
        docImage: document.getElementById('docImage'),
        downloadDocBtn: document.getElementById('downloadDocBtn'),
        clearBtn: document.getElementById('clearBtn'),
        exportBtn: document.getElementById('exportBtn'),
        importBtn: document.getElementById('importBtn')
    };

    // Load saved data
    const stored = await chrome.storage.local.get([
        'pluginEnabled', 'serviceType', 'email', 'veteransData', 'stats', 'generatedDoc'
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

    // Show generated doc if exists
    if (stored.generatedDoc) {
        elements.docImage.src = stored.generatedDoc;
        elements.docPreview.classList.add('show');
    }

    // Update service info display
    function updateServiceInfo() {
        const service = SERVICE_INFO[elements.serviceType.value];
        elements.serviceInfo.innerHTML = `
            <strong>${service.name}</strong>
            <div>${service.type} • ${service.description}</div>
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
    function showStatus(message, type = 'success') {
        elements.status.textContent = message;
        elements.status.className = `status-message show ${type}`;
        setTimeout(() => {
            elements.status.classList.remove('show');
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

    // Generate Document button
    elements.generateDocBtn.addEventListener('click', async () => {
        showDocumentCustomizer();
    });

    // Download document button
    elements.downloadDocBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.download = `student-id-${Date.now()}.png`;
        link.href = elements.docImage.src;
        link.click();
        showStatus('Document downloaded!', 'success');
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
        a.download = `sheerid-backup-${Date.now()}.json`;
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

    // Show document customizer dialog
    function showDocumentCustomizer() {
        const modal = document.createElement('div');
        modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 20px;';

        const dialog = document.createElement('div');
        dialog.style.cssText = 'background: var(--bg-primary); border-radius: 12px; padding: 24px; max-width: 400px; width: 100%; max-height: 90vh; overflow-y: auto;';

        dialog.innerHTML = `
            <h2 style="margin-bottom: 20px; font-size: 20px; font-weight: 700;">Generate Student ID</h2>

            <div class="form-group">
                <label>First Name</label>
                <input type="text" id="customFirstName" placeholder="John" style="width: 100%;">
            </div>

            <div class="form-group">
                <label>Last Name</label>
                <input type="text" id="customLastName" placeholder="Doe" style="width: 100%;">
            </div>

            <div class="form-group">
                <label>University/School</label>
                <input type="text" id="customSchool" placeholder="Stanford University" style="width: 100%;">
            </div>

            <div class="form-group">
                <label>Student ID (Optional)</label>
                <input type="text" id="customStudentId" placeholder="Auto-generated" style="width: 100%;">
            </div>

            <div class="form-group">
                <label>Issue Date</label>
                <input type="date" id="customDate" style="width: 100%;">
            </div>

            <div class="form-group">
                <label>Valid Until</label>
                <input type="date" id="customValidUntil" style="width: 100%;">
            </div>

            <div class="button-grid">
                <button class="btn btn-primary" id="generateBtn">
                    <span>✨</span>
                    <span>Generate</span>
                </button>
                <button class="btn btn-secondary" id="cancelBtn">
                    <span>✕</span>
                    <span>Cancel</span>
                </button>
            </div>
        `;

        modal.appendChild(dialog);
        document.body.appendChild(modal);

        // Set default dates
        const today = new Date();
        const validUntil = new Date(today);
        validUntil.setFullYear(validUntil.getFullYear() + 1);

        dialog.querySelector('#customDate').value = today.toISOString().split('T')[0];
        dialog.querySelector('#customValidUntil').value = validUntil.toISOString().split('T')[0];

        // Cancel button
        dialog.querySelector('#cancelBtn').addEventListener('click', () => {
            modal.remove();
        });

        // Generate button
        dialog.querySelector('#generateBtn').addEventListener('click', async () => {
            const firstName = dialog.querySelector('#customFirstName').value.trim() || 'John';
            const lastName = dialog.querySelector('#customLastName').value.trim() || 'Doe';
            const school = dialog.querySelector('#customSchool').value.trim() || 'University';
            const studentId = dialog.querySelector('#customStudentId').value.trim();
            const issueDate = dialog.querySelector('#customDate').value;
            const validUntil = dialog.querySelector('#customValidUntil').value;

            modal.remove();
            showStatus('Generating document...', 'success');

            try {
                const docData = await generateStudentID(firstName, lastName, school, studentId, issueDate, validUntil);
                elements.docImage.src = docData;
                elements.docPreview.classList.add('show');

                // Save for later use
                await chrome.storage.local.set({ generatedDoc: docData });

                showStatus('Document generated successfully!', 'success');
            } catch (err) {
                showStatus('Failed to generate document: ' + err.message, 'error');
            }
        });

        // Click outside to close
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    // Generate student ID using canvas
    async function generateStudentID(firstName, lastName, school, studentId, issueDate, validUntil) {
        const width = 650;
        const height = 400;
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');

        // Background
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, width, height);

        // Header
        const headerColor = '#' + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0');
        ctx.fillStyle = headerColor;
        ctx.fillRect(0, 0, width, 60);

        // Title
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('STUDENT IDENTIFICATION CARD', width / 2, 38);

        // School name
        ctx.fillStyle = headerColor;
        ctx.font = 'bold 18px Arial';
        ctx.fillText(school.substring(0, 50), width / 2, 95);

        // Photo placeholder
        ctx.strokeStyle = '#b4b4b4';
        ctx.lineWidth = 2;
        ctx.strokeRect(30, 120, 120, 160);
        ctx.fillStyle = '#e0e0e0';
        ctx.fillRect(32, 122, 116, 156);
        ctx.fillStyle = '#b4b4b4';
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('PHOTO', 90, 205);

        // Student info
        const id = studentId || `STU${Math.floor(Math.random() * 900000 + 100000)}`;
        const issue = issueDate || new Date().toISOString().split('T')[0];
        const valid = validUntil || new Date(new Date().setFullYear(new Date().getFullYear() + 1)).toISOString().split('T')[0];

        const info = [
            `Name: ${firstName} ${lastName}`,
            `ID: ${id}`,
            `Status: Full-time Student`,
            `Issued: ${issue}`,
            `Valid Until: ${valid}`
        ];

        ctx.fillStyle = '#333333';
        ctx.font = '18px Arial';
        ctx.textAlign = 'left';
        let y = 135;
        for (const line of info) {
            ctx.fillText(line, 175, y);
            y += 28;
        }

        // Barcode
        ctx.fillStyle = '#000000';
        for (let i = 0; i < 20; i++) {
            const x = 480 + i * 7;
            const h = 30 + Math.random() * 20;
            ctx.fillRect(x, 280, 3, h);
        }

        // Footer
        ctx.fillStyle = headerColor;
        ctx.fillRect(0, height - 40, width, 40);
        ctx.fillStyle = '#ffffff';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Property of University - If found, please return', width / 2, height - 18);

        return canvas.toDataURL('image/png');
    }
});
