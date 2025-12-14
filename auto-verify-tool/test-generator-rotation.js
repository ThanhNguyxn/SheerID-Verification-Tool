
const { generateStudentCard, closeBrowser } = require('./generator');
const UNIVERSITIES = require('./universities-data');
const fs = require('fs');

// Mock global.emitLog for standalone testing
global.emitLog = (msg) => console.log(`[LOG] ${msg}`);

(async () => {
    console.log('🚀 Starting Generator Rotation Test...');

    // Select a few diverse universities to test
    const testCases = [
        UNIVERSITIES.find(u => u.name === 'Harvard University'), // US
        UNIVERSITIES.find(u => u.name === 'University of Toronto'), // Canada
        UNIVERSITIES.find(u => u.name === 'University of Oxford'), // UK
        UNIVERSITIES.find(u => u.name === 'Hanoi University of Science and Technology') // Vietnam
    ];

    for (const uni of testCases) {
        if (!uni) continue;
        console.log(`\n🧪 Testing: ${uni.name} (${uni.country})`);

        const studentInfo = {
            fullName: 'Test Student',
            university: uni.name,
            studentId: '12345678',
            dob: '2000-01-01'
        };

        try {
            const buffer = await generateStudentCard(studentInfo);
            const fileName = `test_card_${uni.shortName.replace(/[\s\/\\]+/g, '_')}.png`;
            fs.writeFileSync(fileName, buffer);
            console.log(`✅ Success! Saved to ${fileName}`);
        } catch (error) {
            console.error(`❌ Failed: ${error.message}`);
        }

        // Small delay
        await new Promise(r => setTimeout(r, 2000));
    }

    await closeBrowser();
    console.log('\n🏁 Test Complete.');
})();
