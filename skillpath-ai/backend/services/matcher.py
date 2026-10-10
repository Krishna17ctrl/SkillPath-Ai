import re
from .data_loader import opportunities

def _clean_token(value: str) -> str:
    val = re.sub(r"^[^\w+#]+|[^\w+#]+$", "", str(value or "").lower().strip())
    return " ".join(val.replace("-", " ").split())

def _extract_variants(value: str) -> set[str]:
    raw = str(value or "").strip()
    if not raw:
        return set()
    cleaned = _clean_token(raw)
    variants = {cleaned} if cleaned else set()
    no_paren = _clean_token(re.sub(r"\(.*?\)", "", raw))
    if no_paren:
        variants.add(no_paren)
    for inner in re.findall(r"\((.*?)\)", raw):
        ci = _clean_token(inner)
        if ci:
            variants.add(ci)
    for part in re.split(r"[/&]|\band\b", raw, flags=re.I):
        cp = _clean_token(part)
        if cp:
            variants.add(cp)
    return {v for v in variants if v}

def _norm(x):
    return _clean_token(x)

def match_opportunities(profile: dict, target_career: str | None = None) -> list[dict]:
    student_skills = profile.get("skills", [])
    student_variants = set()
    for s in student_skills:
        student_variants.update(_extract_variants(s))

    projects = profile.get("projects") or []
    education = _norm(profile.get("education", ""))
    results = []
    
    for opp in opportunities():
        required = opp.get("required_skills", [])
        preferred = opp.get("preferred_skills", [])
        
        # Skill is matched if any variant matches student skills
        matched = [
            s for s in required 
            if any(v in student_variants for v in _extract_variants(s))
        ]
        
        developing = [
            s for s in required 
            if s not in matched and any(
                any(v in student_variants for v in _extract_variants(alias))
                for alias in _related_aliases(s)
            )
        ]
        
        missing = [s for s in required if s not in matched and s not in developing]
        skill_score = (len(matched) + 0.5 * len(developing)) / len(required) * 70 if required else 0
        preferred_score = (sum(1 for s in preferred if any(v in student_variants for v in _extract_variants(s))) / len(preferred) * 10) if preferred else 5
        project_score = 10 if projects else (3 if not opp.get("projects_required") else 0)
        edu_score = 10 if not education or any(_norm(x) in education or education in _norm(x) for x in opp.get("education", [])) else 4
        score = round(min(100, skill_score + preferred_score + project_score + edu_score))
        
        critical_missing = [
            s for s in opp.get("critical_skills", [])
            if not any(v in student_variants for v in _extract_variants(s))
        ]
        
        classification = "APPLY NOW" if score >= 80 and not critical_missing else "PREPARE & APPLY" if score >= 60 else "NOT YET"
        reasons = []
        if matched:
            reasons.append(f"Your profile demonstrates verified strength in {', '.join(matched[:3])}.")
        if missing:
            reasons.append(f"Build concrete project evidence in {', '.join(missing[:3])}.")
        if projects:
            reasons.append("Your documented project portfolio significantly bolsters this application match.")
        if not reasons:
            reasons.append("Add relevant core skills and documented projects to advance your match score.")
            
        results.append({
            **opp, "match_score": score, "matched_skills": matched,
            "developing_skills": developing, "missing_skills": missing,
            "critical_missing_skills": critical_missing,
            "classification": classification, "explanation": " ".join(reasons)
        })
        
    # Keep matches relevant to target career first, then score.
    target = _norm(target_career or profile.get("target_career", ""))
    results.sort(key=lambda x: (0 if target and _norm(x["role"]) == target else 1, -x["match_score"]))
    return results

def _related_aliases(skill):
    aliases = {
        "scikit-learn": ["machine learning", "scikit learn", "sklearn"],
        "machine learning": ["scikit-learn", "numpy", "pandas"],
        "sql": ["postgresql", "mysql", "sqlite"],
        "javascript": ["react", "typescript"],
        "rest apis": ["fastapi", "rest api"],
        "fastapi": ["rest apis", "python"],
        "data visualization": ["power bi", "matplotlib", "seaborn"]
    }
    return aliases.get(_norm(skill), [])

