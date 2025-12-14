const axios = require('axios');
const { generateStudentCard, generatePayslip, generateTeacherCard, generateDocumentsParallel, closeBrowser } = require('./generator');
const faker = require('faker');
const PDFDocument = require('pdfkit');
const UNIVERSITIES = require('./universities-data');

function getRandomUniversity(country = null) {
    let candidates = UNIVERSITIES;
    if (country) {
        candidates = UNIVERSITIES.filter(u => u.country === country);
    }
    if (candidates.length === 0) return UNIVERSITIES[Math.floor(Math.random() * UNIVERSITIES.length)];
    return candidates[Math.floor(Math.random() * candidates.length)];
}

const SHEERID_API_URL = 'https://services.sheerid.com/rest/v2';

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
    try {
        // 1. Parse Verification ID
        const verificationIdMatch = verificationUrl.match(/verificationId=([a-f0-9]+)/i);
        if (!verificationIdMatch) throw new Error('Invalid Verification URL');
        const verificationId = verificationIdMatch[1];

        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog(`🔍 SheerID ${serviceType.toUpperCase()} Student Verification`);
        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog(`📋 Verification ID: ${verificationId}`);

        // 2. Generate Fake Identity
        global.emitLog('');
        global.emitLog('📝 [Step 1/4] Generating student identity...');
        const firstName = faker.name.firstName();
        const lastName = faker.name.lastName();
        const email = faker.internet.email(firstName, lastName, 'psu.edu');
        const dob = faker.date.between('1998-01-01', '2004-12-31').toISOString().split('T')[0];

        // Select a random university for this verification
        // Prioritize USA (80% chance)
        const prioritizeUS = Math.random() < 0.8;
        const university = prioritizeUS ? getRandomUniversity('USA') : getRandomUniversity();
        global.emitLog(`🎓 Selected University: ${university.name} (ID: ${university.sheerId})`);

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

        // 4. Submit Personal Info (collectStudentPersonalInfo)
        global.emitLog('');
        global.emitLog('📤 [Step 3/4] Submitting student info to SheerID...');
        const step1Response = await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/collectStudentPersonalInfo`, {
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
            deviceFingerprintHash: faker.datatype.hexaDecimal(32).replace('0x', ''),
            locale: 'en-US',
            metadata: {
                verificationId: verificationId,
                marketConsentValue: false,
                refererUrl: `https://services.sheerid.com/verify/67c8c14f5f17a83b745e3f82/?verificationId=${verificationId}`,
                flags: '{"collect-info-step-email-first":"default","doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","font-size":"default","include-cvec-field-france-student":"not-labeled-optional"}',
                submissionOptIn: 'By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount'
            }
        });

        global.emitLog(`   └─ ✅ Step 3 completed: ${step1Response.data.currentStep}`);

        // Skip SSO if needed
        if (step1Response.data.currentStep === 'sso' || step1Response.data.currentStep === 'collectStudentPersonalInfo') {
            global.emitLog('');
            global.emitLog('⏩ Skipping SSO verification...');
            try {
                const ssoResponse = await axios.delete(`${SHEERID_API_URL}/verification/${verificationId}/step/sso`);
                global.emitLog(`   └─ ✅ SSO skipped: ${ssoResponse.data.currentStep}`);
            } catch (e) {
                global.emitLog(`   └─ ⚠️ SSO skip warning: ${e.message}`);
            }
        }

        return await handleDocUpload(verificationId, imageBuffer, 'student_card.png');

    } catch (error) {
        console.error(`❌ ${serviceType} Verification failed:`, error.response ? error.response.data : error.message);
        global.emitLog(`❌ Error: ${error.response ? JSON.stringify(error.response.data) : error.message}`);
        return { success: false, error: error.message };
    }
}

async function verifyTeacher(verificationUrl) {
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

        // 2. Generate Fake Identity
        global.emitLog('');
        global.emitLog('📝 [Step 1/4] Generating teacher identity...');
        const firstName = faker.name.firstName();
        const lastName = faker.name.lastName();
        const email = faker.internet.email(firstName, lastName, 'psu.edu');

        // Select a random university for this verification (Teachers: US Only)
        const university = getRandomUniversity('USA');
        global.emitLog(`🎓 Selected University: ${university.name} (ID: ${university.sheerId})`);

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

        // 4. Submit Personal Info (collectTeacherPersonalInfo) - Bolt.new style
        global.emitLog('');
        global.emitLog('📤 [Step 3/4] Submitting teacher info to SheerID...');
        const step1Response = await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/collectTeacherPersonalInfo`, {
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
            deviceFingerprintHash: faker.datatype.hexaDecimal(32).replace('0x', ''),
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

        global.emitLog(`   └─ ✅ Step 3 completed: ${step1Response.data.currentStep}`);

        // Skip SSO if needed
        if (step1Response.data.currentStep === 'sso' || step1Response.data.currentStep === 'collectTeacherPersonalInfo') {
            global.emitLog('');
            global.emitLog('⏩ Skipping SSO verification...');
            try {
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
            if (rewardCode) {
                return { success: true, message: 'Verification successful!', rewardCode: rewardCode };
            } else {
                return { success: true, message: 'Verification submitted. Please check your email for the code.' };
            }
        }

        return uploadResult;

    } catch (error) {
        console.error('❌ Teacher Verification failed:', error.response ? error.response.data : error.message);
        global.emitLog(`❌ Error: ${error.response ? JSON.stringify(error.response.data) : error.message}`);
        return { success: false, error: error.message };
    }
}

async function verifyGPT(verificationUrl) {
    try {
        // 1. Parse Verification ID
        const verificationIdMatch = verificationUrl.match(/verificationId=([a-f0-9]+)/i);
        if (!verificationIdMatch) throw new Error('Invalid Verification URL');
        const verificationId = verificationIdMatch[1];

        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog('🔍 SheerID CHATGPT TEACHER Verification (K12 Style)');
        global.emitLog('═══════════════════════════════════════════════════════════');
        global.emitLog(`📋 Verification ID: ${verificationId}`);

        // 2. Generate Fake Identity with birthDate (required for k12)
        global.emitLog('');
        global.emitLog('📝 [Step 1/5] Generating teacher identity...');
        const firstName = faker.name.firstName();
        const lastName = faker.name.lastName();
        const email = faker.internet.email(firstName, lastName, 'springfield.k12.or.us');
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
                id: 3995910,
                idExtended: '3995910',
                name: 'Springfield High School (Springfield, OR)'
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

module.exports = { verifySheerID };
