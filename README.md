# SkillPath AI — Quickstart & Execution Guide

SkillPath AI is an intelligent career readiness and skill mapping platform. It analyzes a student's technical competencies against target roles, computes a project-level readiness score, builds an actionable learning path, and recommends matching demo opportunities.

---

## ⚡ Quick Start (1-Command Launch)

From the project root (`skillpath-ai-mvp`), run either of the following scripts in your terminal:

### Option A: Windows Command Prompt (CMD)
```cmd
run.bat
```

### Option B: Windows PowerShell
```powershell
.\run.ps1
```
*(If PowerShell restricts script execution, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first, then run `.\run.ps1`)*

Both scripts will automatically spawn two terminal windows:
- **Backend Service:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive API Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Frontend App:** [http://localhost:5173](http://localhost:5173)

---

## 💻 Manual Terminal Execution

If you prefer running services manually or are on macOS/Linux, open two separate terminal windows.

### Terminal 1: Backend (FastAPI)

#### Windows (PowerShell):
```powershell
cd skillpath-ai\backend
.\.venv\Scripts\Activate.ps1
# (Optional first time setup: pip install -r requirements.txt)
python -m uvicorn main:app --reload --port 8000
```
*Note: If PowerShell blocks script activation, directly run:*
```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

#### Windows (Command Prompt):
```cmd
cd skillpath-ai\backend
.\.venv\Scripts\activate.bat
python -m uvicorn main:app --reload --port 8000
```

#### macOS / Linux (Bash / Zsh):
```bash
cd skillpath-ai/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

---

### Terminal 2: Frontend (React + Vite + TypeScript)

#### All Platforms:
```bash
cd skillpath-ai/frontend
npm install
npm run dev
```
Access the application at [http://localhost:5173](http://localhost:5173).

---

## 🧪 Running the Automated Test Suite

The test suite validates authentication, user data isolation, resume parsing (text, PDF, DOCX), CRUD operations, and recommendation algorithms.

### Run All Tests with Pytest:
```powershell
cd skillpath-ai\backend
.\.venv\Scripts\python.exe -m pytest tests -v
```

### Run Specific Test Modules Directly:
```powershell
cd skillpath-ai\backend

# 1. Authentication & multi-user data isolation tests
.\.venv\Scripts\python.exe tests/test_auth_and_isolation.py

# 2. Student profile & CRUD operation tests
.\.venv\Scripts\python.exe tests/test_crud_and_profile.py

# 3. Resume text extraction & file upload tests
.\.venv\Scripts\python.exe tests/test_resume_upload.py

# 4. Recommendation, skill gap & readiness score tests
.\.venv\Scripts\python.exe tests/test_services.py
```

---

## 🌐 Key URLs & Endpoints

| Resource | URL | Description |
| :--- | :--- | :--- |
| **Frontend Application** | [http://localhost:5173](http://localhost:5173) | Interactive student dashboard & career advisor |
| **Backend API Root** | [http://127.0.0.1:8000](http://127.0.0.1:8000) | FastAPI server root |
| **API Documentation** | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) | Swagger UI for exploring and testing endpoints |
| **Health Check** | [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health) | Service uptime check |

### Core REST Endpoints
- `POST /api/auth/register` — Register a new student account
- `POST /api/auth/login` — Login & receive JWT authentication token
- `GET /api/profile/me` — Retrieve the authenticated student's profile
- `POST /api/resume/analyze` — Parse resume text or file (PDF/DOCX/TXT) for skills and projects
- `GET /api/careers` — List target career paths and required technical competencies
- `POST /api/career/analyze` — Analyze gap between student profile and target career
- `POST /api/readiness/calculate` — Compute readiness score & category
- `POST /api/skillpath/generate` — Generate structured learning milestones
- `GET /api/opportunities` — Retrieve demo job/internship listings
- `POST /api/opportunities/match` — Match profile with opportunities (APPLY NOW / PREPARE)

---

## 📂 Project Architecture

```text
skillpath-ai-mvp/
├── run.bat                         # 1-click launcher for Windows CMD
├── run.ps1                         # 1-click launcher for Windows PowerShell
├── README.md                       # Main execution guide
└── skillpath-ai/
    ├── backend/
    │   ├── main.py                 # FastAPI application routes & middleware
    │   ├── database.py             # SQLite schemas, connection & isolation
    │   ├── schemas.py              # Pydantic models & validation
    │   ├── requirements.txt        # Python dependencies (FastAPI, pytest, etc.)
    │   ├── skillpath.db            # SQLite database file
    │   ├── services/               # Gap analysis, readiness, resume parsing
    │   └── tests/                  # 17 automated tests across 4 test suites
    └── frontend/
        ├── package.json            # Frontend dependencies
        ├── vite.config.ts          # Vite build configuration
        └── src/                    # React UI, components, and state management
```

---

## ❓ Troubleshooting

1. **Port 8000 or 5173 Already in Use:**
   - Change the port when launching uvicorn: `uvicorn main:app --reload --port 8001`
   - Or stop the running process using Task Manager or `netstat -ano | findstr :8000`.
2. **PowerShell Script Execution Policy Error:**
   - Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in your PowerShell window.
3. **Database Reset:**
   - If you ever wish to re-initialize sample data, simply remove `skillpath-ai/backend/skillpath.db` and start the backend; it will auto-create and seed clean demo tables on startup.
