import json
from pathlib import Path
from typing import Any, Dict, List


def _normalize_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()] if str(value).strip() else []


def _normalize_years(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_candidates(data_path: Path) -> List[Dict[str, Any]]:
    with data_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    normalized: List[Dict[str, Any]] = []
    for item in data:
        normalized.append(
            {
                "id": str(item.get("id", "")),
                "name": _normalize_string(item.get("name")),
                "title": _normalize_string(item.get("title")),
                "company": _normalize_string(item.get("company")),
                "industry": _normalize_string(item.get("industry")),
                "location": _normalize_string(item.get("location")),
                "years_experience": _normalize_years(item.get("years_experience")),
                "skills": _normalize_list(item.get("skills")),
            }
        )
    return normalized
