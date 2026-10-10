import sys
from pathlib import Path
import sqlite3
import uuid

backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from main import app
from database import DB_PATH, get_connection, init_db

init_db()
client = TestClient(app)

def test_registration_and_hashing():
    email = f"alice_{uuid.uuid4().hex}@example.com"
    res = client.post("/api/auth/register", json={
        "email": email,
        "full_name": "Alice Developer",
        "password": "Password123!"
    })
    assert res.status_code == 200, res.text
    data = res.json()
    assert "token" in data
    assert data["user"]["email"] == email.lower()

    # Check password is hashed with bcrypt and NOT plaintext in database
    with get_connection() as conn:
        cur = conn.execute("SELECT hashed_password FROM users WHERE email = ?", (email.lower(),))
        row = cur.fetchone()
        assert row is not None
        assert row["hashed_password"] != "Password123!"
        assert row["hashed_password"].startswith("$2b$") or row["hashed_password"].startswith("$2a$")

    # Duplicate registration fails
    dup_res = client.post("/api/auth/register", json={
        "email": email,
        "full_name": "Alice Duplicate",
        "password": "Password123!"
    })
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"]

def test_login_and_logout():
    email = f"bob_{uuid.uuid4().hex}@example.com"
    reg = client.post("/api/auth/register", json={
        "email": email,
        "full_name": "Bob Builder",
        "password": "SecretPassword!"
    })
    assert reg.status_code == 200

    # Invalid password fails
    bad_login = client.post("/api/auth/login", json={
        "email": email,
        "password": "WrongPassword"
    })
    assert bad_login.status_code == 401

    # Valid login succeeds
    good_login = client.post("/api/auth/login", json={
        "email": email,
        "password": "SecretPassword!"
    })
    assert good_login.status_code == 200
    token = good_login.json()["token"]

    # Access protected route
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == email.lower()

    # Logout
    logout_res = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_res.status_code == 200

    # Token is now invalid
    me_after = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_after.status_code == 401

def test_user_isolation():
    # Create User A
    email_a = f"usera_{uuid.uuid4().hex}@example.com"
    res_a = client.post("/api/auth/register", json={
        "email": email_a,
        "full_name": "User Alpha",
        "password": "Password123!"
    })
    token_a = res_a.json()["token"]

    # Create User B
    email_b = f"userb_{uuid.uuid4().hex}@example.com"
    res_b = client.post("/api/auth/register", json={
        "email": email_b,
        "full_name": "User Beta",
        "password": "Password123!"
    })
    token_b = res_b.json()["token"]

    # User A adds a skill
    skill_res = client.post("/api/skills", json={
        "skill_name": "PyTorch",
        "proficiency": "Advanced"
    }, headers={"Authorization": f"Bearer {token_a}"})
    assert skill_res.status_code == 200
    skill_a_id = skill_res.json()["id"]

    # User B should NOT see User A's skill
    skills_b = client.get("/api/skills", headers={"Authorization": f"Bearer {token_b}"}).json()
    assert not any(s["id"] == skill_a_id for s in skills_b)

    # User B cannot delete User A's skill
    del_res = client.delete(f"/api/skills/{skill_a_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert del_res.status_code in [404, 403]

    # User A adds a project
    proj_res = client.post("/api/projects/user", json={
        "title": "Alpha Project",
        "description": "Alpha description",
        "technologies": "Python"
    }, headers={"Authorization": f"Bearer {token_a}"})
    assert proj_res.status_code == 200
    proj_a_id = proj_res.json()["id"]

    # User B cannot modify User A's project
    update_res = client.put(f"/api/projects/user/{proj_a_id}", json={
        "title": "Hacked Title"
    }, headers={"Authorization": f"Bearer {token_b}"})
    assert update_res.status_code in [404, 403]

    # Unauthenticated request rejected
    unauth = client.get("/api/skills")
    assert unauth.status_code == 401

if __name__ == "__main__":
    test_registration_and_hashing()
    print("[PASS] test_registration_and_hashing")
    test_login_and_logout()
    print("[PASS] test_login_and_logout")
    test_user_isolation()
    print("[PASS] test_user_isolation")
    print("\nAll Auth & User Isolation tests passed successfully!")
