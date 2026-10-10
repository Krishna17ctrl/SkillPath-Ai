# SkillPath AI — Demo-ready MVP

SkillPath AI analyzes a student's skills against a target career, estimates readiness with a transparent project-level score, creates a prioritized learning path, and matches the profile to a small local demo opportunity dataset.

## MVP features
- Student profile form and resume text/PDF/DOCX upload
- Lightweight skill extraction with aliases and confidence
- Career requirements and strong/developing/missing skill comparison
- Transparent weighted readiness score (30/20/20/15/15)
- Rule-based personalized learning path and project suggestions
- Opportunity match score, explanations, and APPLY NOW / PREPARE & APPLY / NOT YET classification
- React dashboard connected to FastAPI
- SQLite profile persistence and sample demo data

**Data note:** opportunities are illustrative local demo records, not live vacancies. The app does not scrape job sites. Readiness categories are project-level estimates, not industry-certified assessments. The resume parser and recommendation engine are lightweight fallbacks, not a claim of a trained deep-learning model.

## Requirements
- Python 3.10+
- Node.js 18+ and npm

## Run on Windows (PowerShell)
Open two terminals from the project root.

### 1. Backend
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload
```
If PowerShell blocks activation, use `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\python.exe -m uvicorn main:app --reload`.

Backend: http://127.0.0.1:8000  
Swagger API docs: http://127.0.0.1:8000/docs  
Health: http://127.0.0.1:8000/api/health

### 2. Frontend
```powershell
cd frontend
npm install
npm run dev
```
Open the local URL printed by Vite (usually http://localhost:5173).

### 3. Run Automated Tests
```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests -v
```
All 17 automated tests validate auth, user isolation, resume parsing, and recommendation services.

## Run on macOS/Linux
Backend:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Demo walkthrough
1. Open the frontend and click **Load demo profile**.
2. Review the student profile and target career.
3. Paste resume text or upload a PDF/DOCX, then analyze it.
4. Click **Analyze career** to see skill gaps and readiness.
5. Review SkillPath actions and matched opportunities.
6. Open `/docs` to demonstrate the backend APIs.

## API endpoints
- `GET /api/health`
- `GET /api/careers`
- `GET /api/opportunities`
- `POST /api/profile`
- `POST /api/resume/analyze`
- `POST /api/career/analyze`
- `POST /api/skill-gap/analyze`
- `POST /api/readiness/calculate`
- `POST /api/skillpath/generate`
- `POST /api/opportunities/match`

## Design notes
- Existing trained models: place model artifacts in `backend/models/trained_models/` and add a wrapper in the relevant service. The MVP does not overwrite or retrain existing models.
- If integrating an existing frontend/backend, compare first and transplant only the needed services/routes rather than replacing working code.
- SQLite database is created automatically at `backend/skillpath.db`.
- CORS is configured for Vite's local development origin. Adjust `backend/main.py` if the frontend runs on a different origin.
