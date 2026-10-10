import sys
from pathlib import Path
import io

backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from main import app
from database import init_db

init_db()
client = TestClient(app)

def test_resume_text_extraction():
    sample_resume = """
    Prajwal S. Kumar
    Education: B.Tech in Computer Science
    
    Technical Skills:
    Python, SQL, PostgreSQL, Machine Learning, Scikit-learn, Git, FastAPI, React
    
    Projects:
    • Intelligent Search System: Built using Python and vector indexing.
    • Cloud Dashboard: Real-time telemetry monitoring.
    
    Certifications:
    • Deep Learning Specialization (Coursera)
    """
    res = client.post("/api/resume/analyze", data={"text": sample_resume})
    assert res.status_code == 200, res.text
    data = res.json()
    assert "Python" in data["skills"]
    assert "SQL" in data["skills"]
    assert "FastAPI" in data["skills"]
    assert len(data["projects"]) >= 1
    assert len(data["certifications"]) >= 1
    # Ensure Experience is completely absent
    assert "experience" not in data

def test_resume_txt_file_upload():
    content = b"Candidate Skills: Python, Docker, Kubernetes, Linux, Git."
    res = client.post(
        "/api/resume/analyze",
        files={"file": ("resume.txt", io.BytesIO(content), "text/plain")}
    )
    assert res.status_code == 200, res.text
    data = res.json()
    assert "Python" in data["skills"]
    assert "Git" in data["skills"]
    assert "experience" not in data

def test_empty_file_rejected():
    res = client.post(
        "/api/resume/analyze",
        files={"file": ("empty.txt", io.BytesIO(b""), "text/plain")}
    )
    assert res.status_code == 400
    assert "empty" in res.json()["detail"].lower()

def test_unsupported_file_type_rejected():
    res = client.post(
        "/api/resume/analyze",
        files={"file": ("resume.png", io.BytesIO(b"\x89PNG\r\n\x1a\n\x00"), "image/png")}
    )
    assert res.status_code == 400
    assert "unsupported" in res.json()["detail"].lower()

def test_oversized_file_rejected():
    # 5 MB + 1 KB
    huge_content = b"A" * (5 * 1024 * 1024 + 1024)
    res = client.post(
        "/api/resume/analyze",
        files={"file": ("huge.txt", io.BytesIO(huge_content), "text/plain")}
    )
    assert res.status_code == 413
    assert "5 mb" in res.json()["detail"].lower()

def test_empty_input_rejected():
    res = client.post("/api/resume/analyze", data={"text": "   "})
    assert res.status_code == 400
    assert "provide resume text" in res.json()["detail"].lower()

if __name__ == "__main__":
    test_resume_text_extraction()
    print("[PASS] test_resume_text_extraction")
    test_resume_txt_file_upload()
    print("[PASS] test_resume_txt_file_upload")
    test_empty_file_rejected()
    print("[PASS] test_empty_file_rejected")
    test_unsupported_file_type_rejected()
    print("[PASS] test_unsupported_file_type_rejected")
    test_oversized_file_rejected()
    print("[PASS] test_oversized_file_rejected")
    test_empty_input_rejected()
    print("[PASS] test_empty_input_rejected")
    print("\nAll Resume Upload & Analysis tests passed successfully!")
