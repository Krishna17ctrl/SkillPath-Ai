# SkillPath AI — Career Readiness & Skill Mapping Platform

SkillPath AI evaluates a student's technical proficiencies against target industry careers, computes a project-level readiness benchmark, builds a personalized learning roadmap, and matches the profile against curated internship and job opportunities.

---

## 🌐 Single Unified Website Link

The application now runs as a **single unified service** where FastAPI serves both the interactive React frontend and all backend REST endpoints under one port.

> ### 👉 **Unified Website Link:** [http://127.0.0.1:8000](http://127.0.0.1:8000) (or [http://localhost:8000](http://localhost:8000))
> - **Interactive Frontend UI:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
> - **Interactive API Docs (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
> - **Health & Status Check:** [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

No need to open or configure separate URLs for frontend and backend. Everything is unified.

---

## ⚡ 1-Click Execution (Terminal)

From the project root directory (`skillpath-ai-mvp`), run either command:

### Windows Command Prompt (CMD):
```cmd
run.bat
```

### Windows PowerShell:
```powershell
.\run.ps1
```
*(If PowerShell restricts script execution, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once, then run `.\run.ps1`)*

The script automatically:
1. Validates or builds the frontend bundle into `skillpath-ai/frontend/dist`.
2. Starts the backend FastAPI server on port `8000`.
3. Opens [http://127.0.0.1:8000](http://127.0.0.1:8000) directly in your default browser.

---

## 💻 Manual Terminal Execution

### Run Single Unified Application
```powershell
cd skillpath-ai\backend
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

### (Optional) Frontend Independent Development Mode
If making live edits to React components with instant Hot Module Reloading (Vite):
```powershell
cd skillpath-ai\frontend
npm run dev
```
Development proxy will run at [http://localhost:5173](http://localhost:5173) and automatically talk to the backend on port 8000.

---

## 🐙 GitHub Repository: Push & Clone Instructions

### Push this Project to GitHub (Single Repository Link)

1. **Create a new empty repository on GitHub** (e.g. `https://github.com/<YOUR-USERNAME>/skillpath-ai`).
2. Run these commands from the root folder (`skillpath-ai-mvp`):

```bash
# 1. Add your remote GitHub repository
git remote add origin https://github.com/<YOUR-USERNAME>/skillpath-ai.git

# 2. Push all code to GitHub
git push -u origin main
```

---

### Clone & Run for Any User / Collaborator

Anyone can clone the entire repository using the single GitHub repository link:

```bash
# 1. Clone repository
git clone https://github.com/<YOUR-USERNAME>/skillpath-ai.git
cd skillpath-ai

# 2. Run immediately (Windows)
run.bat
```

---

## 🛠️ Errors Solved & Key Enhancements

1. **Fixed "Run Live Analysis" & Profile Saving:**
   - **Root Cause:** The frontend invoked `api.saveProfile(clean)` targeting `POST /api/profile`, but the FastAPI backend lacked the `POST /api/profile` endpoint, causing HTTP 404 and halting analysis execution.
   - **Fix:** Implemented `@app.post("/api/profile")` and `@app.get("/api/profile")` in FastAPI to handle both authenticated and guest/demo profiles.
   - **Schema Support:** Updated Pydantic's `StudentProfile` in `schemas.py` to accept `experience: list[str]` and added `extra = "ignore"` for robust validation.
   - **Fuzzy Role Matching:** Upgraded career resolution in `POST /api/career/analyze` to handle case differences, IDs, and partial role names with reliable fallback.

2. **Single Link Architecture:**
   - Fast-served the built React production bundle directly through FastAPI via `StaticFiles` and SPA fallback routing.
   - Dynamically configured `API_BASE` in `frontend/src/api.ts` to use same-origin relative endpoints when running on port `8000` and proxying on port `5173`.

3. **Auto-Compute on Mount:**
   - The dashboard now automatically computes and renders live readiness scores and opportunity matches as soon as the app loads.

4. **Multi-Disciplinary Global Career Tracks:**
   - Expanded far beyond engineering / B.Tech roles to support global opportunities across **Finance, Accounting, UI/UX Design, Product Management, Marketing, HR, Operations, Healthcare, and Cloud/Cybersecurity**.
   - Added 18+ comprehensive global careers and benchmark roles catering to B.Com, B.A., B.Sc., B.B.A., B.Des, B.Tech, M.B.A., and Self-Taught candidates.

5. **Accredited Course Recommendations & Degree Bridging:**
   - Integrated curated, accredited online courses from **Coursera, edX, Google, Stanford Online, CFI, and Harvard Online**.
   - When candidates have non-traditional or diverse degrees, verified credentials and coursework act as a **Degree Bridge** to satisfy baseline qualifications and unlock competitive opportunities.

6. **Candidate Switcher & 1-Click Profile Clearing:**
   - Added a **"Switch Candidate"** and **"Clear Profile"** feature in both the sticky topbar and header CTA.
   - Users can now clear everything with one click to evaluate a completely new person from scratch, or toggle between pre-configured multi-disciplinary candidate personas (Sarah Jenkins - Finance, Elena Rostova - Design, Marcus Chen - Product, Amara Okafor - Marketing, Prajwal - AI).

7. **17/17 Automated Tests Passing:**
   - Replaced static file-modification timestamps with UUIDs to guarantee test idempotency across multiple runs.
   - Pytest suite passes 100% across authentication, multi-tenant isolation, CRUD, resume parsing, and career algorithms.

---

## 🧪 Run Automated Tests

```powershell
cd skillpath-ai\backend
.\.venv\Scripts\python.exe -m pytest tests -v
```

All 17 tests will execute and confirm:
- User registration, login, logout, and bcrypt hashing
- Multi-user data isolation (User B cannot access or modify User A's data)
- Skills, projects, and certificates CRUD operations
- Multi-format resume parsing (PDF, DOCX, TXT)
- Transparent readiness scoring and prioritized action path synthesis
