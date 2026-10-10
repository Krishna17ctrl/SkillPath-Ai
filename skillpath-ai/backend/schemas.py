from pydantic import BaseModel, Field, EmailStr
from typing import Any, Optional

# --- Authentication Schemas ---

class UserRegisterRequest(BaseModel):
    email: str = Field(..., description="Unique email address")
    full_name: str = Field(..., min_length=2, description="Candidate's full name")
    password: str = Field(..., min_length=6, description="Password (at least 6 characters)")

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str

class AuthResponse(BaseModel):
    token: str
    user: UserResponse

# --- Profile & Portfolio Schemas ---

class ProfileUpdateRequest(BaseModel):
    education: Optional[str] = None
    branch: Optional[str] = None
    semester: Optional[str] = None
    target_career: Optional[str] = None
    resume_text: Optional[str] = None

class SkillCreateRequest(BaseModel):
    skill_name: str = Field(..., min_length=1)
    proficiency: str = Field(default="Intermediate")

class SkillUpdateRequest(BaseModel):
    skill_name: Optional[str] = None
    proficiency: Optional[str] = None

class ProjectCreateRequest(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    technologies: str = Field(default="")
    category: Optional[str] = "Academic"
    completion_date: Optional[str] = ""
    repository_url: Optional[str] = ""
    live_url: Optional[str] = ""

class ProjectUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[str] = None
    category: Optional[str] = None
    completion_date: Optional[str] = None
    repository_url: Optional[str] = None
    live_url: Optional[str] = None

class CertificateCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    issuer: str = Field(..., min_length=1)
    issue_date: Optional[str] = ""
    expiry_date: Optional[str] = ""
    credential_id: Optional[str] = ""
    credential_url: Optional[str] = ""

class CertificateUpdateRequest(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None

# --- Core Algorithm Schemas (Experience removed) ---

class StudentProfile(BaseModel):
    name: str = "Student"
    education: str = "BCA"
    branch: str = "AIML"
    semester: str = "7th Semester"
    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    target_career: str = "Machine Learning Intern"
    resume_text: str = ""
    proficiency: dict[str, int] = Field(default_factory=dict)

    model_config = {"extra": "ignore"}

class CareerAnalysisRequest(BaseModel):
    profile: Optional[StudentProfile] = None
    target_career: Optional[str] = None

    model_config = {"extra": "ignore"}

class SkillGapRequest(BaseModel):
    student_skills: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)
    related_skills: dict[str, list[str]] = Field(default_factory=dict)
    proficiency: dict[str, int] = Field(default_factory=dict)

class ReadinessRequest(BaseModel):
    profile: StudentProfile
    skill_gap: dict[str, Any] = Field(default_factory=dict)

class SkillPathRequest(BaseModel):
    skill_gap: dict[str, Any] = Field(default_factory=dict)
    opportunities: list[dict[str, Any]] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)

class OpportunityMatchRequest(BaseModel):
    profile: StudentProfile
    target_career: Optional[str] = None
