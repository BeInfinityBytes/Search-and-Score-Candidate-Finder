from typing import List, Optional

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    requirement: str = Field(..., description="Plain language hiring requirement")
    limit: int = Field(20, ge=1, le=50)
    min_score: int = Field(60, ge=0, le=100)
    broaden_once: bool = Field(True, description="Broaden search once if results are low")


class CandidateScore(BaseModel):
    id: str
    name: str
    title: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    years_experience: Optional[float] = None
    skills: List[str] = []
    score: float
    reason: str


class SearchResponse(BaseModel):
    requirement: str
    total_scored: int
    results: List[CandidateScore]
