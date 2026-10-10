# Adapted weighted readiness assessment after removing Experience
# Rebalanced weights: Technical Skills (30%), Project Portfolio (25%), Industry Alignment (20%), Internship Readiness (15%), Portfolio Strength (10%)
WEIGHTS = {
    "technical_skills": 0.30,
    "project_experience": 0.25,
    "industry_alignment": 0.20,
    "internship_readiness": 0.15,
    "portfolio_strength": 0.10,
}

def calculate_readiness(profile: dict, skill_gap: dict) -> dict:
    required_count = skill_gap.get("required_count", 0)
    strong = len(skill_gap.get("strong", []))
    developing = len(skill_gap.get("developing", []))
    technical = round((strong + 0.5 * developing) / required_count * 100) if required_count else 0
    
    projects = profile.get("projects") or []
    certifications = profile.get("certifications") or []

    # If candidate has provided virtually no profile data, report insufficient info rather than an arbitrary baseline
    if not projects and not certifications and strong == 0 and developing == 0:
        return {
            "overall_score": 0,
            "technical_skills": 0,
            "project_experience": 0,
            "industry_alignment": 0,
            "internship_readiness": 0,
            "portfolio_strength": 0,
            "classification": "Not Ready",
            "weights": {k: int(v * 100) for k, v in WEIGHTS.items()},
            "note": "Insufficient profile data. Add your technical skills and documented projects to calculate a readiness assessment.",
            "is_insufficient": True
        }

    # Project experience score evaluates quality & quantity of documented portfolio work
    project_score = min(100, 30 + 25 * len(projects)) if projects else 10
    
    # Portfolio strength evaluates combined project evidence and external credential verifications
    portfolio_score = min(100, 15 + 25 * len(projects) + 15 * len(certifications)) if (projects or certifications) else 10
    
    # Internship readiness evaluates synthesized capability from technical grasp and project delivery
    internship_score = min(100, round(technical * 0.45 + min(55, 30 * len(projects) + 15 * len(certifications)))) if (projects or certifications or strong > 0) else 10
    
    # Industry alignment assesses overlap with target job expectations
    industry_score = min(100, round(technical * 0.65 + min(35, len(projects) * 12))) if (projects or strong > 0) else 10

    scores = {
        "technical_skills": technical,
        "project_experience": project_score,
        "industry_alignment": industry_score,
        "internship_readiness": internship_score,
        "portfolio_strength": portfolio_score,
    }
    
    overall = round(sum(scores[k] * WEIGHTS[k] for k in WEIGHTS))
    label = "Not Ready" if overall < 40 else "Needs Development" if overall < 60 else "Nearly Ready" if overall < 80 else "Ready"
    
    return {
        "overall_score": overall,
        **scores,
        "classification": label,
        "weights": {k: int(v * 100) for k, v in WEIGHTS.items()},
        "note": "Project-level estimate based on profile evidence and verified coursework; not an industry-certified assessment.",
        "is_insufficient": False
    }
