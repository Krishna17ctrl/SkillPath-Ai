import sys
from pathlib import Path

# Add backend directory to sys.path so services can be imported regardless of execution working directory
backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from services.skill_gap import analyze_skill_gap
from services.readiness import calculate_readiness
from services.skillpath import generate_skillpath

def test_skill_gap_categories():
    result = analyze_skill_gap(
        ["Python", "NumPy"],
        ["Python", "Machine Learning", "SQL"],
        {"Machine Learning": ["NumPy"]}
    )
    assert "Python" in result["strong"]
    assert "Machine Learning" in result["developing"]
    assert "SQL" in result["missing"]

def test_readiness_range():
    result = calculate_readiness(
        {"projects": ["EDA"], "certifications": []},
        {"required_count": 4, "strong": ["Python", "Pandas"], "developing": ["SQL"], "missing": ["Git"]}
    )
    assert 0 <= result["overall_score"] <= 100
    assert result["classification"] in {"Not Ready", "Needs Development", "Nearly Ready", "Ready"}

def test_skillpath_has_action():
    result = generate_skillpath({"missing": ["SQL"], "developing": [], "strong": []}, [])
    assert result["actions"]
    assert result["actions"][0]["priority"] == "High"

if __name__ == "__main__":
    test_skill_gap_categories()
    print("[PASS] test_skill_gap_categories")
    test_readiness_range()
    print("[PASS] test_readiness_range")
    test_skillpath_has_action()
    print("[PASS] test_skillpath_has_action")
    print("\nAll tests passed successfully!")


