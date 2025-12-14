
const UNIVERSITIES = require('./universities-data');

console.log(`✅ Loaded ${UNIVERSITIES.length} universities.`);

// Check for duplicates and missing country
const ids = new Set();
const names = new Set();
let duplicates = 0;
let missingCountry = 0;

UNIVERSITIES.forEach(u => {
    if (ids.has(u.sheerId)) {
        console.warn(`⚠️ Duplicate ID: ${u.sheerId} (${u.name})`);
        duplicates++;
    }
    ids.add(u.sheerId);

    if (names.has(u.name)) {
        console.warn(`⚠️ Duplicate Name: ${u.name}`);
        duplicates++;
    }
    names.add(u.name);

    if (!u.country) {
        console.warn(`⚠️ Missing Country: ${u.name}`);
        missingCountry++;
    }
});

if (duplicates === 0) {
    console.log('✅ No duplicates found.');
}

if (missingCountry === 0) {
    console.log('✅ All universities have country data.');
}

// Test random selection
console.log('🎲 Testing random selection:');
for (let i = 0; i < 5; i++) {
    const u = UNIVERSITIES[Math.floor(Math.random() * UNIVERSITIES.length)];
    console.log(`   - ${u.name} (${u.country}) (ID: ${u.sheerId})`);
}
