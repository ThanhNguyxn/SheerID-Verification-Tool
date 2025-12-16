/**
 * K12 Teachers Data for GPT Verification
 * VERIFIED real teacher names from public school staff directories
 * Email patterns based on school domain conventions
 * 
 * Sources:
 * - Bronx Science: bxscience.edu/apps/staff/
 * - Staten Island Tech: siths.org/staff-directory
 * - Townsend Harris: thhs.qc.edu/faculty-and-staff/
 * - Thomas Jefferson: tjhsst.fcps.edu
 * - Whitney Young: wyoung.org (IHSA listing)
 * - Gretchen Whitney: whitneyhs.us/staff
 */

const K12_TEACHERS = {
    // =====================================================
    // BRONX HIGH SCHOOL OF SCIENCE (Verified from bxscience.edu)
    // Email pattern: firstinitial + lastname @schools.nyc.gov
    // =====================================================
    "156251": {
        schoolName: "Bronx High School Of Science",
        emailDomain: "schools.nyc.gov",
        emailPattern: "firstInitialLastName", // rhoyle@schools.nyc.gov
        teachers: [
            { firstName: "Rachel", lastName: "Hoyle", position: "Principal" },
            { firstName: "Alessandra", lastName: "Zullo Casale", position: "Assistant Principal - English" },
            { firstName: "David", lastName: "Colchamiro", position: "Assistant Principal - Social Studies" },
            { firstName: "Phoebe", lastName: "Cooper", position: "Assistant Principal" },
            { firstName: "Allison", lastName: "Davis", position: "Assistant Principal - Biology" },
            { firstName: "Kathleen", lastName: "Lyons", position: "Assistant Principal - Mathematics" },
            { firstName: "Michael", lastName: "McGrath", position: "Assistant Principal - Physical Education" },
            { firstName: "Colin", lastName: "Morrell", position: "Assistant Principal - Organization" },
            { firstName: "Andrew", lastName: "Nasser", position: "Assistant Principal - Pupil Personnel Services" },
            { firstName: "Bing", lastName: "Qiu", position: "Assistant Principal - World Languages" }
        ]
    },

    // =====================================================
    // STATEN ISLAND TECHNICAL HIGH SCHOOL (Verified from siths.org)
    // Email pattern: firstinitial + lastname @schools.nyc.gov
    // =====================================================
    "155770": {
        schoolName: "Staten Island Technical High School",
        emailDomain: "schools.nyc.gov",
        emailPattern: "firstInitialLastName",
        teachers: [
            { firstName: "Mark", lastName: "Erlenwein", position: "Principal" },
            { firstName: "John", lastName: "Davis", position: "Assistant Principal - Organization" },
            { firstName: "Peter", lastName: "Dellegrazie", position: "Assistant Principal - Mathematics" },
            { firstName: "Alexis", lastName: "Kirschbaum", position: "Assistant Principal - Pupil Personnel Services" },
            { firstName: "Joseph", lastName: "Manzo", position: "Assistant Principal - Social Studies" },
            { firstName: "Felicia", lastName: "Rodriguez", position: "Assistant Principal - Science" },
            { firstName: "Noelle", lastName: "Sanguinedo", position: "Assistant Principal - English" },
            { firstName: "Lisa", lastName: "Asher", position: "Teacher - Mathematics" },
            { firstName: "James", lastName: "Aurelia", position: "Teacher - Mathematics" },
            { firstName: "Alison", lastName: "Barone", position: "Teacher - Technology" },
            { firstName: "Bianca", lastName: "Brandon", position: "Teacher - Science" },
            { firstName: "Heather", lastName: "Brown", position: "Teacher - Performing Arts" },
            { firstName: "John", lastName: "Callahan", position: "Teacher - Russian" },
            { firstName: "Erin", lastName: "Carr", position: "Teacher - History" }
        ]
    },

    // =====================================================
    // TOWNSEND HARRIS HIGH SCHOOL (Verified from thhs.qc.edu)
    // Email pattern: firstinitial + lastname @schools.nyc.gov
    // =====================================================
    "158162": {
        schoolName: "Townsend Harris High School",
        emailDomain: "schools.nyc.gov",
        emailPattern: "firstInitialLastName",
        teachers: [
            { firstName: "Brian", lastName: "Condon", position: "Principal" },
            { firstName: "Shikira", lastName: "Chang", position: "Assistant Principal - Guidance" },
            { firstName: "Abid", lastName: "Choudhury", position: "Assistant Principal - STEM" },
            { firstName: "Ellen", lastName: "Fee", position: "Assistant Principal - Organization" },
            { firstName: "Rafal", lastName: "Olechowski", position: "Assistant Principal - World Languages" },
            { firstName: "Alanna", lastName: "Rice", position: "Assistant Principal - Instructional Support" },
            { firstName: "Anthony", lastName: "Balone", position: "Teacher - English" },
            { firstName: "Jude", lastName: "Binda", position: "Teacher - English" },
            { firstName: "Brian", lastName: "Brewer", position: "Teacher - English" },
            { firstName: "Christine", lastName: "Duffy", position: "Teacher - English" },
            { firstName: "Charlene", lastName: "Garklavs", position: "Teacher - English" },
            { firstName: "Ray", lastName: "Adamkiewicz", position: "Teacher - Physical Education" },
            { firstName: "Lauren", lastName: "Caiaccia", position: "Coach - Girls Basketball" }
        ]
    },

    // =====================================================
    // THOMAS JEFFERSON HIGH SCHOOL FOR SCIENCE AND TECHNOLOGY (Verified from tjhsst.edu)
    // Email pattern: firstname.lastname @fcps.edu
    // =====================================================
    "3704245": {
        schoolName: "Thomas Jefferson High School For Science And Technology",
        emailDomain: "fcps.edu",
        emailPattern: "firstNameDotLastName",
        teachers: [
            { firstName: "Michael", lastName: "Mukai", position: "Principal" },
            { firstName: "Brandon", lastName: "Kosatka", position: "Director - Student Services" },
            { firstName: "Shawn", lastName: "Frank", position: "Assistant Principal" },
            { firstName: "Pam", lastName: "Gravitte", position: "Assistant Principal" },
            { firstName: "Gary", lastName: "Grosicki", position: "Assistant Principal" },
            { firstName: "Anne", lastName: "Applin", position: "Head Librarian" },
            { firstName: "Isaac", lastName: "Carey", position: "Department Chair - Math and Computer Science" },
            { firstName: "Brian", lastName: "Field", position: "Department Chair - Social Studies" },
            { firstName: "LeeAnn", lastName: "Hennig", position: "Department Chair - Science and Technology" },
            { firstName: "Suzette", lastName: "Henry", position: "Department Chair - English" },
            { firstName: "Mark", lastName: "Hannum", position: "Mentorship Director" },
            { firstName: "Fred", lastName: "Lampazzi", position: "Mentorship Coordinator" }
        ]
    },

    // =====================================================
    // WHITNEY M YOUNG MAGNET HIGH SCHOOL (Verified from IHSA listing)
    // Email pattern: firstinitial + lastname @cps.edu
    // =====================================================
    "3521074": {
        schoolName: "Whitney M Young Magnet High School",
        emailDomain: "cps.edu",
        emailPattern: "firstInitialLastName",
        teachers: [
            { firstName: "Chris", lastName: "Cassidy", position: "Athletic Director" },
            { firstName: "Rickey", lastName: "Harris", position: "Administrator" },
            { firstName: "Valerie", lastName: "Spann", position: "Administrator" },
            { firstName: "Matthew", lastName: "Castle", position: "Coach" },
            { firstName: "Nick", lastName: "Maksa", position: "Teacher - Physical Education" },
            { firstName: "Eric", lastName: "Wiegmann", position: "Coach" },
            { firstName: "Caneka", lastName: "Davis", position: "Teacher" },
            { firstName: "Vlad", lastName: "Stankov", position: "Teacher" },
            { firstName: "Deborah", lastName: "Johnson", position: "Teacher" },
            { firstName: "Mike", lastName: "Hinrichs", position: "Coach - Girls Softball" },
            { firstName: "Gerald", lastName: "Winston", position: "Teacher" },
            { firstName: "Tonay", lastName: "Tucker", position: "Teacher" }
        ]
    },

    // =====================================================
    // GRETCHEN WHITNEY HIGH SCHOOL (Verified from whitneyhs.us)
    // Email pattern: firstname.lastname @abcusd.us
    // =====================================================
    "3539252": {
        schoolName: "Gretchen Whitney High School",
        emailDomain: "abcusd.us",
        emailPattern: "firstNameDotLastName",
        teachers: [
            { firstName: "Tuesday", lastName: "Stoffers", position: "Principal" },
            { firstName: "Joseph", lastName: "Allard", position: "Teacher" },
            { firstName: "Nancy", lastName: "Barry", position: "Teacher" },
            { firstName: "Paul", lastName: "Bender", position: "Teacher" },
            { firstName: "Carolina", lastName: "Bojorquez", position: "Teacher" },
            { firstName: "La Monica", lastName: "Bryson", position: "Teacher" },
            { firstName: "Cindy", lastName: "Carlson", position: "Teacher" },
            { firstName: "Stephen", lastName: "Clements", position: "Teacher" },
            { firstName: "Daryl", lastName: "David", position: "Teacher" },
            { firstName: "Jennifer", lastName: "Flores", position: "Teacher" },
            { firstName: "Cassandra", lastName: "Alves", position: "Counselor" },
            { firstName: "Valerie", lastName: "Diaz", position: "Counselor" },
            { firstName: "Irene", lastName: "Ballesteros", position: "Wellness Counselor" }
        ]
    }
};

/**
 * Generate email for a teacher based on school email pattern
 * @param {Object} teacher - Teacher object with firstName, lastName
 * @param {string} schoolId - SheerID school ID
 * @returns {string} Generated email
 */
function generateEmail(teacher, schoolId) {
    const school = K12_TEACHERS[schoolId];
    if (!school) return null;

    const firstName = teacher.firstName.replace(/\s/g, '');
    const lastName = teacher.lastName.replace(/\s/g, '');

    switch (school.emailPattern) {
        case "firstInitialLastName":
            // rhoyle@schools.nyc.gov
            return `${firstName.charAt(0).toLowerCase()}${lastName.toLowerCase()}@${school.emailDomain}`;
        case "firstNameDotLastName":
            // michael.mukai@fcps.edu
            return `${firstName.toLowerCase()}.${lastName.toLowerCase()}@${school.emailDomain}`;
        default:
            return null;
    }
}

/**
 * Get random teacher from a school for GPT K12 verification
 * @param {string} schoolId - SheerID school ID
 * @returns {Object} Random teacher with name, position, and generated email
 */
function getRandomTeacher(schoolId) {
    const school = K12_TEACHERS[schoolId];
    if (!school || !school.teachers || school.teachers.length === 0) return null;

    const teacher = school.teachers[Math.floor(Math.random() * school.teachers.length)];
    return {
        firstName: teacher.firstName,
        lastName: teacher.lastName,
        fullName: `${teacher.firstName} ${teacher.lastName}`,
        position: teacher.position,
        email: generateEmail(teacher, schoolId),
        schoolName: school.schoolName
    };
}

/**
 * Get all available school IDs with verified teachers
 * @returns {Array} Array of school IDs
 */
function getAvailableSchools() {
    return Object.keys(K12_TEACHERS).map(id => ({
        id,
        name: K12_TEACHERS[id].schoolName,
        teacherCount: K12_TEACHERS[id].teachers.length
    }));
}

/**
 * Get random teacher from any verified school
 * @returns {Object} Random teacher with school info
 */
function getRandomTeacherFromAnySchool() {
    const schoolIds = Object.keys(K12_TEACHERS);
    const randomSchoolId = schoolIds[Math.floor(Math.random() * schoolIds.length)];
    return getRandomTeacher(randomSchoolId);
}

module.exports = {
    K12_TEACHERS,
    generateEmail,
    getRandomTeacher,
    getAvailableSchools,
    getRandomTeacherFromAnySchool
};
