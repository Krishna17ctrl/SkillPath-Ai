import re
from .data_loader import skills_catalog

def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\u00a0", " ")).strip()

def extract_skills(text: str) -> dict:
    cleaned = normalize_text(text)
    lower = cleaned.lower()
    found = []
    catalog = skills_catalog()
    for item in catalog:
        name = item["name"]
        aliases = item.get("aliases", []) + [name]
        matched = False
        for alias in aliases:
            alias = alias.strip().lower()
            if not alias:
                continue
            # Boundaries prevent matching "java" inside "javascript".
            pattern = r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])"
            if re.search(pattern, lower):
                matched = True
                break
        if matched:
            found.append(name)
    # Conservative, explainable section extraction preserving full sentences with punctuation.
    def section_items(labels):
        for label in labels:
            m = re.search(rf"{label}\s*[:\-]\s*(.+?)(?=\n\s*[A-Z][A-Za-z /&-]{{2,30}}\s*[:\-]|\Z)", cleaned, re.I | re.S)
            if m:
                raw_items = [
                    re.sub(r"^[•\-\*\t\s]+", "", x).strip() 
                    for x in re.split(r"\n+|•|(?<=\n)\s*[\-\*]\s+", m.group(1))
                ]
                return [x for x in raw_items if len(x) > 3][:8]
        return []
    education = ""
    for candidate in ["BCA", "B.Sc", "BSc", "B.Tech", "BTech", "MCA", "M.Tech", "MBA"]:
        if re.search(rf"\b{re.escape(candidate)}\b", cleaned, re.I):
            education = candidate
            break
    projects = section_items(["projects", "academic projects", "project portfolio"])
    certifications = section_items(["certifications", "certificates", "courses"])
    return {
        "skills": found,
        "education": {"qualification": education} if education else {},
        "projects": projects,
        "certifications": certifications,
        "confidence": round(min(0.98, 0.45 + 0.08 * len(found)), 2),
        "method": "Dictionary matching with alias normalization (lightweight fallback)"
    }
