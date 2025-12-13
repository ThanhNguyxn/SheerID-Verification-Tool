const puppeteer = require('puppeteer');
const path = require('path');

async function generateStudentCard(studentInfo) {
    console.log('📸 Launching browser to generate student card...');
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    try {
        // Navigate to the generator
        await page.goto('https://thanhnguyxn.github.io/student-card-generator/', {
            waitUntil: 'networkidle0'
        });

        // Wait for the country select to be available
        await page.waitForSelector('#countrySelect');

        // Select Country (USA)
        await page.select('#countrySelect', 'USA');

        // Wait for university select to be enabled and populated
        await page.waitForFunction(() => {
            const select = document.querySelector('#universitySelect');
            return !select.disabled && select.options.length > 1;
        });

        // Select Pennsylvania State University (must match org in API submission)
        await page.select('#universitySelect', 'Pennsylvania State University-Main Campus');

        // Clear and fill in the form with exact info from API
        await page.$eval('#studentName', el => el.value = '');
        await page.type('#studentName', studentInfo.fullName || 'John Doe');

        await page.$eval('#studentId', el => el.value = '');
        await page.type('#studentId', studentInfo.studentId || '12345678');

        // Date of Birth (YYYY-MM-DD) - must match birthDate in API
        await page.$eval('#dateOfBirth', el => el.value = '');
        await page.type('#dateOfBirth', studentInfo.dob || '2000-01-01');

        // Wait for preview to update
        await new Promise(r => setTimeout(r, 2000));

        // Find the card element to screenshot
        const cardElement = await page.$('#cardPreview');

        if (!cardElement) {
            throw new Error('Card preview element not found');
        }

        const imageBuffer = await cardElement.screenshot({
            type: 'png',
            encoding: 'binary'
        });

        console.log('✅ Card generated successfully');
        return imageBuffer;

    } catch (error) {
        console.error('❌ Error generating card:', error);
        throw error;
    } finally {
        await browser.close();
    }
}

async function generatePayslip(teacherInfo) {
    console.log('📸 Launching browser to generate payslip...');
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    try {
        // Navigate to the payslip generator
        await page.goto('https://thanhnguyxn.github.io/payslip-generator/', {
            waitUntil: 'networkidle0'
        });

        // Wait for React to fully hydrate
        await new Promise(r => setTimeout(r, 2000));
        await page.waitForSelector('.editor-panel');

        // Helper function to type into input by finding label text in input-group
        const typeByLabel = async (labelText, value) => {
            await page.evaluate((label, val) => {
                const labels = Array.from(document.querySelectorAll('.input-group label'));
                const targetLabel = labels.find(l => l.textContent === label);
                if (targetLabel) {
                    const input = targetLabel.parentElement.querySelector('input');
                    if (input) {
                        // Trigger React's onChange by setting native value setter
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        nativeInputValueSetter.call(input, val);
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }
            }, labelText, value);
        };

        // Fill in the form - Company should match SheerID org
        await typeByLabel('Company Name', 'Pennsylvania State University');
        await typeByLabel('Full Name', teacherInfo.fullName || 'Jane Doe');
        await typeByLabel('Position', 'Professor');
        await typeByLabel('Employee ID', teacherInfo.employeeId || 'E-1234567');
        await typeByLabel('Pay Date', new Date().toISOString().split('T')[0]);

        // Wait for preview to update
        await new Promise(r => setTimeout(r, 1500));

        // Find the card element to screenshot
        const cardElement = await page.$('.payslip-container');

        if (!cardElement) {
            throw new Error('Payslip preview element not found');
        }

        const imageBuffer = await cardElement.screenshot({
            type: 'png',
            encoding: 'binary'
        });

        console.log('✅ Payslip generated successfully');
        return imageBuffer;

    } catch (error) {
        console.error('❌ Error generating payslip:', error);
        throw error;
    } finally {
        await browser.close();
    }
}

async function generateTeacherCard(teacherInfo) {
    console.log('📸 Launching browser to generate Faculty ID Card...');
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    try {
        // Navigate to the generator
        await page.goto('https://thanhnguyxn.github.io/student-card-generator/', {
            waitUntil: 'networkidle0'
        });

        // Wait for the country select to be available
        await page.waitForSelector('#countrySelect');

        // Click Teacher mode button to switch to Faculty ID Card
        await page.click('#teacherModeBtn');
        await new Promise(r => setTimeout(r, 500));

        // Select Country (USA)
        await page.select('#countrySelect', 'USA');

        // Wait for university select to be enabled and populated
        await page.waitForFunction(() => {
            const select = document.querySelector('#universitySelect');
            return !select.disabled && select.options.length > 1;
        });

        // Select Pennsylvania State University (must match org in API)
        await page.select('#universitySelect', 'Pennsylvania State University-Main Campus');

        // Fill in the form
        await page.evaluate((name) => {
            document.querySelector('#studentName').value = name;
        }, teacherInfo.fullName || 'Jane Doe');

        await page.evaluate((id) => {
            document.querySelector('#studentId').value = id;
        }, teacherInfo.employeeId || 'UT-' + Math.floor(Math.random() * 900000 + 100000));

        // Date of Birth (YYYY-MM-DD)
        if (teacherInfo.dob) {
            await page.evaluate((dob) => {
                document.querySelector('#dateOfBirth').value = dob;
            }, teacherInfo.dob);
        }

        // Click regenerate to refresh the card
        await page.click('#regenerateBtn');

        // Wait for preview to update
        await new Promise(r => setTimeout(r, 2000));

        // Find the card element to screenshot
        const cardElement = await page.$('.id-card');

        if (!cardElement) {
            throw new Error('Faculty ID Card preview element not found');
        }

        const imageBuffer = await cardElement.screenshot({
            type: 'png',
            encoding: 'binary'
        });

        console.log('✅ Faculty ID Card generated successfully');
        return imageBuffer;

    } catch (error) {
        console.error('❌ Error generating Faculty ID Card:', error);
        throw error;
    } finally {
        await browser.close();
    }
}

module.exports = { generateStudentCard, generatePayslip, generateTeacherCard };
