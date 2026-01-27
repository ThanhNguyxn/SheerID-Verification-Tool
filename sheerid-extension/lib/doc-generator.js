// Document Generator Module
// Generate realistic student ID cards, transcripts, teacher badges using Canvas API

const DocGenerator = {
    // Color schemes for variety
    COLOR_SCHEMES: [
        { primary: '#003366', secondary: '#ffffff', accent: '#0066cc' }, // Blue
        { primary: '#8b0000', secondary: '#ffffff', accent: '#dc143c' }, // Red
        { primary: '#004d00', secondary: '#ffffff', accent: '#228b22' }, // Green
        { primary: '#4b0082', secondary: '#ffffff', accent: '#9370db' }, // Purple
        { primary: '#8b4513', secondary: '#ffffff', accent: '#d2691e' }, // Brown
        { primary: '#000080', secondary: '#ffffff', accent: '#4169e1' }  // Navy
    ],

    // Generate Student ID Card
    async generateStudentID(firstName, lastName, school, options = {}) {
        const width = 650;
        const height = 400;
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');

        // Select random color scheme
        const colors = this.COLOR_SCHEMES[Math.floor(Math.random() * this.COLOR_SCHEMES.length)];

        // Add noise for uniqueness
        if (options.addNoise !== false) {
            this.addNoise(ctx, width, height);
        }

        // Background
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, width, height);

        // Header
        ctx.fillStyle = colors.primary;
        ctx.fillRect(0, 0, width, 60);

        // Title
        ctx.fillStyle = colors.secondary;
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('STUDENT IDENTIFICATION CARD', width / 2, 38);

        // School name
        ctx.fillStyle = colors.primary;
        ctx.font = 'bold 18px Arial';
        ctx.fillText(school.substring(0, 50), width / 2, 95);

        // Photo placeholder
        ctx.strokeStyle = '#b4b4b4';
        ctx.lineWidth = 2;
        ctx.strokeRect(30, 120, 120, 160);
        ctx.fillStyle = '#e0e0e0';
        ctx.fillRect(32, 122, 116, 156);
        ctx.fillStyle = '#b4b4b4';
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('PHOTO', 90, 205);

        // Student info
        const studentId = `STU${Math.floor(Math.random() * 900000 + 100000)}`;
        const year = new Date().getFullYear();
        const info = [
            `Name: ${firstName} ${lastName}`,
            `ID: ${studentId}`,
            `Status: Full-time Student`,
            `Major: Computer Science`,
            `Valid: ${year}-${year + 1}`
        ];

        ctx.fillStyle = '#333333';
        ctx.font = '18px Arial';
        ctx.textAlign = 'left';
        let y = 135;
        for (const line of info) {
            ctx.fillText(line, 175, y);
            y += 28;
        }

        // Barcode
        ctx.fillStyle = '#000000';
        for (let i = 0; i < 20; i++) {
            const x = 480 + i * 7;
            const h = 30 + Math.random() * 20;
            ctx.fillRect(x, 280, 3, h);
        }

        // Footer
        ctx.fillStyle = colors.primary;
        ctx.fillRect(0, height - 40, width, 40);
        ctx.fillStyle = colors.secondary;
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Property of University - If found, please return', width / 2, height - 18);

        // Convert to blob
        return new Promise((resolve) => {
            canvas.toBlob(resolve, 'image/png');
        });
    },

    // Generate Transcript
    async generateTranscript(firstName, lastName, school, options = {}) {
        const width = 850;
        const height = 1100;
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');

        const colors = this.COLOR_SCHEMES[Math.floor(Math.random() * this.COLOR_SCHEMES.length)];

        // Add noise
        if (options.addNoise !== false) {
            this.addNoise(ctx, width, height);
        }

        // Background
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, width, height);

        // Header
        ctx.fillStyle = colors.primary;
        ctx.fillRect(0, 0, width, 100);

        // School name
        ctx.fillStyle = colors.secondary;
        ctx.font = 'bold 28px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(school, width / 2, 40);
        ctx.font = '18px Arial';
        ctx.fillText('OFFICIAL ACADEMIC TRANSCRIPT', width / 2, 75);

        // Student info
        ctx.fillStyle = '#333333';
        ctx.font = 'bold 16px Arial';
        ctx.textAlign = 'left';
        let y = 150;
        ctx.fillText(`Student: ${firstName} ${lastName}`, 50, y);
        y += 30;
        ctx.fillText(`Student ID: STU${Math.floor(Math.random() * 900000 + 100000)}`, 50, y);
        y += 30;
        ctx.fillText(`Date of Birth: ${AntiDetect.generateBirthDate()}`, 50, y);
        y += 30;
        ctx.fillText(`Major: Computer Science`, 50, y);

        // Courses table
        y += 60;
        ctx.font = 'bold 14px Arial';
        ctx.fillText('FALL 2023 - SPRING 2024', 50, y);
        y += 30;

        const courses = [
            ['CS 101', 'Introduction to Programming', '4', 'A'],
            ['CS 201', 'Data Structures', '4', 'A-'],
            ['MATH 201', 'Calculus II', '3', 'B+'],
            ['ENG 102', 'English Composition', '3', 'A'],
            ['CS 301', 'Algorithms', '4', 'A'],
            ['CS 305', 'Database Systems', '3', 'A-']
        ];

        ctx.font = '12px Arial';
        const colWidths = [100, 350, 80, 80];
        let x = 50;

        // Table header
        ctx.fillStyle = colors.primary;
        ctx.fillRect(50, y - 20, 700, 25);
        ctx.fillStyle = colors.secondary;
        ctx.fillText('Course', x + 10, y - 3);
        ctx.fillText('Title', x + colWidths[0] + 10, y - 3);
        ctx.fillText('Credits', x + colWidths[0] + colWidths[1] + 10, y - 3);
        ctx.fillText('Grade', x + colWidths[0] + colWidths[1] + colWidths[2] + 10, y - 3);

        y += 10;
        ctx.fillStyle = '#333333';

        for (const [code, title, credits, grade] of courses) {
            y += 25;
            ctx.fillText(code, x + 10, y);
            ctx.fillText(title, x + colWidths[0] + 10, y);
            ctx.fillText(credits, x + colWidths[0] + colWidths[1] + 10, y);
            ctx.fillText(grade, x + colWidths[0] + colWidths[1] + colWidths[2] + 10, y);
        }

        // GPA
        y += 50;
        ctx.font = 'bold 14px Arial';
        ctx.fillText('Cumulative GPA: 3.75', 50, y);

        // Footer
        y = height - 100;
        ctx.fillStyle = '#666666';
        ctx.font = '12px Arial';
        ctx.fillText('This is an official transcript. Any alterations void this document.', 50, y);

        return new Promise((resolve) => {
            canvas.toBlob(resolve, 'image/png');
        });
    },

    // Generate Teacher Badge
    async generateTeacherBadge(firstName, lastName, school, options = {}) {
        const width = 600;
        const height = 400;
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');

        const colors = this.COLOR_SCHEMES[Math.floor(Math.random() * this.COLOR_SCHEMES.length)];

        // Add noise
        if (options.addNoise !== false) {
            this.addNoise(ctx, width, height);
        }

        // Background
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, width, height);

        // Header
        ctx.fillStyle = colors.primary;
        ctx.fillRect(0, 0, width, 80);

        // Title
        ctx.fillStyle = colors.secondary;
        ctx.font = 'bold 26px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('FACULTY IDENTIFICATION', width / 2, 50);

        // School name
        ctx.fillStyle = colors.primary;
        ctx.font = 'bold 18px Arial';
        ctx.fillText(school.substring(0, 45), width / 2, 120);

        // Photo placeholder
        ctx.strokeStyle = '#b4b4b4';
        ctx.lineWidth = 2;
        ctx.strokeRect(30, 150, 140, 180);
        ctx.fillStyle = '#e0e0e0';
        ctx.fillRect(32, 152, 136, 176);
        ctx.fillStyle = '#b4b4b4';
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('PHOTO', 100, 245);

        // Teacher info
        const teacherId = `TCH${Math.floor(Math.random() * 90000 + 10000)}`;
        const year = new Date().getFullYear();
        const info = [
            `Name: ${firstName} ${lastName}`,
            `ID: ${teacherId}`,
            `Position: Faculty`,
            `Department: Computer Science`,
            `Valid: ${year}-${year + 1}`
        ];

        ctx.fillStyle = '#333333';
        ctx.font = '18px Arial';
        ctx.textAlign = 'left';
        let y = 165;
        for (const line of info) {
            ctx.fillText(line, 200, y);
            y += 32;
        }

        // Footer
        ctx.fillStyle = colors.primary;
        ctx.fillRect(0, height - 50, width, 50);
        ctx.fillStyle = colors.secondary;
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('This badge is property of the institution', width / 2, height - 25);

        return new Promise((resolve) => {
            canvas.toBlob(resolve, 'image/png');
        });
    },

    // Add random noise to canvas for uniqueness
    addNoise(ctx, width, height) {
        const imageData = ctx.createImageData(width, height);
        const data = imageData.data;

        for (let i = 0; i < data.length; i += 4) {
            if (Math.random() < 0.02) { // 2% noise
                const noise = Math.random() * 30;
                data[i] = data[i + 1] = data[i + 2] = 255 - noise;
                data[i + 3] = 255;
            }
        }

        ctx.putImageData(imageData, 0, 0);
    },

    // Convert blob to base64
    async blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DocGenerator;
}
