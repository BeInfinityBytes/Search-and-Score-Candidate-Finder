from difflib import SequenceMatcher
from typing import Any, Dict, List


def _normalize(text: str) -> str:
    return text.strip().lower()


def _similar(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def _matches_any(target: str, options: List[str]) -> bool:
    if not target or not options:
        return False
    target_lower = _normalize(target)
    return any(_normalize(opt) in target_lower for opt in options)


def filter_candidates(
    candidates: List[Dict[str, Any]],
    requirement: Dict[str, Any],
    strict: bool = True,
) -> List[Dict[str, Any]]:
    title_req = _normalize(requirement.get("title", ""))
    industries = requirement.get("industries", [])
    locations = requirement.get("locations", [])

    filtered: List[Dict[str, Any]] = []
    for candidate in candidates:
        title = _normalize(candidate.get("title", ""))
        location = candidate.get("location", "")
        industry = candidate.get("industry", "")

        if title_req:
            if title and (title_req in title or _similar(title_req, title) >= 0.55):
                title_ok = True
            elif not title:
                title_ok = True
            else:
                title_ok = False
        else:
            title_ok = True

        if not title_ok:
            continue

        if strict and locations:
            if location and _matches_any(location, locations):
                location_ok = True
            elif not location:
                location_ok = True
            else:
                location_ok = False
        else:
            location_ok = True

        if not location_ok:
            continue

        if strict and industries:
            if industry and _matches_any(industry, industries):
                industry_ok = True
            elif not industry:
                industry_ok = True
            else:
                industry_ok = False
        else:
            industry_ok = True

        if not industry_ok:
            continue

        filtered.append(candidate)

    return filtered
