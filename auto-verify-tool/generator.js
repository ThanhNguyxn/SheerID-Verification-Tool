const puppeteer = require('puppeteer');
const UNIVERSITIES = require('./universities-data');

// Shared browser instance for performance
let sharedBrowser = null;

async function getBrowser() {
    if (sharedBrowser) {
        if (sharedBrowser.isConnected()) {
            return sharedBrowser;
        }
        sharedBrowser = null;
    }

    global.emitLog('🚀 Launching Chrome browser...');
    sharedBrowser = await puppeteer.launch({
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu'
        ]
    });

    sharedBrowser.on('disconnected', () => {
        global.emitLog('⚠️ Browser disconnected');
        sharedBrowser = null;
    });

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

    // Find university object to get country
    const universityObj = UNIVERSITIES.find(u => u.name === studentInfo.university);
    const country = universityObj ? universityObj.country : 'USA'; // Default to USA
    const universityName = universityObj ? universityObj.name : studentInfo.university;

    try {
        await page.goto('https://thanhnguyxn.github.io/student-card-generator/', {
            waitUntil: 'domcontentloaded',
            timeout: 30000
        });

        await page.waitForSelector('#countrySelect', { timeout: 30000 });

        await page.select('#countrySelect', country);

        await new Promise(r => setTimeout(r, 1000)); // Wait for options to update

        await page.waitForFunction((uniName) => {
            const select = document.querySelector('#universitySelect');
            return !select.disabled && Array.from(select.options).some(opt => opt.textContent === uniName);
        }, { timeout: 30000 }, universityName);

        // Get the value (index) for the selected university
        const universityValue = await page.evaluate((uniName) => {
            const select = document.querySelector('#universitySelect');
            const option = Array.from(select.options).find(opt => opt.textContent === uniName);
            return option ? option.value : null;
        }, universityName);

        if (!universityValue) throw new Error(`University not found in dropdown: ${universityName}`);

        await page.select('#universitySelect', universityValue);

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
        if (page) await page.close();
        // Do not close browser here
    }
}

async function generatePayslip(teacherInfo) {
    global.emitLog('📸 Generating payslip...');
    const browser = await getBrowser();
    const page = await browser.newPage();

    // School rotation - 14 US universities
    // School rotation - use centralized list
    const universities = UNIVERSITIES.map(u => u.name);

    // Select university: Use provided one, or random from list
    const selectedUniversity = teacherInfo.university || universities[Math.floor(Math.random() * universities.length)];
    global.emitLog(`🎓 Payslip university: ${selectedUniversity}`);

    try {
        await page.goto('https://thanhnguyxn.github.io/payslip-generator/', {
            waitUntil: 'domcontentloaded',
            timeout: 30000
        });

        await new Promise(r => setTimeout(r, 3000));
        await page.waitForSelector('.editor-panel', { timeout: 30000 });

        // Fast input using evaluate with random university
        await page.evaluate((info, university) => {
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
            setInput('Company Name', university);
            setInput('Full Name', info.fullName || 'Jane Doe');
            setInput('Position', 'Professor');
            setInput('Employee ID', info.employeeId || 'E-1234567');
        }, teacherInfo, selectedUniversity);

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

async function generateTeacherCard(teacherInfo, options = {}) {
    global.emitLog('📸 Generating Faculty ID Card...');
    const browser = await getBrowser();
    const page = await browser.newPage();

    // School rotation - 14 US universities
    // School rotation - use centralized list
    const universities = UNIVERSITIES.map(u => u.name);

    // Select university: Use provided one, or random from list
    const selectedUniversity = teacherInfo.university || universities[Math.floor(Math.random() * universities.length)];
    global.emitLog(`🎓 Selected university: ${selectedUniversity}`);

    try {
        await page.goto('https://thanhnguyxn.github.io/payslip-generator/', {
            waitUntil: 'domcontentloaded',
            timeout: 30000
        });

        await new Promise(r => setTimeout(r, 3000));
        await page.waitForSelector('.editor-panel', { timeout: 30000 });

        // Fill in employee info with random university
        await page.evaluate((info, university) => {
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
            setInput('Company Name', university);
            setInput('Full Name', info.fullName || 'Jane Doe');
            setInput('Position', 'Professor');
            setInput('Employee ID', info.employeeId || 'E-1234567');
        }, teacherInfo, selectedUniversity);

        await new Promise(r => setTimeout(r, 500));

        // Click Teacher ID tab
        const tabs = await page.$$('.tab-btn');
        for (const tab of tabs) {
            const text = await page.evaluate(el => el.textContent, tab);
            if (text.includes('Teacher ID')) {
                await tab.click();
                break;
            }
        }

        await new Promise(r => setTimeout(r, 1500));

        // Handle PDF generation if requested
        if (options.format === 'pdf') {
            global.emitLog('📄 Generating PDF...');

            try {
                // Wait for the exposed function to be available
                await page.waitForFunction(() => typeof window.getTeacherCardPdfBase64 === 'function', { timeout: 15000 });

                const pdfBase64 = await page.evaluate(async () => {
                    try {
                        return await window.getTeacherCardPdfBase64();
                    } catch (err) {
                        return { error: err.toString() };
                    }
                });

                if (!pdfBase64) throw new Error('PDF generation returned null');
                if (pdfBase64.error) throw new Error(`Browser error: ${pdfBase64.error}`);

                // Convert base64 to buffer (strip data:application/pdf;base64, prefix if present)
                const base64Data = pdfBase64.replace(/^data:.*,/, '');
                const pdfBuffer = Buffer.from(base64Data, 'base64');

                global.emitLog('✅ Faculty ID Card PDF generated');
                return pdfBuffer;
            } catch (err) {
                global.emitLog(`❌ PDF generation failed: ${err.message}`);
                throw err;
            }
        }

        // Screenshot front card only
        const cardElement = await page.$('#teacher-card-front');
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
