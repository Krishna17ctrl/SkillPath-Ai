# Antigravity implementation prompt — SkillPath AI

You are working on **SkillPath AI: AI-Based Skill Gap Analysis, Career Readiness Assessment and Internship Recommendation System**. Treat this repository as the source of truth. The target is a demo-ready academic MVP that can be finished and verified quickly.

## First: inspect before changing
1. Inspect the current folder tree, Git status if available, dependencies, frontend, backend, APIs, database, datasets, and every existing model artifact.
2. Make a short gap report: **Already exists / Missing / Needs modification / Optional**.
3. Preserve working code, trained models, data, API contracts, and components. Do not overwrite or retrain existing models. If this starter package is being used as a new repository, build on its current structure.
4. Before edits, explain the smallest safe implementation plan. Then make the changes, not just recommendations.

## MVP workflow
Student profile → resume text/PDF/DOCX analysis → target career → career requirements → strong/developing/missing skill gap → transparent readiness score → personalized SkillPath → opportunity matching → APPLY NOW / PREPARE & APPLY / NOT YET → dashboard.

## Stack
- Frontend: React, TypeScript, Tailwind CSS
- Backend: Python, FastAPI
- Data/scoring: simple Python services; use existing scikit-learn models if present
- Database: SQLite unless an existing working database should be reused

## Rules
- Keep it simple and explainable. Do not introduce microservices, vector databases, agent frameworks, scraping, or production infrastructure.
- Never present sample opportunities as live vacancies. Do not invent model accuracy or imply the readiness score is industry-certified.
- The dashboard must consume backend results, not hardcoded fake output.
- Validate user input, show readable errors, and never display stack traces to the user.
- Use deterministic fallback services if an existing model is missing or unusable; document that fallback.
- Avoid TODO placeholders for required MVP features.
- Do not change working dependencies or stack without a clear reason.

## Verify end-to-end
1. Start FastAPI and verify `/api/health` and `/docs`.
2. Start Vite and confirm the UI loads.
3. Test demo profile, resume extraction, career analysis, skill-gap categories, weighted readiness score, SkillPath actions, opportunity matches and all three classifications.
4. Run backend tests and frontend production build.
5. Fix only real blockers; report what was actually tested and any remaining limitations.
6. Keep the README setup commands accurate for Windows and macOS/Linux.

## Deliverables
- Implemented code, not pseudocode
- Gap analysis based on actual repository inspection
- Updated setup instructions
- Test/build results with honest status
- A short demo walkthrough and any limitations

Do not claim a test or build succeeded unless you ran it and saw the successful result.
