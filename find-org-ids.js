
const axios = require('axios');
const fs = require('fs');

// List of universities to search for
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
    "Northwestern University"
];

async function findOrgIds() {
    console.log('🔍 Searching for SheerID Organization IDs...');
    const results = [];

    for (const uniName of UNIVERSITIES) {
        try {
            // This is a common SheerID endpoint for organization search
            // We might need to adjust the URL if this one doesn't work
            const response = await axios.get(`https://services.sheerid.com/rest/v2/organization`, {
                params: {
                    searchTerm: uniName,
                    type: 'UNIVERSITY' // Filter by university type
                }
            });

            if (response.data && response.data.length > 0) {
                // Find the best match
                const match = response.data[0]; // Take the first one for now
                console.log(`✅ Found: ${uniName} -> ID: ${match.id} (${match.name})`);
                results.push({
                    name: uniName,
                    sheerIdName: match.name,
                    id: match.id
                });
            } else {
                console.log(`❌ Not Found: ${uniName}`);
            }
        } catch (error) {
            console.error(`⚠️ Error searching for ${uniName}:`, error.message);
        }

        // Add a small delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    console.log('\n📋 Results Summary:');
    console.log(JSON.stringify(results, null, 2));
}

findOrgIds();
