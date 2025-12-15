
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
const K12_SCHOOLS = [
    {
        name: "Dallas Independent School District",
        sheerId: 3995910,
        idExtended: "3995910",
        country: "USA",
        domain: "dallasisd.org",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/dallasisd.png",
        address: "Dallas, TX, USA"
    },
    {
        name: "Challenger School",
        sheerId: 3995910,
        idExtended: "3995910",
        country: "USA",
        domain: "challengerschool.com",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/challenger.png",
        address: "Sandy, UT, USA"
    },
    {
        name: "Los Angeles Unified School District",
        sheerId: 3995910,
        idExtended: "3995910",
        country: "USA",
        domain: "lausd.net",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/lausd.png",
        address: "Los Angeles, CA, USA"
    },
    {
        name: "New York City Department of Education",
        sheerId: 3995910,
        idExtended: "3995910",
        country: "USA",
        domain: "schools.nyc.gov",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/nycdoe.png",
        address: "New York, NY, USA"
    },
    {
        name: "Chicago Public Schools",
        sheerId: 3995910,
        idExtended: "3995910",
        country: "USA",
        domain: "cps.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/cps.png",
        address: "Chicago, IL, USA"
    },
    {
        name: "Clark County School District",
        sheerId: 3995910,
        idExtended: "3995910",
        country: "USA",
        domain: "ccsd.net",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/ccsd.png",
        address: "Las Vegas, NV, USA"
    },
    {
        name: "Fairfax County Public Schools",
        sheerId: 3995910,
        idExtended: "3995910",
        country: "USA",
        domain: "fcps.edu",
        logo: "https://thanhnguyxn.github.io/student-card-generator/img/logos/fcps.png",
        address: "Falls Church, VA, USA"
    }
];

module.exports = { UNIVERSITIES, K12_SCHOOLS };
