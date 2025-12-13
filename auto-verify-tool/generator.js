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

        // Select University (MIT as default)
        // You can change this to random or specific university
        await page.select('#universitySelect', 'Massachusetts Institute of Technology');

        // Fill in the form
        await page.type('#studentName', studentInfo.fullName || 'John Doe');
        await page.type('#studentId', studentInfo.studentId || '12345678');

        // Date of Birth (YYYY-MM-DD)
        await page.type('#dateOfBirth', studentInfo.dob || '2000-01-01');

        // Wait for preview to update (give it a bit more time for the logo to load)
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

        // Helper function to type into input by label text
        const typeByLabel = async (labelText, value) => {
            const [input] = await page.$x(`//label[text()="${labelText}"]/following-sibling::input`);
            if (input) {
                await input.click({ clickCount: 3 }); // Select all
                await input.type(value);
            } else {
                console.warn(`Input for "${labelText}" not found`);
            }
        };

        // Fill in the form
        await typeByLabel('Company Name', 'Pennsylvania State University');
        await typeByLabel('Full Name', teacherInfo.fullName || 'Jane Doe');
        await typeByLabel('Position', 'Professor');
        await typeByLabel('Pay Date', new Date().toISOString().split('T')[0]);

        // Wait for preview to update
        await new Promise(r => setTimeout(r, 1000));

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

module.exports = { generateStudentCard, generatePayslip };
