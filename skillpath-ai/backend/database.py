import sqlite3
from pathlib import Path
import json
import secrets
from datetime import datetime, timedelta
import bcrypt

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "skillpath.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def init_db():
    with get_connection() as conn:
        # Safe migration: if old profiles table exists without user_id, preserve as legacy_profiles
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='profiles'")
        if cur.fetchone():
            col_cur = conn.execute("PRAGMA table_info(profiles)")
            cols = [row["name"] for row in col_cur.fetchall()]
            if "user_id" not in cols:
                conn.execute("DROP TABLE IF EXISTS legacy_profiles")
                conn.execute("ALTER TABLE profiles RENAME TO legacy_profiles")

        # Users table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL COLLATE NOCASE,
                full_name TEXT NOT NULL,
                hashed_password TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # User Profile settings (scoped by user_id)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                education TEXT DEFAULT '',
                branch TEXT DEFAULT '',
                semester TEXT DEFAULT '',
                target_career TEXT DEFAULT 'Machine Learning Intern',
                resume_text TEXT DEFAULT '',
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # User Skills table (normalized, scoped by user_id)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                skill_name TEXT NOT NULL,
                proficiency TEXT DEFAULT 'Intermediate',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, skill_name COLLATE NOCASE)
            )
        """)

        # User Projects table (scoped by user_id)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                technologies TEXT NOT NULL,
                category TEXT DEFAULT 'Academic',
                completion_date TEXT DEFAULT '',
                repository_url TEXT DEFAULT '',
                live_url TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # User Certificates table (scoped by user_id)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                issuer TEXT NOT NULL,
                issue_date TEXT DEFAULT '',
                expiry_date TEXT DEFAULT '',
                credential_id TEXT DEFAULT '',
                credential_url TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Sessions table for bearer token management
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                expires_at TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Retain legacy profiles table if present for safety
        conn.execute("""
            CREATE TABLE IF NOT EXISTS legacy_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# --- Auth & User Functions ---

def create_user(email: str, full_name: str, password: str) -> dict:
    email_clean = email.strip().lower()
    name_clean = full_name.strip()
    hashed = hash_password(password)

    with get_connection() as conn:
        # Check if user already exists
        cur = conn.execute("SELECT id FROM users WHERE email = ?", (email_clean,))
        if cur.fetchone():
            raise ValueError("An account with this email already exists.")

        cur = conn.execute(
            "INSERT INTO users (email, full_name, hashed_password) VALUES (?, ?, ?)",
            (email_clean, name_clean, hashed)
        )
        user_id = cur.lastrowid

        # Initialize an empty profile for the new user (no fabricated data!)
        conn.execute(
            "INSERT INTO profiles (user_id, education, branch, semester, target_career, resume_text) VALUES (?, '', '', '', 'Machine Learning Intern', '')",
            (user_id,)
        )
        conn.commit()
        return {"id": user_id, "email": email_clean, "full_name": name_clean}

def authenticate_user(email: str, password: str) -> dict | None:
    email_clean = email.strip().lower()
    with get_connection() as conn:
        cur = conn.execute("SELECT id, email, full_name, hashed_password FROM users WHERE email = ?", (email_clean,))
        row = cur.fetchone()
        if not row:
            return None
        if not verify_password(password, row["hashed_password"]):
            return None
        return {"id": row["id"], "email": row["email"], "full_name": row["full_name"]}

def create_session(user_id: int, days_valid: int = 7) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = (datetime.utcnow() + timedelta(days=days_valid)).isoformat()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
            (token, user_id, expires_at)
        )
        conn.commit()
    return token

def get_user_by_token(token: str) -> dict | None:
    if not token:
        return None
    with get_connection() as conn:
        cur = conn.execute(
            """
            SELECT u.id, u.email, u.full_name, s.expires_at 
            FROM sessions s 
            JOIN users u ON s.user_id = u.id 
            WHERE s.token = ?
            """,
            (token,)
        )
        row = cur.fetchone()
        if not row:
            return None
        # Check expiration
        try:
            expires = datetime.fromisoformat(row["expires_at"])
            if datetime.utcnow() > expires:
                conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
                conn.commit()
                return None
        except Exception:
            return None

        return {"id": row["id"], "email": row["email"], "full_name": row["full_name"]}

def delete_session(token: str) -> bool:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
        return cur.rowcount > 0

# --- Profile Management ---

def get_user_profile(user_id: int) -> dict:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT education, branch, semester, target_career, resume_text, updated_at FROM profiles WHERE user_id = ?",
            (user_id,)
        )
        row = cur.fetchone()
        if not row:
            # Create if missing
            conn.execute(
                "INSERT INTO profiles (user_id, education, branch, semester, target_career, resume_text) VALUES (?, '', '', '', 'Machine Learning Intern', '')",
                (user_id,)
            )
            conn.commit()
            return {
                "education": "", "branch": "", "semester": "",
                "target_career": "Machine Learning Intern", "resume_text": ""
            }
        return dict(row)

def update_user_profile(user_id: int, updates: dict) -> dict:
    with get_connection() as conn:
        fields = []
        values = []
        for key in ["education", "branch", "semester", "target_career", "resume_text"]:
            if key in updates:
                fields.append(f"{key} = ?")
                values.append(updates[key])
        if fields:
            fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(user_id)
            conn.execute(
                f"UPDATE profiles SET {', '.join(fields)} WHERE user_id = ?",
                tuple(values)
            )
            conn.commit()
    return get_user_profile(user_id)

# --- Skills CRUD (Scoped by user_id) ---

def get_user_skills(user_id: int) -> list[dict]:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, skill_name, proficiency, created_at FROM user_skills WHERE user_id = ? ORDER BY skill_name ASC",
            (user_id,)
        )
        return [dict(row) for row in cur.fetchall()]

def add_user_skill(user_id: int, skill_name: str, proficiency: str = "Intermediate") -> dict:
    name_clean = skill_name.strip()
    if not name_clean:
        raise ValueError("Skill name cannot be empty.")
    valid_prof = proficiency if proficiency in ["Beginner", "Intermediate", "Advanced", "Expert"] else "Intermediate"

    with get_connection() as conn:
        # Check duplicate
        cur = conn.execute(
            "SELECT id FROM user_skills WHERE user_id = ? AND skill_name = ? COLLATE NOCASE",
            (user_id, name_clean)
        )
        if cur.fetchone():
            raise ValueError(f"Skill '{name_clean}' already exists in your profile.")

        cur = conn.execute(
            "INSERT INTO user_skills (user_id, skill_name, proficiency) VALUES (?, ?, ?)",
            (user_id, name_clean, valid_prof)
        )
        conn.commit()
        return {"id": cur.lastrowid, "skill_name": name_clean, "proficiency": valid_prof}

def update_user_skill(user_id: int, skill_id: int, skill_name: str | None, proficiency: str | None) -> dict:
    with get_connection() as conn:
        cur = conn.execute("SELECT id, skill_name, proficiency FROM user_skills WHERE id = ? AND user_id = ?", (skill_id, user_id))
        row = cur.fetchone()
        if not row:
            raise KeyError("Skill not found or access denied.")

        new_name = skill_name.strip() if skill_name is not None and skill_name.strip() else row["skill_name"]
        new_prof = proficiency if proficiency in ["Beginner", "Intermediate", "Advanced", "Expert"] else row["proficiency"]

        # If renaming, check for collision
        if new_name.lower() != row["skill_name"].lower():
            cur = conn.execute("SELECT id FROM user_skills WHERE user_id = ? AND skill_name = ? COLLATE NOCASE AND id != ?", (user_id, new_name, skill_id))
            if cur.fetchone():
                raise ValueError(f"Another skill named '{new_name}' already exists.")

        conn.execute(
            "UPDATE user_skills SET skill_name = ?, proficiency = ? WHERE id = ? AND user_id = ?",
            (new_name, new_prof, skill_id, user_id)
        )
        conn.commit()
        return {"id": skill_id, "skill_name": new_name, "proficiency": new_prof}

def delete_user_skill(user_id: int, skill_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM user_skills WHERE id = ? AND user_id = ?", (skill_id, user_id))
        conn.commit()
        if cur.rowcount == 0:
            raise KeyError("Skill not found or access denied.")
        return True

# --- Projects CRUD (Scoped by user_id) ---

def get_user_projects(user_id: int) -> list[dict]:
    with get_connection() as conn:
        cur = conn.execute(
            """
            SELECT id, title, description, technologies, category, completion_date, repository_url, live_url, created_at 
            FROM user_projects 
            WHERE user_id = ? 
            ORDER BY created_at DESC
            """,
            (user_id,)
        )
        return [dict(row) for row in cur.fetchall()]

def add_user_project(user_id: int, project: dict) -> dict:
    title = project.get("title", "").strip()
    desc = project.get("description", "").strip()
    tech = project.get("technologies", "").strip()
    if not title:
        raise ValueError("Project title is required.")
    if not desc:
        raise ValueError("Project description is required.")

    category = project.get("category", "Academic").strip() or "Academic"
    comp_date = project.get("completion_date", "").strip()
    repo_url = project.get("repository_url", "").strip()
    live_url = project.get("live_url", "").strip()

    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO user_projects (user_id, title, description, technologies, category, completion_date, repository_url, live_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, title, desc, tech, category, comp_date, repo_url, live_url)
        )
        conn.commit()
        return {
            "id": cur.lastrowid, "title": title, "description": desc,
            "technologies": tech, "category": category, "completion_date": comp_date,
            "repository_url": repo_url, "live_url": live_url
        }

def update_user_project(user_id: int, project_id: int, updates: dict) -> dict:
    with get_connection() as conn:
        cur = conn.execute("SELECT id FROM user_projects WHERE id = ? AND user_id = ?", (project_id, user_id))
        if not cur.fetchone():
            raise KeyError("Project not found or access denied.")

        fields = []
        values = []
        for key in ["title", "description", "technologies", "category", "completion_date", "repository_url", "live_url"]:
            if key in updates and updates[key] is not None:
                val = str(updates[key]).strip()
                if key in ["title", "description"] and not val:
                    raise ValueError(f"{key.capitalize()} cannot be empty.")
                fields.append(f"{key} = ?")
                values.append(val)

        if fields:
            values.extend([project_id, user_id])
            conn.execute(
                f"UPDATE user_projects SET {', '.join(fields)} WHERE id = ? AND user_id = ?",
                tuple(values)
            )
            conn.commit()

        cur = conn.execute("SELECT id, title, description, technologies, category, completion_date, repository_url, live_url FROM user_projects WHERE id = ?", (project_id,))
        return dict(cur.fetchone())

def delete_user_project(user_id: int, project_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM user_projects WHERE id = ? AND user_id = ?", (project_id, user_id))
        conn.commit()
        if cur.rowcount == 0:
            raise KeyError("Project not found or access denied.")
        return True

# --- Certificates CRUD (Scoped by user_id) ---

def get_user_certificates(user_id: int) -> list[dict]:
    with get_connection() as conn:
        cur = conn.execute(
            """
            SELECT id, name, issuer, issue_date, expiry_date, credential_id, credential_url, created_at 
            FROM user_certificates 
            WHERE user_id = ? 
            ORDER BY created_at DESC
            """,
            (user_id,)
        )
        return [dict(row) for row in cur.fetchall()]

def add_user_certificate(user_id: int, cert: dict) -> dict:
    name = cert.get("name", "").strip()
    issuer = cert.get("issuer", "").strip()
    if not name:
        raise ValueError("Certificate name is required.")
    if not issuer:
        raise ValueError("Certificate issuer is required.")

    issue_date = cert.get("issue_date", "").strip()
    expiry_date = cert.get("expiry_date", "").strip()
    cred_id = cert.get("credential_id", "").strip()
    cred_url = cert.get("credential_url", "").strip()

    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO user_certificates (user_id, name, issuer, issue_date, expiry_date, credential_id, credential_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, name, issuer, issue_date, expiry_date, cred_id, cred_url)
        )
        conn.commit()
        return {
            "id": cur.lastrowid, "name": name, "issuer": issuer,
            "issue_date": issue_date, "expiry_date": expiry_date,
            "credential_id": cred_id, "credential_url": cred_url
        }

def update_user_certificate(user_id: int, cert_id: int, updates: dict) -> dict:
    with get_connection() as conn:
        cur = conn.execute("SELECT id FROM user_certificates WHERE id = ? AND user_id = ?", (cert_id, user_id))
        if not cur.fetchone():
            raise KeyError("Certificate not found or access denied.")

        fields = []
        values = []
        for key in ["name", "issuer", "issue_date", "expiry_date", "credential_id", "credential_url"]:
            if key in updates and updates[key] is not None:
                val = str(updates[key]).strip()
                if key in ["name", "issuer"] and not val:
                    raise ValueError(f"{key.capitalize()} cannot be empty.")
                fields.append(f"{key} = ?")
                values.append(val)

        if fields:
            values.extend([cert_id, user_id])
            conn.execute(
                f"UPDATE user_certificates SET {', '.join(fields)} WHERE id = ? AND user_id = ?",
                tuple(values)
            )
            conn.commit()

        cur = conn.execute("SELECT id, name, issuer, issue_date, expiry_date, credential_id, credential_url FROM user_certificates WHERE id = ?", (cert_id,))
        return dict(cur.fetchone())

def delete_user_certificate(user_id: int, cert_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM user_certificates WHERE id = ? AND user_id = ?", (cert_id, user_id))
        conn.commit()
        if cur.rowcount == 0:
            raise KeyError("Certificate not found or access denied.")
        return True

# Assemble full candidate profile dictionary for scoring algorithms
def get_full_candidate_profile(user_id: int) -> dict:
    profile = get_user_profile(user_id)
    skills_rows = get_user_skills(user_id)
    projects_rows = get_user_projects(user_id)
    certs_rows = get_user_certificates(user_id)

    with get_connection() as conn:
        cur = conn.execute("SELECT full_name, email FROM users WHERE id = ?", (user_id,))
        user_row = cur.fetchone()
        user_name = user_row["full_name"] if user_row else "Candidate"

    skills_list = [s["skill_name"] for s in skills_rows]
    prof_map = {}
    prof_num = {"Beginner": 2, "Intermediate": 3, "Advanced": 4, "Expert": 5}
    for s in skills_rows:
        prof_map[s["skill_name"]] = prof_num.get(s["proficiency"], 3)

    projects_list = [
        f"{p['title']}: {p['description']}" for p in projects_rows
    ]
    certs_list = [
        f"{c['name']} ({c['issuer']})" for c in certs_rows
    ]

    return {
        "user_id": user_id,
        "name": user_name,
        "education": profile.get("education", ""),
        "branch": profile.get("branch", ""),
        "semester": profile.get("semester", ""),
        "target_career": profile.get("target_career", "Machine Learning Intern"),
        "resume_text": profile.get("resume_text", ""),
        "skills": skills_list,
        "proficiency": prof_map,
        "projects": projects_list,
        "certifications": certs_list,
        # Raw records for detailed UI display
        "raw_skills": skills_rows,
        "raw_projects": projects_rows,
        "raw_certificates": certs_rows
    }
