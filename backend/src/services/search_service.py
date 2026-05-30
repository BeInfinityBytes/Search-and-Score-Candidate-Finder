from pathlib import Path
from typing import Any, Dict, List

from .data_loader import load_candidates
from .filtering import filter_candidates
from .llm_client import LLMClient
from .requirement_parser import parse_requirement
from .scorer import score_candidate


def run_search(
    requirement_text: str,
    data_path: Path,
    limit: int = 20,
    min_score: int = 60,
    broaden_once: bool = True,
) -> Dict[str, Any]:
    candidates = load_candidates(data_path)
    client = LLMClient()
    requirement = parse_requirement(requirement_text, client)

    strict_filtered = filter_candidates(candidates, requirement, strict=True)
    scored = _score_candidates(strict_filtered, requirement, client)
    scored_total = len(scored)

    results = [item for item in scored if item["score"] >= min_score]
    results.sort(key=lambda x: x["score"], reverse=True)

    if broaden_once and len(results) < limit:
        broad_filtered = filter_candidates(candidates, requirement, strict=False)
        new_pool = _exclude_existing(broad_filtered, results)
        broad_scored = _score_candidates(new_pool, requirement, client)
        scored_total += len(broad_scored)
        results.extend([item for item in broad_scored if item["score"] >= min_score])
        results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "requirement": requirement_text,
        "total_scored": scored_total,
        "results": results[:limit],
    }


def _score_candidates(
    candidates: List[Dict[str, Any]],
    requirement: Dict[str, Any],
    client: LLMClient,
) -> List[Dict[str, Any]]:
    scored: List[Dict[str, Any]] = []
    for candidate in candidates:
        score, reason = score_candidate(candidate, requirement, client)
        scored.append({**candidate, "score": score, "reason": reason})
    return scored


def _exclude_existing(
    candidates: List[Dict[str, Any]],
    existing: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    existing_ids = {item.get("id") for item in existing}
    return [candidate for candidate in candidates if candidate.get("id") not in existing_ids]
