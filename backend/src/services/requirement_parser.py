import re
from typing import Any, Dict, List

from .llm_client import LLMClient


def _fallback_parse(requirement: str) -> Dict[str, Any]:
    text = requirement.lower()
    years_match = re.search(r"(\d+)\s*\+?\s*years?", text)
    min_years = int(years_match.group(1)) if years_match else None

    title_part = requirement.split(",")[0].strip()
    title = title_part if title_part else ""

    industries: List[str] = []
    for keyword in ["fintech", "financial services", "banking", "saas", "healthcare"]:
        if keyword in text:
            industries.append(keyword)

    locations: List[str] = []
    location_match = re.search(r"in\s+(.+)$", text)
    if location_match:
        raw = location_match.group(1)
        for part in re.split(r"/|,|\bor\b", raw, flags=re.IGNORECASE):
            cleaned = part.strip()
            if cleaned:
                locations.append(cleaned)

    return {
        "title": title,
        "min_years": min_years,
        "industries": industries,
        "locations": locations,
        "skills": [],
    }


def parse_requirement(requirement: str, client: LLMClient) -> Dict[str, Any]:
    prompt = (
        "Extract a structured JSON from the hiring requirement. "
        "Return only JSON with keys: title (string), min_years (number or null), "
        "industries (array of strings), locations (array of strings), skills (array of strings). "
        "Requirement: "
        f"{requirement}"
    )

    parsed = client.generate_json(prompt)
    if isinstance(parsed, dict):
        return {
            "title": str(parsed.get("title", "")).strip(),
            "min_years": parsed.get("min_years"),
            "industries": [str(x).strip() for x in parsed.get("industries", []) if str(x).strip()],
            "locations": [str(x).strip() for x in parsed.get("locations", []) if str(x).strip()],
            "skills": [str(x).strip() for x in parsed.get("skills", []) if str(x).strip()],
        }

    return _fallback_parse(requirement)
