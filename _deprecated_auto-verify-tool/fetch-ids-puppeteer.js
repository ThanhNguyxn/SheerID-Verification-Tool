
const puppeteer = require('puppeteer');
const fs = require('fs');

const UNIVERSITIES = [
    "Pennsylvania State University",
    "Massachusetts Institute of Technology",
    "Harvard University",
    "Stanford University",
    "University of California, Berkeley",
    "Yale University",
    "Princeton University",
    "Columbia University",
    "New York University",
    "University of California, Los Angeles",
    "University of Chicago",
    "Duke University",
    "Cornell University",
    "Northwestern University",
    "University of Toronto",
    "McGill University",
    "University of British Columbia",
    "Indian Institute of Technology Delhi",
    "University of Mumbai",
    "Hanoi University of Science and Technology",
    "VNU University of Engineering and Technology",
    "VNU University of Information Technology",
    "FPT University",
    "Posts and Telecommunications Institute of Technology",
    "VNU University of Science",
    "University of Oxford",
    "University of Cambridge",
    "Imperial College London",
    "The University of Tokyo",
    "Kyoto University",
    "Seoul National University",
    "Yonsei University",
    "Korea University",
    "Technical University of Munich",
    "Ludwig Maximilian University of Munich",
    "École Polytechnique",
    "PSL Research University",
    "National University of Singapore",
    "Nanyang Technological University",
    "Tsinghua University",
    "Peking University",
    "Fudan University",
    "University of São Paulo",
    "University of Campinas",
    "Federal University of Rio de Janeiro",
    "The University of Melbourne",
    "Australian National University",
    "The University of Sydney"
];

(async () => {
    console.log('🚀 Launching browser...');
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');

    try {
        console.log('🌐 Navigating to SheerID page...');
        await page.goto('https://services.sheerid.com/verify/67c8c14f5f17a83b745e3f82/', {
            waitUntil: 'domcontentloaded',
            timeout: 60000
        });

        console.log('🧪 Fetching program theme...');

        const config = await page.evaluate(async () => {
            try {
                const response = await fetch('https://services.sheerid.com/rest/v2/program/67c8c14f5f17a83b745e3f82/theme');
                const data = await response.json();
                return data;
            } catch (e) {
                return { error: e.toString() };
            }
        });

        let orgSearchUrl = config.config?.orgSearchUrl;
        console.log(`🔗 Base URL: ${orgSearchUrl}`);

        if (!orgSearchUrl) {
            console.error('❌ orgSearchUrl not found');
            return;
        }

        const results = {};

        console.log('🔍 Starting university search...');
        for (const uniName of UNIVERSITIES) {
            const result = await page.evaluate(async (baseUrl, term) => {
                try {
                    let searchUrl;
                    // Remove country=US and tags to allow global search
                    // baseUrl usually looks like: https://.../search?tags=...&country=US&...&name=

                    // We need to parse it carefully
                    const urlParts = baseUrl.split('?');
                    const base = urlParts[0];
                    const params = new URLSearchParams(urlParts[1] || '');

                    // Remove restrictive params
                    params.delete('country');
                    params.delete('tags');

                    // Set name param
                    params.set('name', term);

                    searchUrl = `${base}?${params.toString()}`;

                    const response = await fetch(searchUrl);
                    const data = await response.json();
                    return data;
                } catch (e) {
                    return { error: e.toString() };
                }
            }, orgSearchUrl, uniName);

            if (result.error) {
                console.log(`⚠️ Error searching for ${uniName}: ${result.error}`);
                continue;
            }

            const items = Array.isArray(result) ? result : (result.items || []);

            if (items.length > 0) {
                const match = items[0];
                console.log(`✅ Found: ${uniName} -> ${match.id} (${match.name})`);
                results[uniName] = match.id;
            } else {
                console.log(`❌ Not found: ${uniName}`);
            }

            await new Promise(r => setTimeout(r, 500));
        }

        console.log('💾 Saving results to university-ids.json...');
        fs.writeFileSync('university-ids.json', JSON.stringify(results, null, 2));

    } catch (error) {
        console.error('❌ Fatal error:', error);
    } finally {
        await browser.close();
    }
})();
