const puppeteer = require('puppeteer');

// Shared browser instance for performance
let sharedBrowser = null;

async function getBrowser() {
    if (!sharedBrowser || !sharedBrowser.isConnected()) {
        global.emitLog('🚀 Launching Chrome browser...');
        sharedBrowser = await puppeteer.launch({
            headless: "new",
            protocolTimeout: 300000, // 5 minutes for slow VMs
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--no-first-run',
                '--no-zygote',
                '--single-process',
                '--disable-extensions',
                // Memory optimization
                '--disable-background-networking',
                '--disable-default-apps',
                '--disable-sync',
                '--disable-translate',
                '--mute-audio',
                '--hide-scrollbars',
                '--disable-infobars',
                '--disable-features=site-per-process',
                '--js-flags=--max-old-space-size=512'
            ]
        });
    }
    return sharedBrowser;
}

async function closeBrowser() {
    if (sharedBrowser) {
        await sharedBrowser.close();
        sharedBrowser = null;
    }
}

async function generateStudentCard(studentInfo) {
    global.emitLog('📸 Generating student card...');
    const browser = await getBrowser();
    const page = await browser.newPage();

    try {
        await page.goto('https://thanhnguyxn.github.io/student-card-generator/', {
            waitUntil: 'domcontentloaded',
            timeout: 30000
        });

        await page.waitForSelector('#countrySelect', { timeout: 30000 });
        await page.select('#countrySelect', 'USA');

        await page.waitForFunction(() => {
            const select = document.querySelector('#universitySelect');
            return !select.disabled && select.options.length > 1;
        }, { timeout: 30000 });

        await page.select('#universitySelect', 'Pennsylvania State University-Main Campus');

        // Use evaluate for faster input (no typing delay)
        await page.evaluate((info) => {
            document.querySelector('#studentName').value = info.fullName || 'John Doe';
            document.querySelector('#studentId').value = info.studentId || '12345678';
            document.querySelector('#dateOfBirth').value = info.dob || '2000-01-01';
        }, studentInfo);

        // Shorter wait
        await new Promise(r => setTimeout(r, 1000));

        const cardElement = await page.$('#cardPreview');
        if (!cardElement) throw new Error('Card preview not found');

        const imageBuffer = await cardElement.screenshot({ type: 'png', encoding: 'binary' });
        global.emitLog('✅ Student card generated');
        return imageBuffer;

    } finally {
        await page.close();
    }
}

async function generatePayslip(teacherInfo) {
    global.emitLog('📸 Generating payslip...');
    const browser = await getBrowser();
    const page = await browser.newPage();

    try {
        await page.goto('https://thanhnguyxn.github.io/payslip-generator/', {
            waitUntil: 'domcontentloaded',
            timeout: 30000
        });

        await new Promise(r => setTimeout(r, 3000));
        await page.waitForSelector('.editor-panel', { timeout: 30000 });

        // Fast input using evaluate
        await page.evaluate((info) => {
            const setInput = (label, value) => {
                const labels = Array.from(document.querySelectorAll('.input-group label'));
                const targetLabel = labels.find(l => l.textContent === label);
                if (targetLabel) {
                    const input = targetLabel.parentElement.querySelector('input');
                    if (input) {
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        nativeInputValueSetter.call(input, value);
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }
            };
            setInput('Company Name', 'Pennsylvania State University');
            setInput('Full Name', info.fullName || 'Jane Doe');
            setInput('Position', 'Professor');
            setInput('Employee ID', info.employeeId || 'E-1234567');
        }, teacherInfo);

        await new Promise(r => setTimeout(r, 1000));

        const cardElement = await page.$('.payslip-container');
        if (!cardElement) throw new Error('Payslip container not found');

        const imageBuffer = await cardElement.screenshot({ type: 'png', encoding: 'binary' });
        global.emitLog('✅ Payslip generated');
        return imageBuffer;

    } finally {
        await page.close();
    }
}

async function generateTeacherCard(teacherInfo) {
    global.emitLog('📸 Generating Faculty ID Card...');
    const browser = await getBrowser();
    const page = await browser.newPage();

    try {
        await page.goto('https://thanhnguyxn.github.io/student-card-generator/', {
            waitUntil: 'domcontentloaded',
            timeout: 30000
        });

        await page.waitForSelector('#countrySelect', { timeout: 30000 });
        await page.click('#teacherModeBtn');
        await new Promise(r => setTimeout(r, 500));

        await page.select('#countrySelect', 'USA');

        await page.waitForFunction(() => {
            const select = document.querySelector('#universitySelect');
            return !select.disabled && select.options.length > 1;
        }, { timeout: 30000 });

        await page.select('#universitySelect', 'Pennsylvania State University-Main Campus');

        await page.evaluate((info) => {
            document.querySelector('#studentName').value = info.fullName || 'Jane Doe';
            document.querySelector('#studentId').value = info.employeeId || 'E-1234567';
            if (info.dob) document.querySelector('#dateOfBirth').value = info.dob;
        }, teacherInfo);

        const regenerateBtn = await page.$('#regenerateBtn');
        if (regenerateBtn) await regenerateBtn.click();

        await new Promise(r => setTimeout(r, 1000));

        const cardElement = await page.$('.id-card');
        if (!cardElement) throw new Error('Faculty ID Card not found');

        const imageBuffer = await cardElement.screenshot({ type: 'png', encoding: 'binary' });
        global.emitLog('✅ Faculty ID Card generated');
        return imageBuffer;

    } finally {
        await page.close();
    }
}

// Generate multiple documents in parallel
async function generateDocumentsParallel(info, docTypes = ['payslip', 'teacherCard']) {
    global.emitLog(`📸 Generating ${docTypes.length} documents in parallel...`);
    const startTime = Date.now();

    const promises = docTypes.map(type => {
        switch (type) {
            case 'studentCard': return generateStudentCard(info);
            case 'payslip': return generatePayslip(info);
            case 'teacherCard': return generateTeacherCard(info);
            default: return Promise.resolve(null);
        }
    });

    const results = await Promise.all(promises);
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    global.emitLog(`✅ All documents generated in ${elapsed}s`);

    return results;
}

module.exports = {
    generateStudentCard,
    generatePayslip,
    generateTeacherCard,
    generateDocumentsParallel,
    getBrowser,
    closeBrowser
};
