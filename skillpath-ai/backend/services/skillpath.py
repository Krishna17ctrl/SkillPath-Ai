from .data_loader import projects_catalog

LEARNING = {
    "SQL": ("Learn SELECT, filtering, joins, grouping, and basic database design.", "SQL appears in many data and backend roles."),
    "Git": ("Practice commits, branches, pull requests, and resolving simple conflicts.", "Version control is expected in collaborative software work."),
    "Scikit-learn": ("Train and evaluate a baseline classifier or regressor with a clean train/test split.", "It turns ML concepts into a reproducible implementation."),
    "Machine Learning": ("Study train/test splits, baseline models, overfitting, and evaluation metrics.", "It is a core requirement for ML and data-science roles."),
    "Pandas": ("Practice cleaning, joining, grouping, and handling missing values in a real dataset.", "Data preparation is central to analytics and ML."),
    "NumPy": ("Practice arrays, vectorized operations, and numerical transformations.", "It supports efficient scientific Python workflows."),
    "Statistics": ("Review distributions, sampling, correlation, and hypothesis-testing basics.", "Statistics supports sound interpretation of data."),
    "Data Visualization": ("Create a small dashboard with labeled charts and a short written insight.", "Clear communication makes analysis usable."),
    "FastAPI": ("Build a small typed API with validation and error handling.", "It demonstrates how to expose Python logic to applications."),
    "REST APIs": ("Practice HTTP methods, JSON payloads, status codes, and API testing.", "Most applications need reliable service integration."),
    "React": ("Build a responsive form and result view using reusable components.", "It provides visible proof of frontend implementation."),
    "JavaScript": ("Practice arrays, objects, async/await, and fetch.", "These concepts support interactive web applications."),
    "Data Structures": ("Solve basic array, string, stack, queue, and hash-map problems.", "They improve implementation fluency for software roles."),
    "Algorithms": ("Practice searching, sorting, complexity, and problem decomposition.", "They are common foundations for software interviews."),
}
def generate_skillpath(skill_gap: dict, matched_opportunities: list[dict] | None = None) -> dict:
    missing = skill_gap.get("missing", [])
    developing = skill_gap.get("developing", [])
    shared = {}
    for opp in (matched_opportunities or []):
        for s in opp.get("missing_skills", []):
            shared[s] = shared.get(s, 0) + 1
    ordered = sorted(missing, key=lambda s: (-shared.get(s, 0), s)) + sorted(developing, key=lambda s: (-shared.get(s, 0), s))
    actions = []
    seen = set()
    for skill in ordered:
        if skill in seen: continue
        seen.add(skill)
        learn, why = LEARNING.get(skill, (f"Complete a small hands-on exercise in {skill}.", f"{skill} is listed in your target career requirements."))
        actions.append({"title": f"Build {skill} skills", "skill": skill, "action": learn, "why": why, "priority": "High" if skill in missing else "Medium"})
        if len(actions) >= 5: break
    if skill_gap.get("missing") or skill_gap.get("developing"):
        catalog = projects_catalog()
        gaps = {_norm(s) for s in missing + developing}
        ranked = sorted(catalog, key=lambda p: sum(_norm(s) in gaps for s in p["skills"]), reverse=True)
        if ranked and sum(_norm(s) in gaps for s in ranked[0]["skills"]):
            actions.append({"title": ranked[0]["title"], "skill": "Portfolio project", "action": "Build a small, documented project and publish the code with a README.", "why": ranked[0]["reason"], "priority": "High"})
    if not actions:
        actions.append({"title":"Strengthen your portfolio","skill":"Portfolio","action":"Document one project with problem statement, approach, results, and setup instructions.","why":"Evidence of applied skills helps reviewers assess your work.","priority":"Medium"})
    return {"actions": actions, "next_best_action": actions[0]["title"], "method":"Rule-based prioritization from skill gaps and opportunity overlap."}

def _norm(x):
    return " ".join(str(x).lower().replace("-", " ").split())
