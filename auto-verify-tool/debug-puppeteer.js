
const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    console.log('🚀 Launching browser for debug...');
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Set a realistic user agent
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');

    try {
        console.log('🌐 Navigating to SheerID verification page...');
        await page.goto('https://services.sheerid.com/verify/67c8c14f5f17a83b745e3f82/', { waitUntil: 'networkidle0' });

        console.log('⏳ Waiting 5 seconds...');
        await new Promise(r => setTimeout(r, 5000));

        console.log('📸 Taking screenshot...');
        await page.screenshot({ path: 'debug-screenshot.png', fullPage: true });

        console.log('💾 Saving HTML...');
        const html = await page.content();
        fs.writeFileSync('debug-page.html', html);

    } catch (error) {
        console.error('❌ Error:', error);
    } finally {
        await browser.close();
    }
})();
