"""
SheerID Verification Tool - Universities Data
With weighted selection based on success rates
"""

import random
from typing import Dict, Optional

# ============ UNIVERSITIES (for Student/Teacher) ============
UNIVERSITIES = {
    # USA - Pennsylvania State University (high success rate)
    "2565": {
        "id": 2565,
        "idExtended": "2565",
        "name": "Pennsylvania State University-Main Campus",
        "country": "US",
        "domain": "psu.edu",
        "weight": 100  # Higher = preferred
    },
    "651379": {
        "id": 651379,
        "idExtended": "651379",
        "name": "Pennsylvania State University-World Campus",
        "country": "US",
        "domain": "psu.edu",
        "weight": 95
    },
    "8387": {
        "id": 8387,
        "idExtended": "8387",
        "name": "Pennsylvania State University-Penn State Harrisburg",
        "country": "US",
        "domain": "psu.edu",
        "weight": 90
    },
    # USA - Other universities
    "1495": {
        "id": 1495,
        "idExtended": "1495",
        "name": "University of California-Los Angeles",
        "country": "US",
        "domain": "ucla.edu",
        "weight": 80
    },
    "1139": {
        "id": 1139,
        "idExtended": "1139",
        "name": "University of Texas at Austin",
        "country": "US",
        "domain": "utexas.edu",
        "weight": 80
    },
    # International
    "416515": {
        "id": 416515,
        "idExtended": "416515",
        "name": "University of Toronto",
        "country": "CA",
        "domain": "utoronto.ca",
        "weight": 70
    },
    "416614": {
        "id": 416614,
        "idExtended": "416614",
        "name": "University of British Columbia",
        "country": "CA",
        "domain": "ubc.ca",
        "weight": 70
    }
}

# ============ K12 SCHOOLS (High Schools) ============
K12_SCHOOLS = {
    "3995910": {
        "id": 3995910,
        "idExtended": "3995910",
        "name": "Springfield High School (Springfield, OR)",
        "country": "US",
        "type": "HIGH_SCHOOL",
        "weight": 100
    },
    "3995271": {
        "id": 3995271,
        "idExtended": "3995271",
        "name": "Springfield High School (Springfield, OH)",
        "country": "US",
        "type": "HIGH_SCHOOL",
        "weight": 90
    },
    "3992142": {
        "id": 3992142,
        "idExtended": "3992142",
        "name": "Springfield High School (Springfield, IL)",
        "country": "US",
        "type": "HIGH_SCHOOL",
        "weight": 85
    },
    "3996208": {
        "id": 3996208,
        "idExtended": "3996208",
        "name": "Springfield High School (Springfield, PA)",
        "country": "US",
        "type": "HIGH_SCHOOL",
        "weight": 80
    }
}


def select_university(prefer_usa: bool = True, stats=None) -> Dict:
    """
    Select university based on weights and success rates
    
    Args:
        prefer_usa: Prefer US universities
        stats: VerificationStats instance for dynamic weighting
    """
    candidates = list(UNIVERSITIES.values())
    
    if prefer_usa:
        usa_unis = [u for u in candidates if u.get("country") == "US"]
        if usa_unis:
            candidates = usa_unis
    
    # Calculate weights
    weights = []
    for uni in candidates:
        weight = uni.get("weight", 50)
        
        # Adjust weight based on stats if available
        if stats:
            success_rate = stats.get_org_success_rate(uni["name"])
            weight = weight * (success_rate / 50)  # Normalize around 50%
        
        weights.append(max(1, weight))  # Minimum weight of 1
    
    # Weighted random selection
    total = sum(weights)
    r = random.uniform(0, total)
    
    cumulative = 0
    for uni, weight in zip(candidates, weights):
        cumulative += weight
        if r <= cumulative:
            return uni
    
    return candidates[-1]


def select_k12_school(stats=None) -> Dict:
    """Select K12 school based on weights"""
    candidates = list(K12_SCHOOLS.values())
    
    weights = []
    for school in candidates:
        weight = school.get("weight", 50)
        if stats:
            success_rate = stats.get_org_success_rate(school["name"])
            weight = weight * (success_rate / 50)
        weights.append(max(1, weight))
    
    total = sum(weights)
    r = random.uniform(0, total)
    
    cumulative = 0
    for school, weight in zip(candidates, weights):
        cumulative += weight
        if r <= cumulative:
            return school
    
    return candidates[-1]


def get_university_by_id(uni_id: str) -> Optional[Dict]:
    """Get university by ID"""
    return UNIVERSITIES.get(str(uni_id))


def get_school_by_id(school_id: str) -> Optional[Dict]:
    """Get K12 school by ID"""
    return K12_SCHOOLS.get(str(school_id))
