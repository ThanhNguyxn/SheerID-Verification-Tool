// K-12 Schools and Teacher Organizations Data

const K12_SCHOOLS = [
    // US High Schools
    { id: 10070538, name: "Lincoln High School", state: "CA", type: "K12", weight: 85 },
    { id: 10070540, name: "Washington High School", state: "CA", type: "K12", weight: 84 },
    { id: 10070542, name: "Roosevelt High School", state: "NY", type: "K12", weight: 83 },
    { id: 10070544, name: "Jefferson High School", state: "TX", type: "K12", weight: 82 },
    { id: 10070546, name: "Madison High School", state: "FL", type: "K12", weight: 81 },
    { id: 10070548, name: "Kennedy High School", state: "IL", type: "K12", weight: 80 },
    { id: 10070550, name: "Adams High School", state: "PA", type: "K12", weight: 79 },
    { id: 10070552, name: "Jackson High School", state: "OH", type: "K12", weight: 78 },
    { id: 10070554, name: "Wilson High School", state: "WA", type: "K12", weight: 77 },
    { id: 10070556, name: "Franklin High School", state: "MA", type: "K12", weight: 76 }
];

const UK_SCHOOLS = [
    { id: 273500, name: "St. Mary's Catholic School", region: "London", type: "K12", weight: 85 },
    { id: 273502, name: "Greenfield Academy", region: "Manchester", type: "K12", weight: 84 },
    { id: 273504, name: "Oakwood Secondary School", region: "Birmingham", type: "K12", weight: 83 },
    { id: 273506, name: "Riverside High School", region: "Leeds", type: "K12", weight: 82 },
    { id: 273508, name: "Hillside Academy", region: "Liverpool", type: "K12", weight: 81 },
    { id: 273510, name: "Carlton School", region: "Bristol", type: "K12", weight: 80 }
];

// Military branches for veterans
const MILITARY_BRANCHES = [
    "Army",
    "Navy",
    "Air Force",
    "Marine Corps",
    "Coast Guard",
    "Space Force"
];

// Military status options
const MILITARY_STATUS = [
    { value: "VETERAN", label: "Veteran" },
    { value: "ACTIVE_DUTY", label: "Active Duty" },
    { value: "RESERVE", label: "Reserve" },
    { value: "NATIONAL_GUARD", label: "National Guard" }
];

// Export data
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { K12_SCHOOLS, UK_SCHOOLS, MILITARY_BRANCHES, MILITARY_STATUS };
}
