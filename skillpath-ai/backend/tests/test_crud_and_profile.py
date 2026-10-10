import sys
from pathlib import Path
import uuid

backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from main import app
from database import init_db

init_db()
client = TestClient(app)

def get_auth_token(prefix: str):
    email = f"{prefix}_{uuid.uuid4().hex}@example.com"
    res = client.post("/api/auth/register", json={
        "email": email,
        "full_name": f"{prefix.capitalize()} User",
        "password": "SecurePassword123!"
    })
    assert res.status_code == 200, res.text
    return res.json()["token"]

def test_empty_profile_onboarding():
    token = get_auth_token("newbie")
    headers = {"Authorization": f"Bearer {token}"}
    profile_res = client.get("/api/profile/me", headers=headers)
    assert profile_res.status_code == 200
    p = profile_res.json()
    assert p["skills"] == []
    assert p["projects"] == []
    assert p["certifications"] == []
    assert "experience" not in p
    assert p["education"] == ""
    assert p["branch"] == ""

def test_skills_crud():
    token = get_auth_token("skills_user")
    headers = {"Authorization": f"Bearer {token}"}

    # Add skill
    s1 = client.post("/api/skills", json={"skill_name": "Python", "proficiency": "Expert"}, headers=headers)
    assert s1.status_code == 200
    s1_id = s1.json()["id"]
    assert s1.json()["skill_name"] == "Python"
    assert s1.json()["proficiency"] == "Expert"

    # Add second skill
    s2 = client.post("/api/skills", json={"skill_name": "SQL (PostgreSQL)", "proficiency": "Advanced"}, headers=headers)
    assert s2.status_code == 200

    # Duplicate skill rejected
    dup = client.post("/api/skills", json={"skill_name": "python"}, headers=headers)
    assert dup.status_code == 400
    assert "already exists" in dup.json()["detail"]

    # List skills
    skills_list = client.get("/api/skills", headers=headers).json()
    assert len(skills_list) == 2

    # Edit skill
    edited = client.put(f"/api/skills/{s1_id}", json={"skill_name": "Python 3.12", "proficiency": "Expert"}, headers=headers)
    assert edited.status_code == 200
    assert edited.json()["skill_name"] == "Python 3.12"

    # Delete skill
    del_res = client.delete(f"/api/skills/{s1_id}", headers=headers)
    assert del_res.status_code == 200
    remaining = client.get("/api/skills", headers=headers).json()
    assert len(remaining) == 1

def test_projects_crud():
    token = get_auth_token("proj_user")
    headers = {"Authorization": f"Bearer {token}"}

    # Required fields validation (missing title/description fails)
    bad_proj = client.post("/api/projects/user", json={"title": ""}, headers=headers)
    assert bad_proj.status_code == 422 or bad_proj.status_code == 400

    # Valid project creation
    p1 = client.post("/api/projects/user", json={
        "title": "Autonomous Drone Navigator",
        "description": "Simulated quadcopter path planning in Python using A* search and OpenCV.",
        "technologies": "Python, OpenCV, NumPy",
        "category": "Robotics",
        "completion_date": "2024-05",
        "repository_url": "https://github.com/example/drone-nav",
        "live_url": "https://demo.example.com"
    }, headers=headers)
    assert p1.status_code == 200
    p1_id = p1.json()["id"]
    assert p1.json()["title"] == "Autonomous Drone Navigator"

    # List projects
    projs = client.get("/api/projects/user", headers=headers).json()
    assert len(projs) == 1

    # Edit project
    edited = client.put(f"/api/projects/user/{p1_id}", json={
        "title": "Autonomous Drone Navigator v2",
        "description": "Updated path planning with ROS2 integration."
    }, headers=headers)
    assert edited.status_code == 200
    assert edited.json()["title"] == "Autonomous Drone Navigator v2"

    # Delete project
    del_res = client.delete(f"/api/projects/user/{p1_id}", headers=headers)
    assert del_res.status_code == 200
    assert len(client.get("/api/projects/user", headers=headers).json()) == 0

def test_certificates_crud():
    token = get_auth_token("cert_user")
    headers = {"Authorization": f"Bearer {token}"}

    # Required fields validation (missing issuer fails)
    bad_cert = client.post("/api/certificates", json={"name": "AWS Certified"}, headers=headers)
    assert bad_cert.status_code == 422 or bad_cert.status_code == 400

    # Valid certificate creation
    c1 = client.post("/api/certificates", json={
        "name": "AWS Certified Solutions Architect",
        "issuer": "Amazon Web Services",
        "issue_date": "2024-01-15",
        "expiry_date": "2027-01-15",
        "credential_id": "AWS-829104",
        "credential_url": "https://aws.amazon.com/verify"
    }, headers=headers)
    assert c1.status_code == 200
    c1_id = c1.json()["id"]
    assert c1.json()["name"] == "AWS Certified Solutions Architect"

    # List certificates
    certs = client.get("/api/certificates", headers=headers).json()
    assert len(certs) == 1

    # Edit certificate
    edited = client.put(f"/api/certificates/{c1_id}", json={
        "name": "AWS Solutions Architect — Associate"
    }, headers=headers)
    assert edited.status_code == 200
    assert edited.json()["name"] == "AWS Solutions Architect — Associate"

    # Delete certificate
    del_res = client.delete(f"/api/certificates/{c1_id}", headers=headers)
    assert del_res.status_code == 200
    assert len(client.get("/api/certificates", headers=headers).json()) == 0

def test_profile_update():
    token = get_auth_token("prof_edit_user")
    headers = {"Authorization": f"Bearer {token}"}

    # Update profile
    up_res = client.put("/api/profile/me", json={
        "education": "B.Tech. in Computer Science",
        "branch": "Artificial Intelligence & Data Science",
        "semester": "8th Semester",
        "target_career": "Data Scientist Intern"
    }, headers=headers)
    assert up_res.status_code == 200
    data = up_res.json()
    assert data["education"] == "B.Tech. in Computer Science"
    assert data["branch"] == "Artificial Intelligence & Data Science"
    assert data["target_career"] == "Data Scientist Intern"

if __name__ == "__main__":
    test_empty_profile_onboarding()
    print("[PASS] test_empty_profile_onboarding")
    test_skills_crud()
    print("[PASS] test_skills_crud")
    test_projects_crud()
    print("[PASS] test_projects_crud")
    test_certificates_crud()
    print("[PASS] test_certificates_crud")
    test_profile_update()
    print("[PASS] test_profile_update")
    print("\nAll CRUD & Profile tests passed successfully!")
