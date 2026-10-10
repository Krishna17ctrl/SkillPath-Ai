from pathlib import Path
import io
import re
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pypdf import PdfReader
from docx import Document

from database import (
    init_db, create_user, authenticate_user, create_session,
    get_user_by_token, delete_session, get_user_profile, update_user_profile,
    get_user_skills, add_user_skill, update_user_skill, delete_user_skill,
    get_user_projects, add_user_project, update_user_project, delete_user_project,
    get_user_certificates, add_user_certificate, update_user_certificate, delete_user_certificate,
    get_full_candidate_profile
)
from schemas import (
    UserRegisterRequest, UserLoginRequest, UserResponse, AuthResponse,
    ProfileUpdateRequest, SkillCreateRequest, SkillUpdateRequest,
    ProjectCreateRequest, ProjectUpdateRequest, CertificateCreateRequest, CertificateUpdateRequest,
    StudentProfile, CareerAnalysisRequest, SkillGapRequest, ReadinessRequest,
    SkillPathRequest, OpportunityMatchRequest
)
from services.data_loader import careers, opportunities, projects_catalog
from services.skill_extractor import extract_skills
from services.skill_gap import analyze_skill_gap
from services.readiness import calculate_readiness
from services.matcher import match_opportunities
from services.skillpath import generate_skillpath

app = FastAPI(
    title="SkillPath AI API",
    version="1.0.0",
    description="Career readiness assessment, skill gap analysis, personalized learning paths, and opportunity matching engine."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

# --- Auth Dependency ---

def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authentication token required. Please log in.")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization format. Expected 'Bearer <token>'.")
    user = get_user_by_token(parts[1])
    if not user:
        raise HTTPException(status_code=401, detail="Session expired or invalid token. Please log in again.")
    return user

def get_optional_user(authorization: str | None = Header(default=None)) -> dict | None:
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return get_user_by_token(parts[1])
    return None

# --- General & Reference Endpoints ---

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "SkillPath AI API", "version": "1.0.0"}

@app.get("/api/careers")
def get_careers():
    return careers()

@app.get("/api/opportunities")
def get_opportunities():
    return opportunities()

@app.get("/api/projects")
def get_projects():
    return projects_catalog()

# --- Authentication Endpoints ---

@app.post("/api/auth/register", response_model=AuthResponse)
def register(request: UserRegisterRequest):
    email = request.email.strip().lower()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise HTTPException(status_code=400, detail="Please provide a valid email address.")
    if len(request.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")
    try:
        user = create_user(email=email, full_name=request.full_name, password=request.password)
        token = create_session(user["id"])
        return {"token": token, "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login", response_model=AuthResponse)
def login(request: UserLoginRequest):
    user = authenticate_user(email=request.email, password=request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    token = create_session(user["id"])
    return {"token": token, "user": user}

@app.post("/api/auth/logout")
def logout(authorization: str | None = Header(default=None)):
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            delete_session(parts[1])
    return {"message": "Logged out successfully"}

@app.get("/api/auth/me", response_model=UserResponse)
def get_me(user: dict = Depends(get_current_user)):
    return user

# --- User Profile Endpoints ---

@app.get("/api/profile/me")
def get_my_profile(user: dict = Depends(get_current_user)):
    return get_full_candidate_profile(user["id"])

@app.put("/api/profile/me")
def update_my_profile(request: ProfileUpdateRequest, user: dict = Depends(get_current_user)):
    updates = request.model_dump(exclude_unset=True)
    update_user_profile(user["id"], updates)
    return get_full_candidate_profile(user["id"])

@app.post("/api/profile")
def save_profile(
    profile: StudentProfile,
    user: dict | None = Depends(get_optional_user)
):
    """
    Saves student profile. Works seamlessly for both authenticated users
    (persisted in database) and demo/guest sessions.
    """
    if user:
        update_user_profile(user["id"], {
            "education": profile.education,
            "branch": profile.branch,
            "semester": profile.semester,
            "target_career": profile.target_career,
            "resume_text": profile.resume_text,
        })
    return {"status": "ok", "profile": profile.model_dump()}

@app.get("/api/profile")
def get_profile(user: dict | None = Depends(get_optional_user)):
    if user:
        return get_full_candidate_profile(user["id"])
    return {"status": "ok", "message": "Demo profile active"}

# --- User Skills CRUD (Scoped to User) ---

@app.get("/api/skills")
def list_skills(user: dict = Depends(get_current_user)):
    return get_user_skills(user["id"])

@app.post("/api/skills")
def add_skill(request: SkillCreateRequest, user: dict = Depends(get_current_user)):
    try:
        return add_user_skill(user["id"], request.skill_name, request.proficiency)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/skills/{skill_id}")
def edit_skill(skill_id: int, request: SkillUpdateRequest, user: dict = Depends(get_current_user)):
    try:
        return update_user_skill(user["id"], skill_id, request.skill_name, request.proficiency)
    except KeyError:
        raise HTTPException(status_code=404, detail="Skill not found or access denied.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/skills/{skill_id}")
def remove_skill(skill_id: int, user: dict = Depends(get_current_user)):
    try:
        delete_user_skill(user["id"], skill_id)
        return {"message": "Skill deleted successfully"}
    except KeyError:
        raise HTTPException(status_code=404, detail="Skill not found or access denied.")

# --- User Projects CRUD (Scoped to User) ---

@app.get("/api/projects/user")
def list_user_projects(user: dict = Depends(get_current_user)):
    return get_user_projects(user["id"])

@app.post("/api/projects/user")
def add_project(request: ProjectCreateRequest, user: dict = Depends(get_current_user)):
    try:
        return add_user_project(user["id"], request.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/projects/user/{project_id}")
def edit_project(project_id: int, request: ProjectUpdateRequest, user: dict = Depends(get_current_user)):
    try:
        return update_user_project(user["id"], project_id, request.model_dump(exclude_unset=True))
    except KeyError:
        raise HTTPException(status_code=404, detail="Project not found or access denied.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/projects/user/{project_id}")
def remove_project(project_id: int, user: dict = Depends(get_current_user)):
    try:
        delete_user_project(user["id"], project_id)
        return {"message": "Project deleted successfully"}
    except KeyError:
        raise HTTPException(status_code=404, detail="Project not found or access denied.")

# --- User Certificates CRUD (Scoped to User) ---

@app.get("/api/certificates")
def list_certificates(user: dict = Depends(get_current_user)):
    return get_user_certificates(user["id"])

@app.post("/api/certificates")
def add_certificate(request: CertificateCreateRequest, user: dict = Depends(get_current_user)):
    try:
        return add_user_certificate(user["id"], request.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/certificates/{cert_id}")
def edit_certificate(cert_id: int, request: CertificateUpdateRequest, user: dict = Depends(get_current_user)):
    try:
        return update_user_certificate(user["id"], cert_id, request.model_dump(exclude_unset=True))
    except KeyError:
        raise HTTPException(status_code=404, detail="Certificate not found or access denied.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/certificates/{cert_id}")
def remove_certificate(cert_id: int, user: dict = Depends(get_current_user)):
    try:
        delete_user_certificate(user["id"], cert_id)
        return {"message": "Certificate deleted successfully"}
    except KeyError:
        raise HTTPException(status_code=404, detail="Certificate not found or access denied.")

# --- Robust Resume Extraction (End-to-End Fixed) ---

@app.post("/api/resume/analyze")
async def analyze_resume(
    text: str = Form(default=""),
    file: UploadFile | None = File(default=None)
):
    extracted_text = (text or "").strip()

    if file is not None and file.filename:
        # Check filename extension
        suffix = Path(file.filename).suffix.lower()
        if suffix not in [".pdf", ".docx", ".txt"]:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format '{suffix}'. Please upload a PDF, DOCX, or TXT file."
            )

        # Read content safely in memory and validate file size (max 5 MB)
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty (0 bytes). Please upload a valid document."
            )
        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="The resume file exceeds the maximum 5 MB limit. Please upload a smaller file."
            )

        if suffix == ".pdf":
            try:
                reader = PdfReader(io.BytesIO(content))
                page_texts = [page.extract_text() or "" for page in reader.pages]
                pdf_text = "\n".join(page_texts).strip()
                if not pdf_text:
                    raise HTTPException(
                        status_code=400,
                        detail="No extractable text was found in this PDF. It may be an image scan. OCR is not supported; please paste your resume text or upload a text-based document."
                    )
                extracted_text = pdf_text
            except HTTPException:
                raise
            except Exception as exc:
                raise HTTPException(
                    status_code=400,
                    detail="Could not parse this PDF file. It may be corrupted or password-protected. Try pasting the resume text."
                ) from exc

        elif suffix == ".docx":
            try:
                doc = Document(io.BytesIO(content))
                doc_text = "\n".join(p.text for p in doc.paragraphs).strip()
                if not doc_text:
                    raise HTTPException(
                        status_code=400,
                        detail="No text was found in this DOCX file. Please verify the document contains written content."
                    )
                extracted_text = doc_text
            except HTTPException:
                raise
            except Exception as exc:
                raise HTTPException(
                    status_code=400,
                    detail="Could not parse this DOCX file. Please upload a valid Word document or paste the resume text."
                ) from exc

        elif suffix == ".txt":
            try:
                txt_content = content.decode("utf-8", errors="ignore").strip()
                if not txt_content:
                    raise HTTPException(
                        status_code=400,
                        detail="The uploaded text file is empty. Please verify the file content."
                    )
                extracted_text = txt_content
            except Exception as exc:
                raise HTTPException(
                    status_code=400,
                    detail="Could not read the text file encoding."
                ) from exc

    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Please provide resume text or upload a valid PDF, DOCX, or TXT file to analyze."
        )

    # Extract available skills, education, projects, certifications (NO experience stored)
    result = extract_skills(extracted_text)
    return result

# --- Career Readiness & Opportunity Matching Workflows ---

@app.post("/api/career/analyze")
def analyze_career(
    request: CareerAnalysisRequest,
    user: dict | None = Depends(get_optional_user)
):
    # If user is authenticated, use their real profile unless explicit override provided
    if user:
        profile_data = get_full_candidate_profile(user["id"])
        target = request.target_career or profile_data.get("target_career")
    elif request.profile:
        profile_data = request.profile.model_dump()
        target = request.target_career or profile_data.get("target_career")
    else:
        raise HTTPException(status_code=400, detail="Profile data or active user authentication is required.")

    # Resilient target career matching (exact, ID, case-insensitive, or substring fallback)
    all_careers = careers()
    target_str = str(target or "").strip().lower()
    selected = next(
        (c for c in all_careers if c["name"].lower() == target_str or c["id"].lower() == target_str),
        None
    )
    if not selected:
        selected = next(
            (c for c in all_careers if target_str in c["name"].lower() or c["name"].lower() in target_str),
            None
        )
    if not selected and all_careers:
        selected = all_careers[0]

    if not selected:
        raise HTTPException(status_code=404, detail=f"Target career '{target}' was not found. Please choose a valid role.")

    skills_input = profile_data.get("skills") or []
    prof_input = profile_data.get("proficiency") or {}

    gap = analyze_skill_gap(
        skills_input,
        selected["required_skills"],
        selected.get("related_skills"),
        prof_input
    )
    readiness = calculate_readiness(profile_data, gap)
    matched_opps = match_opportunities({**profile_data, "target_career": selected["name"]}, selected["name"])
    path = generate_skillpath(gap, matched_opps)

    return {
        "target_career": selected,
        "skill_gap": gap,
        "readiness": readiness,
        "skillpath": path,
        "opportunities": matched_opps[:12],
        "opportunity_summary": {
            "apply_now": sum(o["classification"] == "APPLY NOW" for o in matched_opps),
            "prepare_and_apply": sum(o["classification"] == "PREPARE & APPLY" for o in matched_opps),
            "not_yet": sum(o["classification"] == "NOT YET" for o in matched_opps)
        }
    }

@app.post("/api/skill-gap/analyze")
def skill_gap_endpoint(request: SkillGapRequest):
    return analyze_skill_gap(request.student_skills, request.required_skills, request.related_skills, request.proficiency)

@app.post("/api/readiness/calculate")
def readiness_endpoint(request: ReadinessRequest):
    return calculate_readiness(request.profile.model_dump(), request.skill_gap)

@app.post("/api/skillpath/generate")
def skillpath_endpoint(request: SkillPathRequest):
    return generate_skillpath(request.skill_gap, request.opportunities)

@app.post("/api/opportunities/match")
def opportunities_match_endpoint(request: OpportunityMatchRequest):
    return match_opportunities(request.profile.model_dump(), request.target_career)

# --- Static Frontend Serving (Single Unified Website on Port 8000) ---
frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if (frontend_dist / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

@app.get("/{full_path:path}")
async def serve_spa_frontend(full_path: str):
    # Avoid intercepting API routes or Swagger docs
    if full_path.startswith("api/") or full_path in ["docs", "redoc", "openapi.json"]:
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    candidate_file = frontend_dist / full_path
    if candidate_file.is_file():
        return FileResponse(candidate_file)

    index_html = frontend_dist / "index.html"
    if index_html.is_file():
        return FileResponse(index_html)

    return {
        "status": "ok",
        "service": "SkillPath AI",
        "message": "Frontend build not detected. Run 'npm run build' inside frontend/ to serve the unified UI.",
        "api_docs": "/docs"
    }

