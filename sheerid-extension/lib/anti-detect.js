// Anti-Detection Module for SheerID Verification
// Browser fingerprint spoofing and anti-fraud bypass

const AntiDetect = {
    // Chrome User-Agents (2026)
    USER_AGENTS: [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ],

    RESOLUTIONS: [
        "1920x1080", "1366x768", "1536x864", "1440x900", "1280x720",
        "2560x1440", "1600x900", "1680x1050", "1280x800", "1024x768"
    ],

    TIMEZONES: [-8, -7, -6, -5, -4, -3, 0, 1, 2, 3, 5.5, 8, 9, 10],

    LANGUAGES: ["en-US", "en-GB", "en-CA", "en-AU", "es-ES", "fr-FR", "de-DE", "pt-BR"],

    PLATFORMS: ["Win32", "MacIntel", "Linux x86_64"],

    // Generate realistic browser fingerprint
    generateFingerprint() {
        const components = [
            Date.now().toString(),
            Math.random().toString(),
            this.randomChoice(this.RESOLUTIONS),
            this.randomChoice(this.TIMEZONES).toString(),
            this.randomChoice(this.LANGUAGES),
            this.randomChoice(this.PLATFORMS),
            Math.floor(Math.random() * 16 + 1).toString(), // CPU cores
            Math.floor(Math.random() * 30 + 2).toString(), // Memory GB
            Math.floor(Math.random() * 2).toString() // Touch support
        ];

        return this.hashMD5(components.join('|'));
    },

    // Simple MD5 hash
    hashMD5(str) {
        // Simple hash for fingerprint (not cryptographic)
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16).padStart(32, '0').substring(0, 32);
    },

    // Get random choice from array
    randomChoice(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    },

    // Get browser-like headers for SheerID
    getHeaders(forSheerID = false) {
        const ua = this.randomChoice(this.USER_AGENTS);

        const headers = {
            'User-Agent': ua,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://services.sheerid.com',
            'Referer': 'https://services.sheerid.com/',
            'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        };

        // Add NewRelic headers for SheerID (required)
        if (forSheerID) {
            const traceId = this.generateTraceId();
            headers['Newrelic'] = traceId;
            headers['Traceparent'] = `00-${traceId}-${this.generateSpanId()}-01`;
            headers['Tracestate'] = `@nr=0-0-0-0-0-0-0-0-${Date.now()}`;
        }

        return headers;
    },

    // Generate NewRelic trace ID
    generateTraceId() {
        return Array.from({ length: 32 }, () =>
            Math.floor(Math.random() * 16).toString(16)
        ).join('');
    },

    // Generate span ID
    generateSpanId() {
        return Array.from({ length: 16 }, () =>
            Math.floor(Math.random() * 16).toString(16)
        ).join('');
    },

    // Random delay (gamma distribution for human-like timing)
    async randomDelay(min = 300, max = 800) {
        const delay = Math.floor(Math.random() * (max - min) + min);
        await new Promise(resolve => setTimeout(resolve, delay));
    },

    // Generate realistic name
    generateName() {
        const firstNames = [
            "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
            "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
            "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
            "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Emma", "Olivia", "Ava"
        ];
        const lastNames = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker"
        ];

        return {
            first: this.randomChoice(firstNames),
            last: this.randomChoice(lastNames)
        };
    },

    // Generate email from name and domain
    generateEmail(firstName, lastName, domain) {
        const patterns = [
            `${firstName[0].toLowerCase()}${lastName.toLowerCase()}${Math.floor(Math.random() * 900 + 100)}`,
            `${firstName.toLowerCase()}.${lastName.toLowerCase()}${Math.floor(Math.random() * 90 + 10)}`,
            `${lastName.toLowerCase()}${firstName[0].toLowerCase()}${Math.floor(Math.random() * 900 + 100)}`
        ];
        return `${this.randomChoice(patterns)}@${domain}`;
    },

    // Generate birth date (18-26 years old for students)
    generateBirthDate(minAge = 18, maxAge = 26) {
        const year = new Date().getFullYear() - Math.floor(Math.random() * (maxAge - minAge + 1) + minAge);
        const month = Math.floor(Math.random() * 12 + 1);
        const day = Math.floor(Math.random() * 28 + 1);
        return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
    },

    // Generate discharge date (for veterans - last 12 months)
    generateDischargeDate() {
        const today = new Date();
        const daysAgo = Math.floor(Math.random() * 365);
        const date = new Date(today.getTime() - daysAgo * 24 * 60 * 60 * 1000);
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
};

