const axios = require('axios');
const { generateStudentCard, generatePayslip } = require('./generator');
const faker = require('faker');

const SHEERID_API_URL = 'https://services.sheerid.com/rest/v2';

async function verifySheerID(verificationUrl, type = 'student') {
    if (type === 'teacher' || type === 'gpt') {
        // Both Bolt.new (teacher) and ChatGPT (gpt) use the same Teacher verification flow
        return verifyTeacher(verificationUrl);
    } else if (type === 'youtube') {
        return verifyStudent(verificationUrl, 'youtube');
    } else {
        return verifyStudent(verificationUrl, 'spotify');
    }
}

async function verifyStudent(verificationUrl, serviceType = 'spotify') {
    try {
        // 1. Parse Verification ID
        const verificationIdMatch = verificationUrl.match(/verificationId=([a-f0-9]+)/i);
        if (!verificationIdMatch) throw new Error('Invalid Verification URL');
        const verificationId = verificationIdMatch[1];

        console.log(`🔍 Processing ${serviceType} Verification ID: ${verificationId}`);

        // 2. Generate Fake Identity
        const firstName = faker.name.firstName();
        const lastName = faker.name.lastName();
        const email = faker.internet.email(firstName, lastName, 'psu.edu');
        const dob = '2000-01-01'; // Simplified DOB

        const studentInfo = {
            fullName: `${firstName} ${lastName}`,
            dob: dob,
            studentId: Math.floor(Math.random() * 100000000).toString()
        };

        // 3. Generate Document (Screenshot)
        const imageBuffer = await generateStudentCard(studentInfo);

        // 4. Submit Personal Info (Step 1)
        console.log('📤 Submitting personal info...');

        // Metadata differs slightly between services
        const metadata = {
            verificationId: verificationId,
            marketConsentValue: false // Spotify & YouTube both use false
        };

        const step1Response = await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/collectStudentPersonalInfo`, {
            firstName,
            lastName,
            email,
            birthDate: dob,
            organization: {
                id: 2565, // PSU Main Campus
                name: 'Pennsylvania State University-Main Campus'
            },
            deviceFingerprintHash: '686f727269626c656861636b', // Fake hash
            metadata: metadata
        });

        return await handleDocUpload(verificationId, imageBuffer, 'student_card.png');

    } catch (error) {
        console.error(`❌ ${serviceType} Verification failed:`, error.response ? error.response.data : error.message);
        return { success: false, error: error.message };
    }
}

async function verifyTeacher(verificationUrl) {
    try {
        // 1. Parse Verification ID
        const verificationIdMatch = verificationUrl.match(/verificationId=([a-f0-9]+)/i);
        if (!verificationIdMatch) throw new Error('Invalid Verification URL');
        const verificationId = verificationIdMatch[1];

        console.log(`🔍 Processing Teacher Verification ID: ${verificationId}`);

        // 2. Generate Fake Identity
        const firstName = faker.name.firstName();
        const lastName = faker.name.lastName();
        const email = faker.internet.email(firstName, lastName, 'psu.edu');

        const teacherInfo = {
            fullName: `${firstName} ${lastName}`
        };

        // 3. Generate Document (Payslip)
        const imageBuffer = await generatePayslip(teacherInfo);

        // 4. Submit Personal Info (Step 1)
        console.log('📤 Submitting teacher info...');
        const step1Response = await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/collectTeacherPersonalInfo`, {
            firstName,
            lastName,
            email,
            birthDate: "", // Teacher flow often leaves this empty
            phoneNumber: "",
            organization: {
                id: 2565,
                name: 'Pennsylvania State University-Main Campus'
            },
            deviceFingerprintHash: '686f727269626c656861636b',
            metadata: {
                verificationId: verificationId,
                marketConsentValue: true, // Bolt.new uses true
                submissionOptIn: 'By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount',
                flags: '{"doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","include-cvec-field-france-student":"not-labeled-optional","org-search-overlay":"default","org-selected-display":"default"}'
            }
        });

        // Skip SSO if needed
        if (step1Response.data.currentStep === 'sso' || step1Response.data.currentStep === 'collectTeacherPersonalInfo') {
            console.log('⏩ Skipping SSO...');
            try {
                await axios.delete(`${SHEERID_API_URL}/verification/${verificationId}/step/sso`);
            } catch (e) {
                console.log('⚠️ SSO Skip warning (might be already skipped):', e.message);
            }
        }

        // 5. Upload Document (Step 2)
        const uploadResult = await handleDocUpload(verificationId, imageBuffer, 'payslip.png');

        if (uploadResult.success) {
            console.log('⏳ Polling for reward code...');
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

            console.log(`   ...attempt ${i + 1}/${maxAttempts}`);
        } catch (e) {
            console.error('   Polling error:', e.message);
        }
    }
    return null;
}

async function handleDocUpload(verificationId, imageBuffer, fileName) {
    try {
        // 5. Upload Document (Step 2)
        console.log('📤 Uploading document...');

        // Request upload URL
        const docUploadResponse = await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/docUpload`, {
            files: [{
                fileName: fileName,
                mimeType: 'image/png',
                fileSize: imageBuffer.length
            }]
        });

        const uploadUrl = docUploadResponse.data.documents[0].uploadUrl;

        // Upload to S3
        await axios.put(uploadUrl, imageBuffer, {
            headers: { 'Content-Type': 'image/png' }
        });

        // Confirm Upload
        const completeResponse = await axios.post(`${SHEERID_API_URL}/verification/${verificationId}/step/completeDocUpload`);

        console.log('✅ Verification submitted!');
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
