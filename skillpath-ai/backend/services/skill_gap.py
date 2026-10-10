import re

def _clean_token(value: str) -> str:
    # Strip leading/trailing punctuation marks (.,;:!?"'[]{}) while preserving + and # (e.g. C++, C#)
    val = re.sub(r"^[^\w+#]+|[^\w+#]+$", "", str(value or "").lower().strip())
    return " ".join(val.replace("-", " ").split())

def _extract_variants(value: str) -> set[str]:
    raw = str(value or "").strip()
    if not raw:
        return set()
    cleaned = _clean_token(raw)
    variants = {cleaned} if cleaned else set()
    
    # Strip parentheses and add variants (e.g. "SQL (PostgreSQL)" -> "sql", "postgresql")
    no_paren = _clean_token(re.sub(r"\(.*?\)", "", raw))
    if no_paren:
        variants.add(no_paren)
    for inner in re.findall(r"\((.*?)\)", raw):
        ci = _clean_token(inner)
        if ci:
            variants.add(ci)
            
    # Handle compound connectors like &, /, and (e.g. "Git & GitHub" -> "git", "github")
    for part in re.split(r"[/&]|\band\b", raw, flags=re.I):
        cp = _clean_token(part)
        if cp:
            variants.add(cp)
            
    return {v for v in variants if v}

def _norm(value: str) -> str:
    return _clean_token(value)

def analyze_skill_gap(student_skills: list[str], required_skills: list[str],
                      related_skills: dict[str, list[str]] | None = None,
                      proficiency: dict[str, int] | None = None) -> dict:
    related_skills = related_skills or {}
    proficiency = proficiency or {}
    
    # Map student variants back to the original skill entry
    student_variants: dict[str, str] = {}
    for s in student_skills:
        if str(s).strip():
            for v in _extract_variants(s):
                student_variants[v] = s

    # Related skills are normalized so a known related skill can mark a requirement as developing.
    related_norm = {}
    for required, related in related_skills.items():
        req_key = _clean_token(required)
        related_norm[req_key] = {_clean_token(x) for x in related}

    strong, developing, missing = [], [], []
    for skill in required_skills:
        key = _clean_token(skill)
        req_variants = _extract_variants(skill)
        
        # Check if any variant of the required skill exists in student variants
        matched_student_skill = None
        for v in req_variants:
            if v in student_variants:
                matched_student_skill = student_variants[v]
                break
                
        exact = matched_student_skill is not None
        prof = proficiency.get(skill, proficiency.get(matched_student_skill or "", 0))
        
        # Check related skills
        has_related = any(
            any(v in student_variants for v in _extract_variants(rel))
            for rel in related_skills.get(skill, [])
        ) or any(
            v in related_norm.get(key, set())
            for s in student_skills
            for v in _extract_variants(s)
        )
        
        if exact and (not prof or prof >= 4):
            strong.append(skill)
        elif exact or has_related:
            developing.append(skill)
        else:
            missing.append(skill)
            
    total = len(required_skills)
    return {
        "strong": strong, "developing": developing, "missing": missing,
        "required_count": total,
        "coverage_score": round((len(strong) + 0.5 * len(developing)) / total * 100) if total else 0
    }

