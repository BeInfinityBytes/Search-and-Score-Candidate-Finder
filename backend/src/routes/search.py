from pathlib import Path

from fastapi import APIRouter

from schemas.search import SearchRequest, SearchResponse
from services.search_service import run_search

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search_candidates(payload: SearchRequest) -> SearchResponse:
    data_path = Path(__file__).resolve().parents[1] / "data" / "candidates.json"
    result = run_search(
        requirement_text=payload.requirement,
        data_path=data_path,
        limit=payload.limit,
        min_score=payload.min_score,
        broaden_once=payload.broaden_once,
    )
    return SearchResponse(**result)
