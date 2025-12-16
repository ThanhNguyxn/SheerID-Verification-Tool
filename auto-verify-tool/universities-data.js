
// University Database with SheerID Organization IDs
// Merged from payslip-generator and fetched IDs
// Includes Country for student-card-generator UI navigation

const UNIVERSITIES = [
    // USA
    {
        name: "Pennsylvania State University-Main Campus",
        sheerId: 2565,
        country: "USA",
        shortName: "Penn State",
        domain: "psu.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/psu.png",
        color: "#041E42",
        address: "University Park, PA 16802, USA",
        departments: ["Computer Science", "Engineering", "Business", "Education", "Agriculture"]
    },
    {
        name: "Massachusetts Institute of Technology",
        sheerId: 1953,
        country: "USA",
        shortName: "MIT",
        domain: "mit.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/mit_official.svg",
        color: "#A31F34",
        address: "77 Massachusetts Ave, Cambridge, MA 02139, USA",
        departments: ["Computer Science", "Mechanical Engineering", "Physics", "Mathematics", "Electrical Engineering"]
    },
    {
        name: "Harvard University",
        sheerId: 1426,
        country: "USA",
        shortName: "Harvard",
        domain: "harvard.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/harvard.svg",
        color: "#A51C30",
        address: "Cambridge, MA 02138, USA",
        departments: ["Law", "Medicine", "Business", "Political Science", "Economics"]
    },
    {
        name: "Stanford University",
        sheerId: 3113,
        country: "USA",
        shortName: "Stanford",
        domain: "stanford.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/stanford.svg",
        color: "#8C1515",
        address: "450 Serra Mall, Stanford, CA 94305, USA",
        departments: ["Computer Science", "Engineering", "Business", "Law", "Medicine"]
    },
    {
        name: "University of California, Berkeley",
        sheerId: 3491,
        country: "USA",
        shortName: "UC Berkeley",
        domain: "berkeley.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/berkeley.svg",
        color: "#003262",
        address: "Berkeley, CA 94720, USA",
        departments: ["Computer Science", "Economics", "Engineering", "Business", "Political Science"]
    },
    {
        name: "Yale University",
        sheerId: 590759,
        country: "USA",
        shortName: "Yale",
        domain: "yale.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/yale.svg",
        color: "#00356B",
        address: "New Haven, CT 06520, USA",
        departments: ["Law", "History", "Economics", "Political Science", "Psychology"]
    },
    {
        name: "Princeton University",
        sheerId: 2626,
        country: "USA",
        shortName: "Princeton",
        domain: "princeton.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/princeton.png",
        color: "#FF6600",
        address: "Princeton, NJ 08544, USA",
        departments: ["Mathematics", "Physics", "Economics", "Computer Science", "Public Policy"]
    },
    {
        name: "Columbia University",
        sheerId: 698,
        country: "USA",
        shortName: "Columbia",
        domain: "columbia.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/columbia.png",
        color: "#B9D9EB",
        address: "116th St & Broadway, New York, NY 10027, USA",
        departments: ["Business", "Law", "Journalism", "Medicine", "International Relations"]
    },
    {
        name: "New York University",
        sheerId: 2285,
        country: "USA",
        shortName: "NYU",
        domain: "nyu.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/nyu.png",
        color: "#57068C",
        address: "70 Washington Square S, New York, NY 10012, USA",
        departments: ["Business", "Film", "Law", "Arts", "Media"]
    },
    {
        name: "University of California, Los Angeles",
        sheerId: 3499,
        country: "USA",
        shortName: "UCLA",
        domain: "ucla.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/ucla.png",
        color: "#2774AE",
        address: "Los Angeles, CA 90095, USA",
        departments: ["Film", "Business", "Engineering", "Medicine", "Psychology"]
    },
    {
        name: "University of Chicago",
        sheerId: 3508,
        country: "USA",
        shortName: "UChicago",
        domain: "uchicago.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/uchicago.png",
        color: "#800000",
        address: "5801 S Ellis Ave, Chicago, IL 60637, USA",
        departments: ["Economics", "Law", "Business", "Physics", "Political Science"]
    },
    {
        name: "Duke University",
        sheerId: 943,
        country: "USA",
        shortName: "Duke",
        domain: "duke.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/duke.png",
        color: "#003087",
        address: "Durham, NC 27708, USA",
        departments: ["Medicine", "Business", "Law", "Engineering", "Public Policy"]
    },
    {
        name: "Cornell University",
        sheerId: 751,
        country: "USA",
        shortName: "Cornell",
        domain: "cornell.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/cornell.png",
        color: "#B31B1B",
        address: "Ithaca, NY 14850, USA",
        departments: ["Engineering", "Hotel Administration", "Agriculture", "Business", "Computer Science"]
    },
    {
        name: "Northwestern University",
        sheerId: 2420,
        country: "USA",
        shortName: "Northwestern",
        domain: "northwestern.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/northwestern.png",
        color: "#4E2A84",
        address: "Evanston, IL 60208, USA",
        departments: ["Journalism", "Business", "Engineering", "Law", "Medicine"]
    },
    // Canada
    {
        name: "University of Toronto",
        sheerId: 328355,
        country: "Canada",
        shortName: "U of T",
        domain: "utoronto.ca",
        address: "Toronto, ON, Canada"
    },
    {
        name: "McGill University",
        sheerId: 4782066,
        country: "Canada",
        shortName: "McGill",
        domain: "mcgill.ca",
        address: "Montreal, QC, Canada"
    },
    {
        name: "University of British Columbia",
        sheerId: 328315,
        country: "Canada",
        shortName: "UBC",
        domain: "ubc.ca",
        address: "Vancouver, BC, Canada"
    },
    // India
    {
        name: "Indian Institute of Technology Delhi",
        sheerId: 10007277,
        country: "India",
        shortName: "IIT Delhi",
        domain: "iitd.ac.in",
        address: "New Delhi, India"
    },
    {
        name: "University of Mumbai",
        sheerId: 3819983,
        country: "India",
        shortName: "Mumbai University",
        domain: "mu.ac.in",
        address: "Mumbai, India"
    },
    // Vietnam
    {
        name: "Hanoi University of Science and Technology",
        sheerId: 588731,
        country: "Vietnam",
        shortName: "HUST",
        domain: "hust.edu.vn",
        address: "Hanoi, Vietnam"
    },
    {
        name: "VNU University of Engineering and Technology",
        sheerId: 10066238,
        country: "Vietnam",
        shortName: "VNU-UET",
        domain: "uet.vnu.edu.vn",
        address: "Hanoi, Vietnam"
    },
    {
        name: "VNU University of Information Technology",
        sheerId: 588738,
        country: "Vietnam",
        shortName: "UIT",
        domain: "uit.edu.vn",
        address: "Ho Chi Minh City, Vietnam"
    },
    {
        name: "FPT University",
        sheerId: 588772,
        country: "Vietnam",
        shortName: "FPT",
        domain: "fpt.edu.vn",
        address: "Hanoi, Vietnam"
    },
    {
        name: "Posts and Telecommunications Institute of Technology",
        sheerId: 588608,
        country: "Vietnam",
        shortName: "PTIT",
        domain: "ptit.edu.vn",
        address: "Hanoi, Vietnam"
    },
    {
        name: "VNU University of Science",
        sheerId: 10492794,
        country: "Vietnam",
        shortName: "VNU-HUS",
        domain: "hus.vnu.edu.vn",
        address: "Hanoi, Vietnam"
    },
    // UK
    {
        name: "University of Oxford",
        sheerId: 273409,
        country: "UK",
        shortName: "Oxford",
        domain: "ox.ac.uk",
        address: "Oxford, UK"
    },
    {
        name: "University of Cambridge",
        sheerId: 273378,
        country: "UK",
        shortName: "Cambridge",
        domain: "cam.ac.uk",
        address: "Cambridge, UK"
    },
    {
        name: "Imperial College London",
        sheerId: 273294,
        country: "UK",
        shortName: "Imperial",
        domain: "imperial.ac.uk",
        address: "London, UK"
    },
    // Japan
    {
        name: "The University of Tokyo",
        sheerId: 354085,
        country: "Japan",
        shortName: "UTokyo",
        domain: "u-tokyo.ac.jp",
        address: "Tokyo, Japan"
    },
    {
        name: "Kyoto University",
        sheerId: 353961,
        country: "Japan",
        shortName: "KyotoU",
        domain: "kyoto-u.ac.jp",
        address: "Kyoto, Japan"
    },
    // South Korea
    {
        name: "Seoul National University",
        sheerId: 356569,
        country: "South Korea",
        shortName: "SNU",
        domain: "snu.ac.kr",
        address: "Seoul, South Korea"
    },
    {
        name: "Yonsei University",
        sheerId: 356632,
        country: "South Korea",
        shortName: "Yonsei",
        domain: "yonsei.ac.kr",
        address: "Seoul, South Korea"
    },
    {
        name: "Korea University",
        sheerId: 356431,
        country: "South Korea",
        shortName: "KU",
        domain: "korea.ac.kr",
        address: "Seoul, South Korea"
    },
    // Germany
    {
        name: "Technical University of Munich",
        sheerId: 10011178,
        country: "Germany",
        shortName: "TUM",
        domain: "tum.de",
        address: "Munich, Germany"
    },
    {
        name: "Ludwig Maximilian University of Munich",
        sheerId: 344450,
        country: "Germany",
        shortName: "LMU",
        domain: "lmu.de",
        address: "Munich, Germany"
    },
    // France
    {
        name: "École Polytechnique",
        sheerId: 329766,
        country: "France",
        shortName: "Polytechnique",
        domain: "polytechnique.edu",
        address: "Palaiseau, France"
    },
    {
        name: "PSL Research University",
        sheerId: 10148649,
        country: "France",
        shortName: "PSL",
        domain: "psl.eu",
        address: "Paris, France"
    },
    // Singapore
    {
        name: "National University of Singapore",
        sheerId: 356355,
        country: "Singapore",
        shortName: "NUS",
        domain: "nus.edu.sg",
        address: "Singapore"
    },
    {
        name: "Nanyang Technological University",
        sheerId: 356356,
        country: "Singapore",
        shortName: "NTU",
        domain: "ntu.edu.sg",
        address: "Singapore"
    },
    // China
    {
        name: "Tsinghua University",
        sheerId: 3852634,
        country: "China",
        shortName: "Tsinghua",
        domain: "tsinghua.edu.cn",
        address: "Beijing, China"
    },
    {
        name: "Peking University",
        sheerId: 3852964,
        country: "China",
        shortName: "PKU",
        domain: "pku.edu.cn",
        address: "Beijing, China"
    },
    {
        name: "Fudan University",
        sheerId: 3853298,
        country: "China",
        shortName: "Fudan",
        domain: "fudan.edu.cn",
        address: "Shanghai, China"
    },
    // Brazil
    {
        name: "University of São Paulo",
        sheerId: 10042652,
        country: "Brazil",
        shortName: "USP",
        domain: "usp.br",
        address: "São Paulo, Brazil"
    },
    {
        name: "University of Campinas",
        sheerId: 10059316,
        country: "Brazil",
        shortName: "Unicamp",
        domain: "unicamp.br",
        address: "Campinas, Brazil"
    },
    {
        name: "Federal University of Rio de Janeiro",
        sheerId: 412760,
        country: "Brazil",
        shortName: "UFRJ",
        domain: "ufrj.br",
        address: "Rio de Janeiro, Brazil"
    },
    // Australia
    {
        name: "The University of Melbourne",
        sheerId: 345301,
        country: "Australia",
        shortName: "Melbourne",
        domain: "unimelb.edu.au",
        address: "Melbourne, Australia"
    },
    {
        name: "Australian National University",
        sheerId: 345276,
        country: "Australia",
        shortName: "ANU",
        domain: "anu.edu.au",
        address: "Canberra, Australia"
    },
    {
        name: "The University of Sydney",
        sheerId: 345303,
        country: "Australia",
        shortName: "USyd",
        domain: "sydney.edu.au",
        address: "Sydney, Australia"
    }
];

// K-12 School Districts and Charter Networks (Preferred by OpenAI/ChatGPT)
// NOTE: Individual high schools with type "K12" work better than districts
// These schools were discovered using the K12 Tips methodology from README
// All verified via SheerID API: orgsearch.sheerid.net/rest/organization/v2/search?type=K12
const K12_SCHOOLS = [
    // ============================================
    // NYC SPECIALIZED HIGH SCHOOLS (8 schools)
    // ============================================
    { name: "Stuyvesant High School", sheerId: 155694, type: "K12", city: "New York, NY", staffUrl: "https://stuy.enschool.org/apps/staff/" },
    { name: "Bronx High School Of Science", sheerId: 156251, type: "K12", city: "Bronx, NY", staffUrl: "https://www.bxscience.edu/apps/staff/" },
    { name: "Brooklyn Technical High School", sheerId: 157582, type: "K12", city: "Brooklyn, NY", staffUrl: "https://www.bths.edu/apps/staff/" },
    { name: "Staten Island Technical High School", sheerId: 155770, type: "K12", city: "Staten Island, NY", staffUrl: "https://www.siths.org/staff-directory" },
    { name: "Townsend Harris High School", sheerId: 158162, type: "K12", city: "Flushing, NY", staffUrl: "https://thhs.qc.edu/faculty-and-staff/" },
    { name: "High School for Math, Science and Engineering", sheerId: 155694, type: "K12", city: "New York, NY" },
    { name: "Queens High School for Sciences at York College", sheerId: 158162, type: "K12", city: "Jamaica, NY" },
    { name: "Information Technology High School", sheerId: 3496072, type: "K12", city: "Long Island City, NY" },

    // ============================================
    // CHICAGO SELECTIVE ENROLLMENT (5 schools)
    // ============================================
    { name: "Walter Payton College Preparatory High School", sheerId: 3521141, type: "K12", city: "Chicago, IL", staffUrl: "https://www.wpcp.org/apps/staff/" },
    { name: "Whitney M Young Magnet High School", sheerId: 3521074, type: "K12", city: "Chicago, IL", staffUrl: "https://www.wyoung.org/staff" },
    { name: "Northside College Preparatory High School", sheerId: 219471, type: "K12", city: "Chicago, IL" },
    { name: "Lane Technical High School", sheerId: 219254, type: "K12", city: "Chicago, IL" },
    { name: "STEM Magnet Academy Elementary School", sheerId: 3521073, type: "K12", city: "Chicago, IL" },

    // ============================================
    // VIRGINIA / DC AREA STEM (3 schools)
    // ============================================
    { name: "Thomas Jefferson High School For Science And Technology", sheerId: 3704245, type: "K12", city: "Alexandria, VA", note: "#1 STEM school in USA", staffUrl: "https://tjhsst.fcps.edu/faculty" },
    { name: "BASIS Independent McLean", sheerId: 4815368, type: "K12", city: "McLean, VA" },
    { name: "McKinley Technology High School", sheerId: 167407, type: "K12", city: "Washington, DC" },

    // ============================================
    // CALIFORNIA ELITE HIGH SCHOOLS (10 schools)
    // ============================================
    { name: "Gretchen Whitney High School", sheerId: 3539252, type: "K12", city: "Cerritos, CA", note: "#1 Public HS in CA", staffUrl: "https://www.whitneyhs.us/staff" },
    { name: "Lowell High School (San Francisco)", sheerId: 262338, type: "K12", city: "San Francisco, CA", staffUrl: "https://www.sfusd.edu/school/lowell-high-school" },
    { name: "Palo Alto High School", sheerId: 262370, type: "K12", city: "Palo Alto, CA", staffUrl: "https://www.paly.net/about/staff-directory" },
    { name: "Gunn (Henry M.) High School", sheerId: 262410, type: "K12", city: "Palo Alto, CA" },
    { name: "Palos Verdes Peninsula High School", sheerId: 254044, type: "K12", city: "Palos Verdes, CA" },
    { name: "Palos Verdes High School", sheerId: 254042, type: "K12", city: "Palos Verdes, CA" },
    { name: "Foothill Technology High School", sheerId: 259802, type: "K12", city: "Ventura, CA" },
    { name: "BASIS Independent Silicon Valley", sheerId: 3554672, type: "K12", city: "San Jose, CA" },
    { name: "Technology High School (Rohnert Park)", sheerId: 263711, type: "K12", city: "Rohnert Park, CA" },
    { name: "KIPP Esperanza High School", sheerId: 10010525, type: "K12", city: "East Palo Alto, CA" },

    // ============================================
    // NEW JERSEY / NORTHEAST (5 schools)
    // ============================================
    { name: "High Technology High School", sheerId: 10286510, type: "K12", city: "Lincroft, NJ", note: "#1 Public HS in NJ" },
    { name: "Technology High School (Newark)", sheerId: 151793, type: "K12", city: "Newark, NJ" },
    { name: "Lowell High School (Massachusetts)", sheerId: 145511, type: "K12", city: "Lowell, MA" },
    { name: "Phillips Academy Andover", sheerId: 145364, type: "K12", city: "Andover, MA", note: "Elite prep school" },
    { name: "Phillips Exeter Academy", sheerId: 148201, type: "K12", city: "Exeter, NH", note: "Elite prep school" },

    // ============================================
    // BASIS CHARTER NETWORK (6 schools)
    // ============================================
    { name: "BASIS Scottsdale", sheerId: 3536914, type: "K12", city: "Scottsdale, AZ" },
    { name: "BASIS Tucson North", sheerId: 250527, type: "K12", city: "Tucson, AZ" },
    { name: "BASIS Mesa", sheerId: 3536799, type: "K12", city: "Mesa, AZ" },
    { name: "BASIS Chandler", sheerId: 3707277, type: "K12", city: "Chandler, AZ" },
    { name: "BASIS Peoria", sheerId: 3537336, type: "K12", city: "Peoria, AZ" },
    { name: "BASIS Flagstaff", sheerId: 3537729, type: "K12", city: "Flagstaff, AZ" },

    // ============================================
    // KIPP CHARTER NETWORK (8 schools)
    // ============================================
    { name: "KIPP Academy Charter School (Bronx)", sheerId: 155846, type: "K12", city: "Bronx, NY" },
    { name: "KIPP DC Public Charter Schools", sheerId: 3501341, type: "K12", city: "Washington, DC" },
    { name: "KIPP SoCal Public Schools", sheerId: 10488713, type: "K12", city: "Los Angeles, CA" },
    { name: "KIPP New Jersey Schools", sheerId: 3493517, type: "K12", city: "Newark, NJ" },
    { name: "KIPP Philadelphia Public Schools", sheerId: 3500589, type: "K12", city: "Philadelphia, PA" },
    { name: "KIPP Columbus", sheerId: 3508555, type: "K12", city: "Columbus, OH" },
    { name: "KIPP Sunnyside High School", sheerId: 238013, type: "K12", city: "Houston, TX" },
    { name: "KIPP Academy Lynn Charter School", sheerId: 145625, type: "K12", city: "Lynn, MA" },

    // ============================================
    // SUCCESS ACADEMY NETWORK (5 schools)
    // ============================================
    { name: "Success Academy (NY Central)", sheerId: 10236792, type: "K12", city: "New York, NY" },
    { name: "Success Academy Charter School - Harlem", sheerId: 4581454, type: "K12", city: "New York, NY" },
    { name: "Success Academy Charter School - Union Square", sheerId: 3495255, type: "K12", city: "New York, NY" },
    { name: "Success Academy Charter School - Hudson Yards", sheerId: 3495291, type: "K12", city: "New York, NY" },
    { name: "Success Academy Charter School - Hell's Kitchen", sheerId: 3495299, type: "K12", city: "New York, NY" },

    // ============================================
    // LINCOLN HIGH SCHOOLS (Multiple locations)
    // ============================================
    { name: "Lincoln High School (Tacoma, WA)", sheerId: 270998, type: "K12", city: "Tacoma, WA", staffUrl: "https://lincoln.tacomaschools.org/contact" },
    { name: "Lincoln High School (Portland, OR)", sheerId: 268293, type: "K12", city: "Portland, OR", staffUrl: "https://www.lincolnhs.org/apps/staff/" },
    { name: "Lincoln High School (San Diego, CA)", sheerId: 257321, type: "K12", city: "San Diego, CA" },

    // ============================================
    // OTHER NOTABLE MAGNET SCHOOLS (10 schools)
    // ============================================
    { name: "Central Magnet School", sheerId: 189685, type: "K12", city: "Murfreesboro, TN" },
    { name: "Tucson Magnet High School", sheerId: 250255, type: "K12", city: "Tucson, AZ" },
    { name: "Classical Magnet School", sheerId: 3703766, type: "K12", city: "Hartford, CT" },
    { name: "Garner Magnet High School", sheerId: 174308, type: "K12", city: "Garner, NC" },
    { name: "Manor New Technology High School", sheerId: 242065, type: "K12", city: "Manor, TX" },
    { name: "Academic Magnet High School", sheerId: 177339, type: "K12", city: "North Charleston, SC", note: "#1 Public HS in SC" },
    { name: "Broughton Magnet High School", sheerId: 3503466, type: "K12", city: "Raleigh, NC" },
    { name: "King-Drew Magnet High School", sheerId: 3539022, type: "K12", city: "Los Angeles, CA" },
    { name: "Benson Magnet High School", sheerId: 3527182, type: "K12", city: "Omaha, NE" },
    { name: "Galileo Magnet High School", sheerId: 3502961, type: "K12", city: "Danville, VA" },

    // ============================================
    // SCIENCE ACADEMIES (10 schools)
    // ============================================
    { name: "Fulton Science Academy", sheerId: 10148026, type: "K12", city: "Alpharetta, GA" },
    { name: "Bio-Med Science Academy STEM School", sheerId: 3704829, type: "K12", city: "Rootstown, OH" },
    { name: "Envision Science Academy", sheerId: 3503442, type: "K12", city: "Wake Forest, NC" },
    { name: "Harmony Science Academy Dallas", sheerId: 3706876, type: "K12", city: "Dallas, TX" },
    { name: "Horizon Science Academy Columbus HS", sheerId: 3508525, type: "K12", city: "Columbus, OH" },
    { name: "Magnolia Science Academy 1", sheerId: 3539426, type: "K12", city: "Reseda, CA" },
    { name: "Magnolia Science Academy 3", sheerId: 254735, type: "K12", city: "Carson, CA" },
    { name: "Dove Science Academy High School OKC", sheerId: 3529406, type: "K12", city: "Oklahoma City, OK" },
    { name: "Science Academy of Chicago", sheerId: 216860, type: "K12", city: "Mount Prospect, IL" },
    { name: "Travis Science Academy", sheerId: 237052, type: "K12", city: "Temple, TX" },

    // ============================================
    // ELITE PREP SCHOOLS (10 schools)
    // ============================================
    { name: "Berkeley Preparatory School", sheerId: 185742, type: "K12", city: "Tampa, FL" },
    { name: "Georgetown Preparatory School", sheerId: 168570, type: "K12", city: "Rockville, MD" },
    { name: "Shorecrest Preparatory School", sheerId: 185870, type: "K12", city: "Saint Petersburg, FL" },
    { name: "Trinity Preparatory School", sheerId: 183106, type: "K12", city: "Winter Park, FL" },
    { name: "Seattle Preparatory School", sheerId: 269977, type: "K12", city: "Seattle, WA" },
    { name: "Fordham Preparatory School", sheerId: 156050, type: "K12", city: "Bronx, NY" },
    { name: "Rutgers Preparatory School", sheerId: 154979, type: "K12", city: "Somerset, NJ" },
    { name: "Scranton Preparatory School", sheerId: 165101, type: "K12", city: "Scranton, PA" },
    { name: "Flintridge Preparatory School", sheerId: 254919, type: "K12", city: "La Canada Flintridge, CA" },
    { name: "Eastside Preparatory School", sheerId: 3554995, type: "K12", city: "Kirkland, WA" },

    // ============================================
    // EARLY COLLEGE HIGH SCHOOLS (8 schools)
    // ============================================
    { name: "Early College High School Dallas", sheerId: 235022, type: "K12", city: "Dallas, TX" },
    { name: "Early College High School at Carver", sheerId: 179760, type: "K12", city: "Atlanta, GA" },
    { name: "Early College at Guilford", sheerId: 174145, type: "K12", city: "Greensboro, NC" },
    { name: "Early College Academy Columbus", sheerId: 3508435, type: "K12", city: "Columbus, OH" },
    { name: "Early College High School Costa Mesa", sheerId: 258878, type: "K12", city: "Costa Mesa, CA" },
    { name: "Early College High School at Delaware State", sheerId: 3501075, type: "K12", city: "Dover, DE" },
    { name: "Early College Alliance", sheerId: 203333, type: "K12", city: "Ypsilanti, MI" },
    { name: "Early College High School Round Rock", sheerId: 3533810, type: "K12", city: "Round Rock, TX" },

    // ============================================
    // IDEA PUBLIC SCHOOLS (5 schools)
    // ============================================
    { name: "IDEA Public Schools", sheerId: 3533677, type: "K12", city: "Weslaco, TX" },
    { name: "IDEA Public Charter School DC", sheerId: 10521304, type: "K12", city: "Washington, DC" },
    { name: "IDEA Health Professions", sheerId: 10057129, type: "K12", city: "Austin, TX" },
    { name: "SEED Public Charter School", sheerId: 3501292, type: "K12", city: "Washington, DC" },
    { name: "IDEA Price Hill", sheerId: 10000736, type: "K12", city: "Cincinnati, OH" },

    // ============================================
    // HUMANITIES & IB SCHOOLS (8 schools)
    // ============================================
    { name: "Humanities Preparatory School", sheerId: 155269, type: "K12", city: "New York, NY" },
    { name: "Governor's School For Arts And Humanities", sheerId: 3504562, type: "K12", city: "Greenville, SC" },
    { name: "Indiana Academy For Sci Math And Humanities", sheerId: 3705062, type: "K12", city: "Muncie, IN" },
    { name: "Connecticut International Baccalaureate Academy", sheerId: 149911, type: "K12", city: "East Hartford, CT" },
    { name: "Heights HS International Baccalaureate School", sheerId: 3532141, type: "K12", city: "Houston, TX" },
    { name: "Jefferson County IB High School", sheerId: 3506566, type: "K12", city: "Birmingham, AL" },
    { name: "Texas Academy Leadership Humanities", sheerId: 3532903, type: "K12", city: "Beaumont, TX" },
    { name: "Hall International Academy Arts Humanities", sheerId: 4584414, type: "K12", city: "Boise, ID" },

    // ============================================
    // WESTLAKE & BELLEVUE SCHOOLS (8 schools)
    // ============================================
    { name: "Westlake High School Austin", sheerId: 242400, type: "K12", city: "Austin, TX" },
    { name: "Westlake High School CA", sheerId: 255557, type: "K12", city: "Westlake Village, CA" },
    { name: "Westlake High School Saratoga Springs", sheerId: 10010881, type: "K12", city: "Saratoga Springs, UT" },
    { name: "Bellevue High School WA", sheerId: 269511, type: "K12", city: "Bellevue, WA" },
    { name: "Interlake Senior High School", sheerId: 269566, type: "K12", city: "Bellevue, WA" },
    { name: "Newport Senior High School", sheerId: 269544, type: "K12", city: "Bellevue, WA" },
    { name: "Sammamish Senior High School", sheerId: 269532, type: "K12", city: "Bellevue, WA" },
    { name: "Bellevue Christian School", sheerId: 269510, type: "K12", city: "Bellevue, WA" }
];

module.exports = { UNIVERSITIES, K12_SCHOOLS };


