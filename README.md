# SkillVeda Candidate Finder

## Overview
A FastAPI service that parses a hiring requirement, searches candidates from a JSON dataset, scores matches using an LLM (Gemini via REST), and returns the top candidates with brief reasons.

## How it Works
1. Load and normalize candidates from JSON.
2. Parse the requirement into structured fields (title, years, industries, locations, skills).
3. Apply a first-pass filter to reduce the candidate pool.
4. Score each candidate with Gemini (or a heuristic fallback if the LLM key is missing).
5. Rank and return the top 20 with reasons.
6. Optional: broaden search once if results are insufficient.

## Missing Data Handling
- Missing fields are treated as unknown, not disqualifying.
- Candidates with missing fields get a small confidence penalty but can still rank.

## Setup
1. Create a virtual environment in `backend`.
2. Install dependencies from `backend/requirements.txt`.
3. Add your Gemini key in `.env`.

## Run
From the backend folder:
- Start API: `uvicorn main:app --reload`

## API
- `POST /search`

Example body:
```
{
  "requirement": "Customer Success Manager, 3+ years, fintech / financial services background, in Bangalore or Delhi NCR.",
  "limit": 20,
  "min_score": 60,
  "broaden_once": true
}
```

## Sample Output (Top 20)
Requirement: “Customer Success Manager, 3+ years, fintech / financial services background, in Bangalore or Delhi NCR.”

1. Arjun Menon — 80 — title matches; 12.0 years experience; industry matches
2. Rahul Mukherjee — 80 — title matches; 8.0 years experience; industry matches
3. Riya Chopra — 75 — title matches; 4.0 years experience; location matches
4. Nikhil Mehta — 60 — title matches; 3.0 years experience
5. Naina Iyer — 60 — title matches; 3.0 years experience
6. Siddharth Nair — 60 — title matches; 3.0 years experience
7. Rakesh Bose — 60 — title matches; 5.0 years experience
8. Priya Agarwal — 60 — title matches; 9.0 years experience
9. Gaurav Ghosh — 60 — title matches; 7.0 years experience
10. Naina Mehta — 60 — title matches; 3.0 years experience
11. Ramya Das — 60 — title matches; 3.0 years experience
12. Mohit Kapoor — 60 — title matches; 6.0 years experience
13. Manish Rao — 60 — title matches; 12.0 years experience
14. Bhavna Agarwal — 60 — title matches; 3.0 years experience
15. Neha Reddy — 60 — title matches; 8.0 years experience
16. Hari Pillai — 60 — title matches; 7.0 years experience
17. Riya Khan — 60 — title matches; 4.0 years experience
18. Kavya Kulkarni — 60 — title matches; 7.0 years experience
19. Neha Chopra — 60 — title matches; 5.0 years experience
20. Farhan Kulkarni — 60 — title matches; 5.0 years experience

## Improvement With More Time
Embeddings-based semantic retrieval before LLM scoring to improve recall and reduce LLM calls I will implement this as I will get time to implement.
