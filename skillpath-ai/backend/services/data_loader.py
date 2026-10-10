from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def load_json(filename: str):
    with (DATA_DIR / filename).open("r", encoding="utf-8") as f:
        return json.load(f)

def careers():
    return load_json("careers.json")

def skills_catalog():
    return load_json("skills.json")

def opportunities():
    return load_json("opportunities.json")

def projects_catalog():
    return load_json("projects.json")
