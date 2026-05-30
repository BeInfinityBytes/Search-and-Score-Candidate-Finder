import logging
from typing import Any, Dict, List, Tuple

from .llm_client import LLMClient

logger = logging.getLogger(__name__)


def _normalize(text: str) -> str:
    return text.strip().lower()


def _matches_any(target: str, options: List[str]) -> bool:
    if not target or not options:
        return False
    target_lower = _normalize(target)
    return any(_normalize(opt) in target_lower for opt in options)


def _heuristic_score(candidate: Dict[str, Any], requirement: Dict[str, Any]) -> Tuple[float, str]:
    score = 0.0
    reasons: List[str] = []

    title_req = _normalize(requirement.get("title", ""))
    cand_title = _normalize(candidate.get("title", ""))
    if title_req:
        if cand_title and title_req in cand_title:
            score += 35
            reasons.append("title matches")
        elif not cand_title:
            score += 10
            reasons.append("title missing")
    else:
        score += 10

    min_years = requirement.get("min_years")
    cand_years = candidate.get("years_experience")
    if min_years is not None:
        if cand_years is None:
            score += 10
            reasons.append("years missing")
        elif cand_years >= min_years:
            score += 25
            reasons.append(f"{cand_years} years experience")
        else:
            score += max(0.0, 25 * (cand_years / max(min_years, 1)))
            reasons.append(f"{cand_years} years experience")

    industries = requirement.get("industries", [])
    if industries:
        if _matches_any(candidate.get("industry", ""), industries):
            score += 20
            reasons.append("industry matches")
        elif not candidate.get("industry"):
            score += 8
            reasons.append("industry missing")

    locations = requirement.get("locations", [])
    if locations:
        if _matches_any(candidate.get("location", ""), locations):
            score += 15
            reasons.append("location matches")
        elif not candidate.get("location"):
            score += 5
            reasons.append("location missing")

    skills_req = requirement.get("skills", [])
    if skills_req:
        skills = [s.lower() for s in candidate.get("skills", [])]
        match_count = len([s for s in skills_req if s.lower() in skills])
        if match_count:
            score += min(5, match_count * 2)
            reasons.append("skills overlap")

    score = min(score, 100.0)
    reason = "; ".join(reasons) if reasons else "basic profile match"
    return score, reason


def score_candidate(candidate: Dict[str, Any], requirement: Dict[str, Any], client: LLMClient) -> Tuple[float, str]:
    if client.is_available():
        prompt = (
            "You are scoring candidate fit. Return JSON only with keys: score (0-100), reason (short). "
            "Weight title and years highest, then industry and location, then skills. "
            "If data is missing, reduce confidence but do not auto-reject. "
            f"Requirement: {requirement}. Candidate: {candidate}."
        )
        result = client.generate_json(prompt)
        if isinstance(result, dict) and "score" in result and "reason" in result:
            try:
                score = float(result.get("score", 0))
                reason = str(result.get("reason", ""))
                logger.info("Using Gemini score for candidate %s: %s", candidate.get("id"), score)
                return score, reason
            except (TypeError, ValueError):
                pass
        logger.warning("Gemini response missing score/reason; falling back for candidate %s", candidate.get("id"))

    score, reason = _heuristic_score(candidate, requirement)
    logger.info("Using heuristic score for candidate %s: %s", candidate.get("id"), score)
    return score, reason
